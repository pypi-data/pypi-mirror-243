import functools
import logging
import re
import sys
import textwrap
from typing import Optional

import fire
from termcolor import colored

from .kadia_ai import KadiaAI
from .exceptions import QdrantStorageNotAvailableError


def exception_handler(func):
    @functools.wraps(func)
    async def wrapper_func(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except QdrantStorageNotAvailableError as e:
            print(
                f"{colored('INFO', 'red')}: Cannot connect to Qdrant: {e.info}\n"
                f"{colored('HINT', 'yellow')}: Launch qdrant using `docker run -p 6333:6333 -p 6334:6334 qdrant/qdrant`",
                file=sys.stderr,
            )
            raise

    return wrapper_func


class KadiaCli:
    def __init__(self, kadia: Optional[KadiaAI] = None):
        self.kadia = kadia or KadiaAI()

    async def add_all_documents(self, query: str = "", batch_size: int = 200):
        async with self.kadia as kadia:
            batch = []
            async for document in kadia.data_source.stream_documents(query=query):
                logging.getLogger("statbox").info(
                    {"action": "collect_document", "document": document.document_id}
                )
                batch.append(document)
                if len(batch) >= batch_size:
                    await self.kadia.upsert_documents(batch)
                    batch = []
            if batch:
                await self.kadia.upsert_documents(batch)

    @exception_handler
    async def chat_doc(
        self,
        document_query: str,
        query: str,
        n_chunks: int = 5,
        minimum_score: float = 0.5,
    ):
        """
        Ask a question about content of document identified by DOI.

        :param document_query: query that returns unique document
        :param query: Text query to the document
        :param n_chunks: the number of chunks to extract
            more means more tokens to use and more precision in answer
        :param minimum_score:
        """
        async with self.kadia as kadia:
            print(f"{colored('Document', 'green')}: {document_query}")
            print(f"{colored('Q', 'green')}: {query}")
            kadia_response = await kadia.chat_document(
                document_query,
                query,
                n_chunks,
                minimum_score=minimum_score,
            )
            print(f"{colored('A', 'green')}: {kadia_response.answer}")

    @exception_handler
    async def chat_sci(
        self,
        query: str,
        n_chunks: int = 5,
        n_documents: int = 10,
        minimum_score: float = 0.5,
    ):
        """
        Ask a general questions

        :param query: text query to the document
        :param n_chunks: the number of chunks to extract
            more means more tokens to use and more precision in answer
        :param n_documents: the number of chunks to extract
            more means more tokens to use and more precision in answer
        :param minimum_score:
        """
        async with self.kadia as kadia:
            print(f"{colored('Q', 'green')}: {query}")
            kadia_response = await kadia.chat_science(
                query=query,
                n_chunks=n_chunks,
                n_documents=n_documents,
                minimum_score=minimum_score,
            )
            answer = re.sub(
                r"\(DOI:\s*([^)]+)\)",
                r"(https://doi.org/\g<1>)",
                kadia_response.answer,
            )
            references = []
            visited = set()
            for chunk in kadia_response.chunks:
                field, value = chunk.document_id.split(":", 1)
                document_id = f"{field}:{value}"
                if document_id in visited:
                    continue
                visited.add(document_id)
                title = chunk.title.replace("\n", " - ")
                references.append(f"{document_id}: {title}")
            references = "\n".join(references)
            print(f"{colored('A', 'green')}: {answer}")
            print(
                f"{colored('References', 'green')}:\n{textwrap.indent(references, ' - ')}"
            )

    @exception_handler
    async def chunk_document(
        self,
        document_query: str,
    ):
        """
        Ask a question about content of document identified by DOI.

        :param document_query: query that returns unique document
        """
        async with self.kadia as kadia:
            print(f"{colored('Document', 'green')}: {document_query}")
            documents = await kadia.data_source.search_documents(document_query, limit=1)
            document_chunks = await kadia.generate_chunks_from_document(documents[0])
            print(f"{colored('Chunks', 'green')}: {document_chunks}")

    @exception_handler
    async def sum_doc(self, document_query: str):
        """
        Summarization of the document

        :param document_query: query that returns unique document
        """
        async with self.kadia as kadia:
            print(f"{colored('Document', 'green')}: {document_query}")
            kadia_response = await kadia.summarize_document(document_query)
            print(f"{colored('Summarization', 'green')}: {kadia_response.answer}")

    @exception_handler
    async def semantic_search(
        self,
        query: str,
        n_chunks: int = 5,
        n_documents: int = 10,
        minimum_score: float = 0.5,
        use_only_keywords: bool = True,
    ):
        """
        Search related to query text chunks among `n` documents

        :param query: query to STC
        :param n_chunks: number of chunks to return
        :param n_documents: the number of documents to extract from STC
        :param minimum_score:
        :param use_only_keywords:
        """
        async with self.kadia as kadia:
            print(f"{colored('Q', 'green')}: {query}")
            scored_chunks = await kadia.semantic_search(
                query=query,
                n_chunks=n_chunks,
                n_documents=n_documents,
                minimum_score=minimum_score,
                use_only_keywords=use_only_keywords,
            )
            references = []
            for scored_chunk in scored_chunks:
                field, value = scored_chunk.chunk.document_id.split(":", 1)
                document_id = f"{field}:{value}"
                title = scored_chunk.chunk.title.replace("\n", " - ")
                references.append(
                    f" - {document_id}: {title}\n   {scored_chunk.chunk.text}"
                )
            references = "\n".join(references)
            print(f"{colored('References', 'green')}:\n{references}")


def kadia_cli(debug: bool = False):
    """
    :param debug: add debugging output
    :return:
    """
    logging.basicConfig(
        stream=sys.stdout, level=logging.INFO if debug else logging.ERROR
    )
    kadia = KadiaCli()
    return {
        "add-all-documents": kadia.add_all_documents,
        "chat-doc": kadia.chat_doc,
        "chat-sci": kadia.chat_sci,
        "chunk_document": kadia.chunk_document,
        "semantic-search": kadia.semantic_search,
        "sum-doc": kadia.sum_doc,
        "write-config": kadia.kadia.ensure_config,
    }


def run():
    fire.Fire(kadia_cli, name="kadia")


if __name__ == "__main__":
    run()
