from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Body

from app.services.document_service import DocumentService
from app.models.document import Document, CreateDocumentRequest

document_router = APIRouter(prefix='/document', tags=['Document'])


@document_router.get('/')
def get_document(document_service: DocumentService = Depends(DocumentService)) -> list[Document]:
    return document_service.get_document()


@document_router.post('/')
def add_order(
        document_info: CreateDocumentRequest,
        order_service: DocumentService = Depends(DocumentService)
) -> Document:
    try:
        document = order_service.create_document(document_info.doc_id, document_info.ord_id, document_info.type,
                                                 document_info.create_date, document_info.completion_date,
                                                 document_info.doc)
        return document.dict()
    except KeyError:
        raise HTTPException(400, f'Order with id={document_info.doc_id} already exists')


@document_router.post('/{id}/delete')
def delete_order(id: UUID, document_service: DocumentService = Depends(DocumentService)) -> Document:
    try:
        document = document_service.delete_document(id)
        return document.dict()
    except KeyError:
        raise HTTPException(404, f'Document with id={id} not found')
