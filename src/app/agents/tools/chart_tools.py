import json
from typing import List, Dict, Any
from langchain_core.tools import tool
from app.utils.logger import logger
from app.utils.chart_helpers import (
    generate_chart_config,
    validate_plotly_config,
    fallback_plotly_config
)

_chart_recommendations = {"data": []}


def _store_chart_recommendation(config: Dict[str, Any]):
    global _chart_recommendations
    _chart_recommendations["data"].append(config)
    logger.debug(f"[CHART STORE] Stored recommendation, total: {len(_chart_recommendations['data'])}")


def get_chart_recommendations() -> List[Dict[str, Any]]:
    global _chart_recommendations
    return _chart_recommendations["data"]


def clear_chart_recommendations():
    global _chart_recommendations
    _chart_recommendations = {"data": []}
    logger.debug("[CHART STORE] Cleared recommendations")


def create_chart_tools() -> list:
    
    @tool
    def validate_plotly_schema(plotly_config: str) -> str:
        try:
            config = json.loads(plotly_config) if isinstance(plotly_config, str) else plotly_config
            result = validate_plotly_config(config)
            logger.debug(f"[CHART VALIDATION] Valid: {result['valid']}, Errors: {len(result['errors'])}, Warnings: {len(result['warnings'])}")
            return json.dumps(result)
        except json.JSONDecodeError as e:
            return json.dumps({"valid": False, "errors": [f"Invalid JSON: {str(e)}"], "warnings": []})
        except Exception as e:
            return json.dumps({"valid": False, "errors": [str(e)], "warnings": []})
    
    @tool
    def recommend_chart(columns: str, sample_data: str, user_intent: str = "") -> str:
        try:
            cols = [c.strip() for c in columns.split(",")]
            data = json.loads(sample_data) if sample_data else []
            
            config = generate_chart_config(cols, data, user_intent)
            _store_chart_recommendation(config)
            
            logger.info(f"[CHART TOOL] Recommendation stored: {config['chart_type']}")
            return json.dumps(config)
            
        except Exception as e:
            logger.error(f"[CHART TOOL] Error: {str(e)}")
            cols_list = []
            try:
                cols_list = [c.strip() for c in columns.split(",")]
            except:
                pass
            config = fallback_plotly_config(cols_list, [], user_intent)
            _store_chart_recommendation(config)
            return json.dumps(config)
    
    return [validate_plotly_schema, recommend_chart]
