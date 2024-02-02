import enum
from uuid import UUID
from datetime import datetime
from pydantic import ConfigDict, BaseModel


class Document(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    # doc_id: UUID
    doc_id: UUID
    # ord_id: UUID
    ord_id: UUID
    type: str
    create_date: datetime
    completion_date: datetime
    doc: str


class CreateDocumentRequest(BaseModel):
    # doc_id: UUID
    doc_id: UUID
    # ord_id: UUID
    ord_id: UUID
    type: str
    create_date: datetime
    completion_date: datetime
    doc: str
