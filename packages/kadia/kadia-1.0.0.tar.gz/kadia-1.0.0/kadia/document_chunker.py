import logging
from dataclasses import dataclass
from datetime import datetime
from typing import (
    List,
    Optional,
)

from langchain.text_splitter import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter
from unstructured.cleaners.core import clean

from .data_source.base import SourceDocument

BANNED_SECTIONS = {
    'author contribution',
    'data availability statement',
    'declaration of competing interest',
    'acknowledgments',
    'acknowledgements',
    'supporting information',
    'conflict of interest disclosures',
    'conflict of interest',
    'conflict of interest statement',
    'ethics statement',
    'references',
    'external links',
    'further reading',
    'works cited',
    'bibliography',
    'notes',
    'sources',
    'footnotes',
    'suggested readings',
}


@dataclass
class Chunk:
    document_id: Optional[str]
    chunk_id: Optional[int]
    title: Optional[str]
    length: Optional[int]
    # What should be stored in the database
    text: Optional[str] = None
    # What should be embedded, defaults to `text` if None
    real_text: Optional[str] = None
    embedding: Optional[bytes] = None
    with_content: bool = False


class DocumentChunker:
    def __init__(self, text_splitter, chunk_size: int = 1024, chunk_overlap: int = 128, add_metadata: bool = False):
        self.text_splitter = text_splitter
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.add_metadata = add_metadata

    def to_chunks(self, source_document: SourceDocument) -> List[Chunk]:
        logging.getLogger('statbox').info({
            'action': 'chunking',
            'document_id': source_document.document_id,
            'mode': 'kadia',
        })
        document = source_document.document
        abstract = document.get('abstract', '')
        content = document.get('content', '')

        headers_to_split_on = [
            ("#", "h1"),
            ("##", "h2"),
            ("###", "h3"),
            ("####", "h4"),
            ("#####", "h5"),
            ("######", "h6"),
        ]

        # MD splits
        markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
        md_header_splits = markdown_splitter.split_text(abstract + '\n\n' + content)

        # Char-level splits

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap
        )

        # Split
        splits = text_splitter.split_documents(md_header_splits)
        chunks = []

        for chunk_id, split in enumerate(splits):
            chunk_text = clean(str(split.page_content), extra_whitespace=True, dashes=True, bullets=True, trailing_punctuation=True)
            parts = [chunk_text]
            title_parts = [document["title"]]
            for hn in range(6):
                if hn_value := split.metadata.get(f'h{hn}'):
                    title_parts.append(hn_value)
            if self.add_metadata:
                parts.append(f'TITLE: {" ".join(title_parts)}')
                if 'issued_at' in document:
                    issued_at = datetime.utcfromtimestamp(document['issued_at'])
                    parts.append(f'YEAR: {issued_at.year}')
                if 'metadata' in document and 'keywords' in document['metadata']:
                    keywords = ', '.join(document['metadata']['keywords'])
                    parts.append(f'KEYWORDS: {keywords}')
                if 'tags' in document:
                    tags = ', '.join(document['tags'])
                    parts.append(f'TAGS: {tags}')
            text = '\n'.join(parts)
            chunks.append(Chunk(
                real_text=text,
                text=chunk_text,
                document_id=source_document.document_id,
                length=len(text),
                chunk_id=chunk_id,
                title='\n'.join(title_parts),
                with_content=bool(content),
            ))
            chunk_id += 1
        return chunks
