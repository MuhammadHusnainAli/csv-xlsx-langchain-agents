import os
import sqlite3
import asyncio
import pandas as pd
from typing import List, Tuple
from concurrent.futures import ThreadPoolExecutor
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from langchain_community.utilities.sql_database import SQLDatabase
from app.config import settings
from app.api.schema.upload import TableInfo
from app.utils.logger import logger


class DatabaseService:
    
    @staticmethod
    def get_session_dir(session_id: str) -> str:
        session_dir = os.path.join(settings.DATA_DIR, session_id)
        os.makedirs(session_dir, exist_ok=True)
        return session_dir
    
    @staticmethod
    def get_database_path(session_id: str) -> str:
        session_dir = DatabaseService.get_session_dir(session_id)
        return os.path.join(session_dir, "data.db")
    
    @staticmethod
    def sanitize_table_name(name: str) -> str:
        sanitized = "".join(c if c.isalnum() or c == "_" else "_" for c in name)
        if sanitized[0].isdigit():
            sanitized = f"table_{sanitized}"
        return sanitized
    
    @staticmethod
    def sanitize_column_name(name: str) -> str:
        sanitized = "".join(c if c.isalnum() or c == "_" else "_" for c in str(name))
        if sanitized and sanitized[0].isdigit():
            sanitized = f"col_{sanitized}"
        return sanitized if sanitized else "unnamed_column"
    
    @staticmethod
    def _process_sheet(xlsx_path: str, sheet_name: str, session_id: str) -> Tuple[str, pd.DataFrame]:
        df = pd.read_excel(xlsx_path, sheet_name=sheet_name)
        table_name = DatabaseService.sanitize_table_name(sheet_name)
        df.columns = [DatabaseService.sanitize_column_name(col) for col in df.columns]
        logger.sheet_processing(session_id, sheet_name, list(df.columns), len(df))
        return table_name, df
    
    @staticmethod
    async def convert_csv_to_sqlite(file_path: str, session_id: str) -> Tuple[str, List[TableInfo]]:
        db_path = DatabaseService.get_database_path(session_id)
        filename = os.path.basename(file_path)
        
        loop = asyncio.get_event_loop()
        with ThreadPoolExecutor() as executor:
            df = await loop.run_in_executor(executor, pd.read_csv, file_path)
        
        table_name = DatabaseService.sanitize_table_name(
            os.path.splitext(filename)[0]
        )
        
        df.columns = [DatabaseService.sanitize_column_name(col) for col in df.columns]
        
        logger.csv_processing(session_id, filename, list(df.columns), len(df))
        
        conn = sqlite3.connect(db_path)
        df.to_sql(table_name, conn, if_exists="replace", index=False)
        conn.close()
        
        tables = [TableInfo(
            table_name=table_name,
            columns=list(df.columns),
            row_count=len(df)
        )]
        
        logger.database_created(session_id, db_path, len(tables))
        
        return db_path, tables
    
    @staticmethod
    async def convert_xlsx_to_sqlite(file_path: str, session_id: str) -> Tuple[str, List[TableInfo]]:
        db_path = DatabaseService.get_database_path(session_id)
        
        xlsx = pd.ExcelFile(file_path)
        sheet_names = xlsx.sheet_names
        
        logger.info(f"Processing XLSX | session={session_id} | sheets={len(sheet_names)}")
        
        loop = asyncio.get_event_loop()
        with ThreadPoolExecutor() as executor:
            tasks = [
                loop.run_in_executor(
                    executor, 
                    DatabaseService._process_sheet, 
                    file_path, 
                    sheet_name,
                    session_id
                )
                for sheet_name in sheet_names
            ]
            results = await asyncio.gather(*tasks)
        
        conn = sqlite3.connect(db_path)
        tables = []
        
        for table_name, df in results:
            df.to_sql(table_name, conn, if_exists="replace", index=False)
            tables.append(TableInfo(
                table_name=table_name,
                columns=list(df.columns),
                row_count=len(df)
            ))
        
        conn.close()
        
        logger.database_created(session_id, db_path, len(tables))
        
        return db_path, tables
    
    @staticmethod
    async def convert_to_sqlite(file_path: str, session_id: str) -> Tuple[str, List[TableInfo]]:
        file_ext = os.path.splitext(file_path)[1].lower()
        
        if file_ext == ".csv":
            return await DatabaseService.convert_csv_to_sqlite(file_path, session_id)
        elif file_ext == ".xlsx":
            return await DatabaseService.convert_xlsx_to_sqlite(file_path, session_id)
        else:
            logger.error(f"Unsupported file type: {file_ext}")
            raise ValueError(f"Unsupported file type: {file_ext}")
    
    @staticmethod
    def get_engine(session_id: str):
        db_path = DatabaseService.get_database_path(session_id)
        connection = sqlite3.connect(db_path, check_same_thread=False)
        return create_engine(
            "sqlite://",
            creator=lambda: connection,
            poolclass=StaticPool,
            connect_args={"check_same_thread": False},
        )
    
    @staticmethod
    def get_sql_database(session_id: str) -> SQLDatabase:
        engine = DatabaseService.get_engine(session_id)
        return SQLDatabase(engine)
