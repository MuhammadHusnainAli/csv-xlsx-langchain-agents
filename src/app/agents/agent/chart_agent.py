from typing import List, Dict, Any, Optional
from app.agents.tools.chart_tools import get_chart_recommendations, clear_chart_recommendations
from app.utils.chart_helpers import generate_chart_config
from app.utils.logger import logger


def run_chart_agent(columns: List[str], rows: List[List[Any]], user_intent: str = "") -> Optional[Dict[str, Any]]:
    clear_chart_recommendations()
    
    logger.info(f"[CHART AGENT] Processing with {len(columns)} columns and {len(rows)} rows")
    logger.debug(f"[CHART AGENT] Columns: {columns[:5]}...")
    
    if not columns or len(columns) < 1:
        logger.warning("[CHART AGENT] No columns provided")
        return None
    
    sample_rows = rows[:10] if len(rows) > 10 else rows
    
    try:
        config = generate_chart_config(columns, sample_rows, user_intent)
        
        if config:
            logger.info(f"[CHART AGENT] Generated {config.get('chart_type', 'unknown')} chart config")
            return config
        
        recommendations = get_chart_recommendations()
        if recommendations:
            config = recommendations[-1]
            logger.info(f"[CHART AGENT] Retrieved stored config: {config.get('chart_type', 'unknown')}")
            return config
        
    except Exception as e:
        logger.error(f"[CHART AGENT] Error: {str(e)}")
    
    logger.warning("[CHART AGENT] No chart recommendation generated")
    return None
