from fastapi import APIRouter, status, UploadFile, File, Form, HTTPException
from beanie import PydanticObjectId

from typing import List, Optional
from pathlib import Path

from models.content import Document
from schemas.schema import ResponseSchema
from schemas.update_schema import DocumentUpdateSchema


router = APIRouter()


@router.post("/documents", status_code=status.HTTP_201_CREATED)
async def create_document(
    name: str = Form(...),
    description: str = Form(None),
    version: int = Form(...),
    project: List[str] = Form(...),
    file: UploadFile = File(...)
):
    upload_dir = Path("uploads") / "documents"
    upload_dir.mkdir(parents=True, exist_ok=True)

    try:
        file_path = upload_dir / file.filename
        contents = await file.read()
        with open(file_path, "wb") as f:
            f.write(contents)
        await file.close()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not save file: {e}")

    # Convert projects to PydanticObjectId
    try:
        project_ids = [PydanticObjectId(p) for p in project]
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid project id in project list: {e}")

    document = Document(
        name=name,
        description=description,
        file=str(file_path),
        version=version,
        project=project_ids,
    )
    await document.insert()
    return ResponseSchema(message="Success")


@router.get("/documents", status_code=status.HTTP_200_OK)
async def get_all_document():
    return await Document.find_all().to_list()


@router.get("/documents/{document_id}", status_code=status.HTTP_200_OK)
async def get_specific_documents(document_id: PydanticObjectId):
    return await Document.get(document_id)


@router.put("/documents/{document_id}", status_code=status.HTTP_200_OK)
async def update_document(
    document_id: PydanticObjectId,
    name: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    version: Optional[int] = Form(None),
    project: Optional[List[str]] = Form(None),
    file: Optional[UploadFile] = File(None),
):
    document = await Document.get(document_id)
    
    update_data = {}
    update_data["name"] = name
    update_data["description"] = description
    update_data["version"] = version


    project_ids = [PydanticObjectId(p) for p in project]
    update_data["project"] = project_ids

    upload_dir = Path("uploads") / "documents"
    upload_dir.mkdir(parents=True, exist_ok=True)
    try:
        file_path = upload_dir / file.filename
        contents = await file.read()
        with open(file_path, "wb") as f:
            f.write(contents)
        await file.close()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not save file: {e}")

    old_file_path = Path(document.file) if getattr(document, "file", None) else None
    if old_file_path and old_file_path.exists():
        old_file_path.unlink()
    
    update_data["file"] = str(file_path)

    await document.set(update_data)
    updated = await Document.get(document_id)
    return updated


@router.delete("/documents/{documents_id}", status_code=status.HTTP_200_OK)
async def delete_document_with_id(documents_id: PydanticObjectId):
        document = await Document.get(documents_id)
        await document.delete()
        return ResponseSchema(message="Success")
