import ast
import re
from typing import Any, List, Dict
from sqlalchemy import inspect
from langchain_community.utilities.sql_database import SQLDatabase
from app.config import settings


def extract_columns_from_query(query: str, db: SQLDatabase) -> List[str]:
    query_upper = query.upper().strip()
    
    if "SELECT *" in query_upper or "SELECT * " in query_upper:
        table_match = re.search(r'FROM\s+(\w+)', query, re.IGNORECASE)
        if table_match:
            table_name = table_match.group(1)
            try:
                inspector = inspect(db._engine)
                columns_info = inspector.get_columns(table_name)
                return [col["name"] for col in columns_info]
            except:
                pass
    else:
        select_match = re.search(r'SELECT\s+(.+?)\s+FROM', query, re.IGNORECASE | re.DOTALL)
        if select_match:
            columns_str = select_match.group(1)
            columns = []
            for col in columns_str.split(','):
                col = col.strip()
                if ' AS ' in col.upper():
                    alias_match = re.search(r'\s+AS\s+(\w+)', col, re.IGNORECASE)
                    if alias_match:
                        columns.append(alias_match.group(1))
                    else:
                        columns.append(col.split()[-1].split('.')[-1])
                else:
                    columns.append(col.split()[-1].split('.')[-1])
            return columns
    
    return []


def parse_result_to_structured(result: str, columns: List[str]) -> Dict[str, Any]:
    if not result:
        return {"columns": columns, "rows": [], "total_rows": 0}
    try:
        parsed = ast.literal_eval(result)
        if isinstance(parsed, list):
            rows = []
            for row in parsed:
                if isinstance(row, (list, tuple)):
                    rows.append(list(row))
                else:
                    rows.append([row])
            return {"columns": columns, "rows": rows, "total_rows": len(rows)}
        return {"columns": columns, "rows": [[parsed]], "total_rows": 1}
    except:
        return {"columns": columns, "rows": [[result]], "total_rows": 1}


def truncate_result_for_llm(result: str) -> str:
    if not result:
        return result
    try:
        parsed = ast.literal_eval(result)
        if isinstance(parsed, list) and len(parsed) > settings.LLM_DISPLAY_LIMIT:
            truncated = parsed[:settings.LLM_DISPLAY_LIMIT]
            return str(truncated) + f"\n... (showing {settings.LLM_DISPLAY_LIMIT} of {len(parsed)} rows)"
        return result
    except:
        return result


def get_row_count(result: str) -> int:
    if not result:
        return 0
    try:
        parsed = ast.literal_eval(result)
        if isinstance(parsed, list):
            return len(parsed)
        return 1
    except:
        return 0

