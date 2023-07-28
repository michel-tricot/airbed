from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List


@dataclass
class Document:
    page_content: str
    metadata: dict

    def __init__(self, page_content=None, metadata=None):
        self.metadata = metadata
        self.page_content = page_content


class BaseLoader(ABC):
    """Utilities for loading data from a directory."""

    @abstractmethod
    def load(self) -> List[Document]:
        """Load data from the input directory."""
