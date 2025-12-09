import json
from typing import List, Tuple, Optional, Dict, Any
from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_community.utilities.sql_database import SQLDatabase
from app.core.llm import get_llm
from app.agents.agent.sql_agent import invoke_sql_agent
from app.agents.agent.chart_agent import run_chart_agent
from app.agents.prompt.main_prompt import MAIN_SYSTEM_PROMPT
from app.api.schema.chat import ChatMessage, QueryResult, QueryResultData, ChartConfig
from app.utils.logger import logger

_main_agent_result = {
    "sql_queries": [],
    "chart_config": None
}


def create_main_agent_tools(db: SQLDatabase) -> list:
    
    @tool
    def call_sql_agent(query: str) -> str:
        """Call the SQL agent to query and analyze data from the database. Pass the user's data-related question or request."""
        global _main_agent_result
        logger.info(f"[MAIN AGENT] Calling SQL Agent with: {query[:50]}...")
        
        result = invoke_sql_agent(db, query)
        
        for q in result["queries"]:
            _main_agent_result["sql_queries"].append({
                "query": q["query"],
                "columns": q["columns"],
                "rows": q["rows"]
            })
        
        response = result["response"]
        if result["queries"]:
            last_query = result["queries"][-1]
            cols_preview = last_query['columns'][:10] if last_query['columns'] else []
            response += f"\n\nData available: {len(last_query['rows'])} rows with columns: {', '.join(cols_preview)}..."
        
        return response
    
    @tool
    def call_chart_agent(columns: str, data: str, intent: str = "") -> str:
        """Generate a Plotly.js chart visualization from query results. Pass column names as comma-separated string, data as JSON array of rows, and optional user intent."""
        global _main_agent_result
        logger.info(f"[MAIN AGENT] Calling Chart Agent for Plotly visualization")
        logger.debug(f"[MAIN AGENT] Chart input - columns: {columns[:100]}...")
        
        try:
            cols = [c.strip() for c in columns.split(",") if c.strip()]
            
            if not cols:
                logger.warning("[MAIN AGENT] No columns provided to chart agent")
                return "Error: No columns provided for chart generation"
            
            try:
                rows = json.loads(data) if data and data.strip() else []
            except json.JSONDecodeError as e:
                logger.warning(f"[MAIN AGENT] Failed to parse data JSON: {e}")
                rows = []
            
            logger.info(f"[MAIN AGENT] Parsed {len(cols)} columns and {len(rows)} rows for chart")
            
            chart_config = run_chart_agent(cols, rows, intent)
            
            if chart_config:
                _main_agent_result["chart_config"] = chart_config
                reasoning = chart_config.get("reasoning", "")
                chart_type = chart_config.get("chart_type", "unknown")
                logger.info(f"[MAIN AGENT] Chart config stored: {chart_type}")
                return f"Plotly chart generated: {chart_type} chart. Title: {chart_config.get('title', 'Chart')}. Reasoning: {reasoning}. The plotly_config is ready for rendering with Plotly.newPlot()."
            
            logger.warning("[MAIN AGENT] Chart agent returned None")
            return "Unable to generate chart recommendation for this data."
            
        except Exception as e:
            logger.error(f"[MAIN AGENT] Chart agent error: {str(e)}")
            import traceback
            logger.error(f"[MAIN AGENT] Traceback: {traceback.format_exc()}")
            return f"Error generating chart: {str(e)}"
    
    return [call_sql_agent, call_chart_agent]


def create_main_agent(db: SQLDatabase):
    llm = get_llm()
    tools = create_main_agent_tools(db)
    
    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt=MAIN_SYSTEM_PROMPT,
    )
    return agent


def clear_main_agent_result():
    global _main_agent_result
    _main_agent_result = {
        "sql_queries": [],
        "chart_config": None
    }


def get_main_agent_result():
    global _main_agent_result
    return _main_agent_result


def is_data_chartable(columns: List[str], rows: List[List[Any]]) -> bool:
    if not columns or len(columns) < 2:
        return False
    
    if not rows or len(rows) < 1:
        return False
    
    if len(rows) > 1000:
        return False
    
    has_numerical = False
    has_categorical_or_date = False
    
    if rows and len(rows) > 0:
        first_row = rows[0]
        for idx, col in enumerate(columns):
            if idx < len(first_row):
                val = first_row[idx]
                col_lower = col.lower()
                
                if isinstance(val, (int, float)) and not isinstance(val, bool):
                    has_numerical = True
                elif any(d in col_lower for d in ["date", "time", "year", "month", "day", "category", "name", "type", "status"]):
                    has_categorical_or_date = True
                elif isinstance(val, str):
                    has_categorical_or_date = True
    
    return has_numerical or (has_categorical_or_date and len(rows) <= 50)


async def run_main_agent(
    db: SQLDatabase, 
    message: str, 
    history: List[ChatMessage] = None
) -> Tuple[str, List[QueryResult], Optional[ChartConfig]]:
    global _main_agent_result
    clear_main_agent_result()
    
    agent = create_main_agent(db)
    
    messages = []
    if history:
        for msg in history:
            messages.append({"role": msg.role, "content": msg.content})
    
    messages.append({"role": "user", "content": message})
    
    logger.info(f"[MAIN AGENT] Processing request: {message[:50]}...")
    
    result = agent.invoke({"messages": messages})
    
    response_messages = result.get("messages", [])
    response_text = "Unable to process your request."
    if response_messages:
        last_message = response_messages[-1]
        if hasattr(last_message, "content"):
            response_text = last_message.content
    
    agent_result = get_main_agent_result()
    
    logger.debug(f"[MAIN AGENT] Final result - SQL queries: {len(agent_result['sql_queries'])}, Chart config: {agent_result['chart_config'] is not None}")
    
    if agent_result["chart_config"] is None and agent_result["sql_queries"]:
        last_query = agent_result["sql_queries"][-1]
        columns = last_query.get("columns", [])
        rows = last_query.get("rows", [])
        
        if is_data_chartable(columns, rows):
            logger.info(f"[MAIN AGENT] Data is chartable ({len(columns)} columns, {len(rows)} rows), auto-generating chart...")
            chart_config = run_chart_agent(columns, rows, message)
            if chart_config:
                agent_result["chart_config"] = chart_config
                logger.info(f"[MAIN AGENT] Auto-generated chart: {chart_config.get('chart_type', 'unknown')}")
        else:
            logger.info(f"[MAIN AGENT] Data not suitable for charting (columns: {len(columns)}, rows: {len(rows)})")
    
    sql_queries = [
        QueryResult(
            query=q["query"],
            result=QueryResultData(
                columns=q["columns"],
                rows=q["rows"]
            )
        )
        for q in agent_result["sql_queries"]
    ]
    
    chart_config = None
    if agent_result["chart_config"]:
        config = agent_result["chart_config"]
        logger.info(f"[MAIN AGENT] Building ChartConfig from: {config.get('chart_type', 'unknown')}")
        chart_config = ChartConfig(
            chart_type=config.get("chart_type", "bar"),
            x_axis=config.get("x_axis", ""),
            y_axis=config.get("y_axis", ""),
            title=config.get("title", "Data Visualization"),
            data_columns=config.get("data_columns", []),
            reasoning=config.get("reasoning"),
            plotly_config=config.get("plotly_config")
        )
    else:
        logger.warning("[MAIN AGENT] No chart_config in agent result")
    
    logger.info(f"[MAIN AGENT] Completed - SQL queries: {len(sql_queries)}, Chart: {'Yes' if chart_config else 'No'}")
    
    return response_text, sql_queries, chart_config
