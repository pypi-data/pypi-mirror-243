from dataclasses import dataclass
from typing import (
    List,
    Optional,
)


@dataclass
class SourceDocument:
    document: dict
    document_id: str


class BaseDataSource:
    async def stream_documents(
        self,
        query: str,
        limit: int = 0,
    ) -> List[SourceDocument]:
        raise NotImplementedError()

    async def search_documents(
        self, query: str, limit: int = 5, sources: Optional[List[str]] = None
    ) -> List[SourceDocument]:
        raise NotImplementedError()
