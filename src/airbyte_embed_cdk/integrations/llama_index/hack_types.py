from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass
class LCDocument:
    page_content: str
    metadata: dict

    def __init__(self, page_content: str = "", metadata: Dict[str, Any] = {}) -> None:
        self.metadata = metadata
        self.page_content = page_content


@dataclass
class Document:
    text: str
    metadata: dict

    def __init__(self, text: str = "", metadata: Dict[str, Any] = {}) -> None:
        self.metadata = metadata
        self.text = text

    def to_langchain_format(self) -> LCDocument:
        metadata = self.metadata or {}
        return LCDocument(page_content=self.text, metadata=metadata)

    @classmethod
    def from_langchain_format(cls, doc: LCDocument) -> "Document":
        return cls(text=doc.page_content, metadata=doc.metadata)


class BaseReader(ABC):
    """Utilities for loading data from a directory."""

    @abstractmethod
    def load_data(self, *args: Any, **load_kwargs: Any) -> List[Document]:
        """Load data from the input directory."""

    def load_langchain_documents(self, **load_kwargs: Any) -> List[LCDocument]:
        """Load data in LangChain document format."""
        docs = self.load_data(**load_kwargs)
        return [d.to_langchain_format() for d in docs]
