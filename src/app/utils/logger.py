import logging
import sys
from typing import List, Optional


class Logger:
    _instance: Optional["Logger"] = None
    _logger: Optional[logging.Logger] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._setup_logger()
        return cls._instance
    
    def _setup_logger(self):
        self._logger = logging.getLogger("csv-xlsx-agent")
        self._logger.setLevel(logging.DEBUG)
        
        if not self._logger.handlers:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(logging.DEBUG)
            
            formatter = logging.Formatter(
                "\033[90m%(asctime)s\033[0m | "
                "%(levelname)s | "
                "\033[36m%(name)s\033[0m | "
                "%(message)s",
                datefmt="%Y-%m-%d %H:%M:%S"
            )
            console_handler.setFormatter(formatter)
            self._logger.addHandler(console_handler)
    
    def info(self, message: str):
        self._logger.info(f"\033[32m{message}\033[0m")
    
    def debug(self, message: str):
        self._logger.debug(f"\033[90m{message}\033[0m")
    
    def warning(self, message: str):
        self._logger.warning(f"\033[33m{message}\033[0m")
    
    def error(self, message: str):
        self._logger.error(f"\033[31m{message}\033[0m")
    
    def success(self, message: str):
        self._logger.info(f"\033[32m[SUCCESS] {message}\033[0m")
    
    def file_upload(self, filename: str, session_id: str):
        self._logger.info(f"\033[34m[FILE UPLOAD]\033[0m | session={session_id} | file={filename}")
    
    def sheet_processing(self, session_id: str, sheet_name: str, columns: List[str], row_count: int):
        cols_str = ", ".join(columns[:5])
        if len(columns) > 5:
            cols_str += f"... (+{len(columns) - 5} more)"
        self._logger.info(
            f"\033[35m[SHEET]\033[0m | session={session_id} | "
            f"sheet={sheet_name} | rows={row_count} | columns=[{cols_str}]"
        )
    
    def database_created(self, session_id: str, db_path: str, table_count: int):
        self._logger.info(
            f"\033[32m[DATABASE CREATED]\033[0m | session={session_id} | "
            f"tables={table_count} | path={db_path}"
        )
    
    def chat_request(self, session_id: str, message: str):
        msg_preview = message[:50] + "..." if len(message) > 50 else message
        self._logger.info(f"\033[36m[CHAT REQUEST]\033[0m | session={session_id} | message={msg_preview}")
    
    def sql_query(self, query: str, rows_returned: int = 0):
        query_preview = query[:80] + "..." if len(query) > 80 else query
        self._logger.info(f"\033[33m[SQL QUERY]\033[0m | query={query_preview} | rows={rows_returned}")
    
    def chat_response(self, session_id: str, queries_executed: int):
        self._logger.info(
            f"\033[32m[CHAT RESPONSE]\033[0m | session={session_id} | "
            f"queries_executed={queries_executed}"
        )
    
    def csv_processing(self, session_id: str, filename: str, columns: List[str], row_count: int):
        cols_str = ", ".join(columns[:5])
        if len(columns) > 5:
            cols_str += f"... (+{len(columns) - 5} more)"
        self._logger.info(
            f"\033[35m[CSV]\033[0m | session={session_id} | "
            f"file={filename} | rows={row_count} | columns=[{cols_str}]"
        )


logger = Logger()
