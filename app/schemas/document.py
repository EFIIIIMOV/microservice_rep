from sqlalchemy import Column, String, DateTime, Integer
from sqlalchemy.dialects.postgresql import UUID
from app.schemas.base_schema import Base


class Document(Base):
    __tablename__ = 'document'

    # doc_id: Column(UUID(as_uuid=True), primary_key=True)
    # ord_id: Column(UUID(as_uuid=True))
    doc_id = Column(UUID(as_uuid=True), primary_key=True)
    ord_id = Column(UUID(as_uuid=True), nullable=False)
    type = Column(String, nullable=False)
    create_date = Column(DateTime, nullable=False)
    doc = Column(String, nullable=False)
