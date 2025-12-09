import re
from typing import Tuple, List, Dict, Any

FORBIDDEN_KEYWORDS = [
    "INSERT", "UPDATE", "DELETE", "DROP", "ALTER", "CREATE", "TRUNCATE",
    "GRANT", "REVOKE", "DENY", "BEGIN", "COMMIT", "ROLLBACK", "SAVEPOINT",
    "VACUUM", "REINDEX", "ATTACH", "DETACH", "PRAGMA"
]

FORBIDDEN_PATTERNS = [
    r";\s*(INSERT|UPDATE|DELETE|DROP|ALTER|CREATE|TRUNCATE)",
    r"--\s*$",
    r"/\*.*\*/",
    r";\s*--",
    r"UNION\s+ALL\s+SELECT.*FROM\s+sqlite_master",
    r"LOAD_EXTENSION",
    r"writefile\s*\(",
]


def hardcoded_validation(query: str) -> Tuple[bool, str, List[Dict[str, Any]]]:
    query_upper = query.upper().strip()
    errors = []
    
    if not query_upper.startswith(("SELECT", "WITH", "EXPLAIN")):
        errors.append({
            "code": "INVALID_QUERY_START",
            "message": f"Query must start with SELECT, WITH, or EXPLAIN. Found: {query_upper[:20]}...",
            "severity": "CRITICAL"
        })
        return False, "Query does not start with an allowed keyword", errors
    
    for keyword in FORBIDDEN_KEYWORDS:
        pattern = r'\b' + keyword + r'\b'
        if re.search(pattern, query_upper):
            if keyword == "CREATE" and "CREATE" not in query_upper.split("(")[0]:
                continue
            errors.append({
                "code": f"FORBIDDEN_{keyword}",
                "message": f"{keyword} operations are not allowed. This is a read-only database.",
                "severity": "CRITICAL"
            })
    
    for pattern in FORBIDDEN_PATTERNS:
        if re.search(pattern, query_upper, re.IGNORECASE | re.DOTALL):
            errors.append({
                "code": "INJECTION_PATTERN",
                "message": f"Potentially dangerous pattern detected in query",
                "severity": "CRITICAL"
            })
    
    semicolon_count = query.count(";")
    if semicolon_count > 1 or (semicolon_count == 1 and not query.strip().endswith(";")):
        errors.append({
            "code": "MULTIPLE_STATEMENTS",
            "message": "Multiple SQL statements detected. Only single statements are allowed.",
            "severity": "CRITICAL"
        })
    
    open_parens = query.count("(")
    close_parens = query.count(")")
    if open_parens != close_parens:
        errors.append({
            "code": "UNBALANCED_PARENTHESES",
            "message": f"Unbalanced parentheses: {open_parens} opening, {close_parens} closing",
            "severity": "ERROR"
        })
    
    single_quotes = query.count("'")
    if single_quotes % 2 != 0:
        errors.append({
            "code": "UNBALANCED_QUOTES",
            "message": "Unbalanced single quotes in query",
            "severity": "ERROR"
        })
    
    is_valid = len(errors) == 0
    message = "Query passed hardcoded validation" if is_valid else f"Found {len(errors)} validation errors"
    
    return is_valid, message, errors

