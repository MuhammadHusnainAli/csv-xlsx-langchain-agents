import json
from langchain_core.tools import tool
from langchain_community.utilities.sql_database import SQLDatabase
from app.utils.logger import logger
from app.config import settings
from app.core.llm import get_llm
from app.utils.sql_helpers import (
    extract_columns_from_query,
    parse_result_to_structured,
    truncate_result_for_llm,
    get_row_count
)
from app.utils.sql_validation import hardcoded_validation
from app.agents.prompt.sql_validation_prompt import SQL_VALIDATION_PROMPT

executed_queries = []


def create_sql_tools(db: SQLDatabase) -> list:
    
    @tool
    def get_schema(table_names: str = "") -> str:
        """Get the database schema including table names, columns, and data types. Optionally pass comma-separated table names to get specific tables only."""
        if table_names:
            tables = [t.strip() for t in table_names.split(",")]
            logger.debug(f"Getting schema for tables: {tables}")
            return db.get_table_info(table_names=tables)
        logger.debug("Getting schema for all tables")
        return db.get_table_info()
    
    @tool
    def validate_query(query: str) -> str:
        """Validate a SQL query for security and syntax before execution. Returns JSON with validation result, errors, and recommendations."""
        logger.info(f"[SQL VALIDATION] Validating query: {query[:50]}...")
        
        is_valid_hardcoded, hardcoded_message, hardcoded_errors = hardcoded_validation(query)
        
        if not is_valid_hardcoded:
            logger.warning(f"[SQL VALIDATION] Hardcoded validation FAILED: {hardcoded_message}")
            result = {
                "is_valid": False,
                "is_safe": False,
                "validation_result": {
                    "syntax_valid": False,
                    "security_valid": False,
                    "best_practices_valid": False
                },
                "errors": hardcoded_errors,
                "warnings": [],
                "natural_language_summary": f"REJECTED by security filter: {hardcoded_message}",
                "recommendation": "REJECT",
                "modified_query": None
            }
            return json.dumps(result)
        
        try:
            llm = get_llm()
            prompt = SQL_VALIDATION_PROMPT.format(query=query)
            
            logger.debug("[SQL VALIDATION] Invoking LLM for detailed validation")
            response = llm.invoke(prompt)
            response_text = response.content if hasattr(response, 'content') else str(response)
            
            try:
                start_idx = response_text.find('{')
                end_idx = response_text.rfind('}') + 1
                if start_idx != -1 and end_idx > start_idx:
                    json_str = response_text[start_idx:end_idx]
                    validation_result = json.loads(json_str)
                else:
                    raise ValueError("No JSON found in LLM response")
            except json.JSONDecodeError as e:
                logger.warning(f"[SQL VALIDATION] Failed to parse LLM response: {e}")
                validation_result = {
                    "is_valid": is_valid_hardcoded,
                    "is_safe": is_valid_hardcoded,
                    "validation_result": {
                        "syntax_valid": True,
                        "security_valid": is_valid_hardcoded,
                        "best_practices_valid": True
                    },
                    "errors": [],
                    "warnings": [],
                    "natural_language_summary": "Query passed basic validation. LLM detailed analysis unavailable.",
                    "recommendation": "EXECUTE" if is_valid_hardcoded else "REJECT",
                    "modified_query": None
                }
            
            recommendation = validation_result.get("recommendation", "EXECUTE")
            logger.info(f"[SQL VALIDATION] Result: {recommendation} - {validation_result.get('natural_language_summary', '')[:100]}...")
            
            return json.dumps(validation_result)
            
        except Exception as e:
            logger.error(f"[SQL VALIDATION] LLM validation error: {str(e)}")
            result = {
                "is_valid": is_valid_hardcoded,
                "is_safe": is_valid_hardcoded,
                "validation_result": {
                    "syntax_valid": True,
                    "security_valid": is_valid_hardcoded,
                    "best_practices_valid": True
                },
                "errors": [],
                "warnings": [{"code": "LLM_UNAVAILABLE", "message": "LLM validation unavailable, using hardcoded rules only"}],
                "natural_language_summary": f"Query passed hardcoded security validation. {hardcoded_message}",
                "recommendation": "EXECUTE" if is_valid_hardcoded else "REJECT",
                "modified_query": None
            }
            return json.dumps(result)
    
    @tool
    def run_query(query: str) -> str:
        """Execute a SQL SELECT query on the database after validation. Returns query results as formatted text."""
        validation_result_str = validate_query.invoke(query)
        validation_result = json.loads(validation_result_str)
        
        if validation_result.get("recommendation") == "REJECT":
            error_msg = validation_result.get("natural_language_summary", "Query rejected by validation")
            logger.warning(f"[SQL QUERY] Query rejected: {error_msg}")
            return f"QUERY REJECTED: {error_msg}"
        
        if validation_result.get("recommendation") == "MODIFY" and validation_result.get("modified_query"):
            query = validation_result["modified_query"]
            logger.info(f"[SQL QUERY] Using modified query: {query[:50]}...")
        
        result = db.run(query)
        row_count = get_row_count(result)
        logger.sql_query(query, row_count)
        columns = extract_columns_from_query(query, db)
        structured_result = parse_result_to_structured(result, columns)
        executed_queries.append({"query": query, "result": structured_result})
        llm_result = truncate_result_for_llm(result)
        return llm_result
    
    @tool
    def explore_data(table_name: str, limit: int = 5) -> str:
        """Explore sample data from a specific table. Returns first N rows to understand the data structure and content."""
        if limit > settings.MAX_QUERY_LIMIT:
            limit = settings.MAX_QUERY_LIMIT
        query = f"SELECT * FROM {table_name} LIMIT {limit}"
        
        validation_result_str = validate_query.invoke(query)
        validation_result = json.loads(validation_result_str)
        
        if validation_result.get("recommendation") == "REJECT":
            error_msg = validation_result.get("natural_language_summary", "Query rejected by validation")
            logger.warning(f"[SQL QUERY] Explore query rejected: {error_msg}")
            return f"QUERY REJECTED: {error_msg}"
        
        result = db.run(query)
        row_count = get_row_count(result)
        logger.sql_query(query, row_count)
        columns = extract_columns_from_query(query, db)
        structured_result = parse_result_to_structured(result, columns)
        executed_queries.append({"query": query, "result": structured_result})
        llm_result = truncate_result_for_llm(result)
        return llm_result
    
    return [get_schema, validate_query, run_query, explore_data]


def get_executed_queries():
    return executed_queries


def clear_executed_queries():
    global executed_queries
    executed_queries = []
