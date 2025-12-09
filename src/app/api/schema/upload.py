from pydantic import BaseModel
from typing import List


class TableInfo(BaseModel):
    table_name: str
    columns: List[str]
    row_count: int


class UploadResponse(BaseModel):
    session_id: str
    filename: str
    database_path: str
    tables: List[TableInfo]
    message: str
