from typing import List, Tuple, Dict, Any
from langchain.agents import create_agent
from langchain_community.utilities.sql_database import SQLDatabase
from app.core.llm import get_llm
from app.agents.tools.sql_tools import create_sql_tools, get_executed_queries, clear_executed_queries
from app.agents.prompt.sql_prompt import SYSTEM_PROMPT
from app.api.schema.chat import ChatMessage, QueryResult, QueryResultData

_sql_agent_instance = None
_current_db = None


def create_sql_agent(db: SQLDatabase):
    llm = get_llm()
    tools = create_sql_tools(db)
    
    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt=SYSTEM_PROMPT,
    )
    return agent


def get_sql_agent(db: SQLDatabase):
    global _sql_agent_instance, _current_db
    if _sql_agent_instance is None or _current_db != db:
        _sql_agent_instance = create_sql_agent(db)
        _current_db = db
    return _sql_agent_instance


def invoke_sql_agent(db: SQLDatabase, query: str) -> Dict[str, Any]:
    clear_executed_queries()
    
    agent = create_sql_agent(db)
    
    result = agent.invoke({"messages": [{"role": "user", "content": query}]})
    
    response_messages = result.get("messages", [])
    response_text = "Unable to process your request."
    if response_messages:
        last_message = response_messages[-1]
        if hasattr(last_message, "content"):
            response_text = last_message.content
    
    executed = get_executed_queries()
    queries_data = []
    for q in executed:
        queries_data.append({
            "query": q["query"],
            "columns": q["result"]["columns"],
            "rows": q["result"]["rows"]
        })
    
    return {
        "response": response_text,
        "queries": queries_data
    }


async def run_sql_agent(db: SQLDatabase, message: str, history: List[ChatMessage] = None) -> Tuple[str, List[QueryResult]]:
    clear_executed_queries()
    
    agent = create_sql_agent(db)
    
    messages = []
    if history:
        for msg in history:
            messages.append({"role": msg.role, "content": msg.content})
    
    messages.append({"role": "user", "content": message})
    
    result = agent.invoke({"messages": messages})
    
    response_messages = result.get("messages", [])
    response_text = "Unable to process your request."
    if response_messages:
        last_message = response_messages[-1]
        if hasattr(last_message, "content"):
            response_text = last_message.content
    
    sql_queries = [
        QueryResult(
            query=q["query"], 
            result=QueryResultData(
                columns=q["result"]["columns"],
                rows=q["result"]["rows"]
            )
        ) 
        for q in get_executed_queries()
    ]
    
    return response_text, sql_queries
