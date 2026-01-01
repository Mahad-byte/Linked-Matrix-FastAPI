from fastapi import APIRouter, status
from beanie import PydanticObjectId

from models.content import Document
from schemas.schema import ResponseSchema, DocumentSchema
from schemas.update_schema import DocumentUpdateSchema


router = APIRouter()


@router.post("/documents", status_code=status.HTTP_201_CREATED)
async def create_document(payload: DocumentSchema):
    
    document = Document(name=payload.name, description=payload.description, 
                      file=payload.file, version=payload.version, project=payload.project)
    await document.insert()
    return ResponseSchema(message="Success")


@router.get("/documents", status_code=status.HTTP_200_OK)
async def get_all_document():
    return await Document.find_all().to_list()


@router.get("/documents/{document_id}", status_code=status.HTTP_200_OK)
async def get_specific_documents(document_id: PydanticObjectId):
    return await Document.get(document_id)


@router.put("/documents/{document_id}", status_code=status.HTTP_200_OK)
async def get_document_with_id(document_id: PydanticObjectId, payload: DocumentUpdateSchema):
    document = await Document.get(document_id)
    update_data = payload.dict(exclude_unset=True)

    await document.set(update_data)
    return document


@router.delete("/documents/{documents_id}", status_code=status.HTTP_200_OK)
async def delete_document_with_id(documents_id: PydanticObjectId):
        document = await Document.get(documents_id)
        await document.delete()
        return ResponseSchema(message="Success")
