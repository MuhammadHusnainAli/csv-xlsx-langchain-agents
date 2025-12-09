import os
from fastapi import APIRouter, HTTPException
from app.api.schema.chat import ChatRequest, ChatResponse
from app.services.database import DatabaseService
from app.agents import run_main_agent
from app.utils.logger import logger

router = APIRouter(tags=["chat"])


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    logger.chat_request(request.session_id, request.message)
    
    db_path = DatabaseService.get_database_path(request.session_id)
    if not os.path.exists(db_path):
        logger.error(f"Database not found | session={request.session_id}")
        raise HTTPException(status_code=404, detail="No database found for this session. Please upload a file first.")
    
    db = DatabaseService.get_sql_database(request.session_id)
    response, sql_queries, chart_config = await run_main_agent(db, request.message, request.history)
    
    logger.chat_response(request.session_id, len(sql_queries))
    
    return ChatResponse(response=response, sql_queries=sql_queries, chart_config=chart_config)
