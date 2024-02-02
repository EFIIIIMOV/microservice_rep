import datetime
from uuid import UUID

from app.models.document import Document
from typing import Optional

documents: list[Document] = [
    Document(doc_id=0, ord_id=0, type='test_doc_type_0', create_date=datetime.datetime.now(),
             completion_date=datetime.datetime.now(), doc='test_doc_doc_0'),
    Document(doc_id=1, ord_id=1, type='test_doc_type_1', create_date=datetime.datetime.now(),
             completion_date=datetime.datetime.now(), doc='test_doc_doc_1'),
    Document(doc_id=2, ord_id=2, type='test_doc_type_2', create_date=datetime.datetime.now(),
             completion_date=datetime.datetime.now(), doc='test_doc_doc_2'),
]


class DocumentRepo():
    def __init__(self, clear: bool = False) -> None:
        if clear:
            documents.clear()

    def get_document(self) -> list[Document]:
        return documents

    # def get_doc_by_id(self, id: UUID) -> Document:
    #     for d in documents:
    #         if d.id == id:
    #             return d
    #
    #     raise KeyError

    def get_document_by_id(self, id: int) -> Document:
        for d in documents:
            if d.doc_id == id:
                return d

        raise KeyError

    def create_document(self, doc: Document) -> Document:
        if len([d for d in documents if d.doc_id == doc.doc_id]) > 0:
            raise KeyError

        documents.append(doc)
        return doc

    def delete_doc(self, id: int) -> Optional[Document]:
        for i, document in enumerate(documents):
            if document.doc_id == id:
                deleted_document = documents.pop(i)
                return deleted_document

        return None
