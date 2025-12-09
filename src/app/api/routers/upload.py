import os
import uuid
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.api.schema.upload import UploadResponse
from app.config import settings
from app.services.database import DatabaseService
from app.utils.logger import logger

router = APIRouter(tags=["upload"])


@router.post("/files", response_model=UploadResponse)
async def upload_file(
    file: UploadFile = File(...)
) -> UploadResponse:
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in settings.ALLOWED_EXTENSIONS:
        logger.error(f"Invalid file type: {file_ext} | file={file.filename}")
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Only {', '.join(settings.ALLOWED_EXTENSIONS)} files are allowed."
        )
    
    session_id = str(uuid.uuid4())
    
    logger.file_upload(file.filename, session_id)
    
    session_dir = DatabaseService.get_session_dir(session_id)
    file_path = os.path.join(session_dir, file.filename)
    
    content = await file.read()
    with open(file_path, "wb") as f:
        f.write(content)
    
    db_path, tables = await DatabaseService.convert_to_sqlite(file_path, session_id)
    
    logger.success(f"File processed | session={session_id} | tables={len(tables)}")
    
    return UploadResponse(
        session_id=session_id,
        filename=file.filename,
        database_path=db_path,
        tables=tables,
        message="File uploaded and converted to SQLite successfully"
    )
