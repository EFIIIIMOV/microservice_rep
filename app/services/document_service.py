# 1. Поменять int на UUID в функциях

from uuid import UUID
from fastapi import Depends
from datetime import datetime

from app.models.document import Document
from app.repositories.db_document_repo import DocumentRepo
from app.repositories.local_document_repo import DocumentRepo


# from app.repositories.local_deliveryman_repo import DeliverymenRepo


class DocumentService():
    order_repo: DocumentRepo

    # deliveryman_repo: DeliverymenRepo

    def __init__(self, document_repo: DocumentRepo = Depends(DocumentRepo)) -> None:
        self.document_repo = document_repo
        # self.deliveryman_repo = DeliverymenRepo()

    def get_document(self) -> list[Document]:
        return self.document_repo.get_document()

    def create_document(self, doc_id: int, ord_id: int, type: str, create_date: datetime, completion_date: datetime,
                        doc: str) -> Document:
        document = Document(doc_id=doc_id, ord_id=ord_id, type=type, create_date=create_date,
                            completion_date=completion_date, doc=doc)

        return self.document_repo.create_document(document)

    def delete_document(self, doc_id: int) -> None:
        return self.document_repo.delete_doc(doc_id)
