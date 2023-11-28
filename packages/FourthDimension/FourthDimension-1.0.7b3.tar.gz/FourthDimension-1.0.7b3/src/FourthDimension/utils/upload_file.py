import json
from FourthDimension.doc.pydantic import Field
from FourthDimension.doc.document import Document


class DocumentSerializable(Document):
    """Class for storing a piece of text and associated metadata."""

    page_content: str
    metadata: dict = Field(default_factory=dict)

    @property
    def lc_serializable(self) -> bool:
        return True

    def __repr__(self):
        return f"Document(page_content='{self.page_content[:50]}...', metadata={self.metadata})"

    def __str__(self):
        return self.__repr__()

    def to_json(self) -> str:
        """Convert the Document object to a JSON string."""
        return json.dumps(
            {
                "page_content": self.page_content,
                "metadata": self.metadata,
            }
        )

    @classmethod
    def from_json(cls, json_str: str):
        """Create a Document object from a JSON string."""
        data = json.loads(json_str)
        return cls(page_content=data["page_content"], metadata=data["metadata"])
