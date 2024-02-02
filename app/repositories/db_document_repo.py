import traceback
from uuid import UUID
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.document import Document
from app.schemas.document import Document as DBDocument


# from app.repositories.local_deliveryman_repo import DeliverymenRepo


class DocumentRepo():
    db: Session

    # deliveryman_repo: DeliverymenRepo

    def __init__(self) -> None:
        self.db = next(get_db())
        # self.deliveryman_repo = DeliverymenRepo()

    def _map_to_model(self, document: DBDocument) -> Document:
        result = Document.from_orm(document)
        # if document.deliveryman_id != None:
        #     result.deliveryman = self.deliveryman_repo.get_deliveryman_by_id(
        #         document.deliveryman_id)

        return result

    def _map_to_schema(self, document: Document) -> DBDocument:
        data = dict(document)
        # del data['deliveryman']
        # data['deliveryman_id'] = document.deliveryman.id if document.deliveryman != None else None
        result = DBDocument(**data)

        return result

    def get_document(self) -> list[Document]:
        documents = []
        for d in self.db.query(DBDocument).all():
            documents.append(self._map_to_model(d))
        return documents

    # def get_document_by_id(self, id: UUID) -> Document:
    #     document = self.db \
    #         .query(DBDocument) \
    #         .filter(DBDocument.id == id) \
    #         .first()
    #
    #     if document == None:
    #         raise KeyError
    #     return self._map_to_model(document)

    def get_document_by_id(self, id: int) -> Document:
        document = self.db \
            .query(DBDocument) \
            .filter(DBDocument.id == id) \
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

    def set_status(self, document: Document) -> Document:
        db_document = self.db.query(DBDocument).filter(
            DBDocument.id == document.id).first()
        db_document.status = document.status
        self.db.commit()
        return self._map_to_model(db_document)

    # def set_deliveryman(self, document: Document) -> Document:
    #     db_document = self.db.query(DBDocument).filter(
    #         DBDocument.id == document.id).first()
    #     db_document.deliveryman_id = document.deliveryman.id
    #     self.db.commit()
    #     return self._map_to_model(db_document)

    # def delete_document(self, doc_id: UUID) -> None:
    #     document = self.db.query(DBDocument).filter(DBDocument.id == doc_id).first()
    #     if document:
    #         self.db.delete(document)
    #         self.db.commit()
    #     else:
    #         raise KeyError("Document not found")

    def delete_document(self, doc_id: int) -> None:
        document = self.db.query(DBDocument).filter(DBDocument.id == doc_id).first()
        if document:
            self.db.delete(document)
            self.db.commit()
        else:
            raise KeyError("Document not found")
