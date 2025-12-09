from pydantic import BaseModel
from typing import List, Literal, Any, Optional, Dict


class ChatMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str


class ChatRequest(BaseModel):
    session_id: str
    message: str
    history: List[ChatMessage] = []


class QueryResultData(BaseModel):
    columns: List[str]
    rows: List[List[Any]]


class QueryResult(BaseModel):
    query: str
    result: QueryResultData


class ChartConfig(BaseModel):
    chart_type: str
    x_axis: str
    y_axis: str
    title: str
    data_columns: List[str]
    reasoning: Optional[str] = None
    plotly_config: Optional[Dict[str, Any]] = None


class ChatResponse(BaseModel):
    response: str
    sql_queries: List[QueryResult] = []
    chart_config: Optional[ChartConfig] = None
