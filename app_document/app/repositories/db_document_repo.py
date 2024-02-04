import traceback
from uuid import UUID
from sqlalchemy.orm import Session

from app_order.app.database import get_db_doc
from app_document.app.models.document import Document
from app_document.app.schemas.document import Document as DBDocument


class DocumentRepo():
    db: Session

    def __init__(self) -> None:
        self.db = next(get_db_doc())

    def _map_to_model(self, document: DBDocument) -> Document:
        result = Document.from_orm(document)

        return result

    def _map_to_schema(self, document: Document) -> DBDocument:
        data = dict(document)
        result = DBDocument(**data)

        return result

    def get_document(self) -> list[Document]:
        documents = []
        for d in self.db.query(DBDocument).all():
            documents.append(self._map_to_model(d))

        return documents

    def get_document_by_id(self, id: UUID) -> Document:
        document = self.db \
            .query(DBDocument) \
            .filter(DBDocument.doc_id == id) \
            .first()

        if document == None:
            raise KeyError
        return self._map_to_model(document)

    def create_document(self, document: Document) -> Document:
        try:
            db_document = self._map_to_schema(document)
            self.db.add(db_document)
            self.db.commit()
            return self._map_to_model(db_document)
        except:
            traceback.print_exc()
            raise KeyError
