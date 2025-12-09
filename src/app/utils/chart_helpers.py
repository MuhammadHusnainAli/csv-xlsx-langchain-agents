import json
from typing import List, Dict, Any
from app.utils.logger import logger
from app.core.llm import get_llm

PLOTLY_SCHEMA_PROMPT = """You are a Plotly.js data visualization expert. Analyze the provided data and generate a complete Plotly.js chart configuration.

DATA INFORMATION:
Columns: {columns}
Sample Data (first 10 rows): {sample_data}
User Intent: {user_intent}

AVAILABLE PLOTLY CHART TYPES (use the exact type name):
- scatter: Scatter plots, line charts (use mode: 'lines', 'markers', or 'lines+markers')
- bar: Vertical bar charts
- pie: Pie charts (uses labels and values instead of x/y)
- histogram: Histogram for distribution
- box: Box plots for statistical distribution
- violin: Violin plots for distribution
- heatmap: Heatmap for matrix data
- contour: Contour plots
- scatter3d: 3D scatter plots
- surface: 3D surface plots
- scatterpolar: Polar scatter/line charts
- barpolar: Polar bar charts
- scattergeo: Geographic scatter plots
- choropleth: Geographic choropleth maps
- scattermapbox: Mapbox scatter plots
- treemap: Treemap hierarchical visualization
- sunburst: Sunburst hierarchical visualization
- funnel: Funnel charts
- funnelarea: Funnel area charts
- waterfall: Waterfall charts
- indicator: KPI indicators and gauges
- candlestick: Financial candlestick charts
- ohlc: Financial OHLC charts
- table: Data tables
- sankey: Sankey diagrams for flow
- parcoords: Parallel coordinates
- parcats: Parallel categories
- carpet: Carpet plots
- scattercarpet: Scatter on carpet
- icicle: Icicle charts

ANALYSIS STEPS:
1. Analyze column types (numerical, categorical, date/time, geographic)
2. Understand the user's visualization intent
3. Choose the most appropriate Plotly chart type
4. Generate complete Plotly.js trace and layout configuration

RESPOND WITH ONLY A VALID JSON OBJECT IN THIS EXACT FORMAT:
{{
    "reasoning": "Detailed explanation of why this chart type and configuration was chosen",
    "chart_type": "plotly_trace_type",
    "plotly_config": {{
        "data": [
            {{
                "type": "chart_type",
                "x": "column_name_or_array",
                "y": "column_name_or_array",
                "mode": "lines|markers|lines+markers (for scatter)",
                "name": "trace_name",
                "marker": {{"color": "color_value"}},
                "text": "column_for_hover_text (optional)"
            }}
        ],
        "layout": {{
            "title": {{"text": "Chart Title"}},
            "xaxis": {{"title": {{"text": "X Axis Label"}}}},
            "yaxis": {{"title": {{"text": "Y Axis Label"}}}},
            "showlegend": true,
            "template": "plotly_white"
        }}
    }},
    "x_axis": "column_name_for_x",
    "y_axis": "column_name_for_y",
    "title": "Chart Title",
    "data_columns": ["columns", "used", "in", "chart"]
}}

For PIE charts use this data format:
{{
    "data": [{{
        "type": "pie",
        "labels": "column_for_labels",
        "values": "column_for_values",
        "hole": 0.3
    }}]
}}

For HISTOGRAM use:
{{
    "data": [{{
        "type": "histogram",
        "x": "column_name"
    }}]
}}

IMPORTANT: The plotly_config must be valid Plotly.js configuration that can be directly used with Plotly.newPlot()
"""

PLOTLY_VALID_TYPES = [
    "scatter", "bar", "pie", "histogram", "box", "violin", "heatmap", "contour",
    "scatter3d", "surface", "scatterpolar", "barpolar", "scattergeo", "choropleth",
    "scattermapbox", "treemap", "sunburst", "funnel", "funnelarea", "waterfall",
    "indicator", "candlestick", "ohlc", "table", "sankey", "parcoords", "parcats",
    "carpet", "scattercarpet", "icicle"
]


def generate_basic_plotly_config(chart_type: str, x_axis: str, y_axis: str, title: str) -> Dict[str, Any]:
    if chart_type == "pie":
        return {
            "data": [{
                "type": "pie",
                "labels": x_axis,
                "values": y_axis,
                "hole": 0.3
            }],
            "layout": {
                "title": {"text": title},
                "showlegend": True,
                "template": "plotly_white"
            }
        }
    elif chart_type == "histogram":
        return {
            "data": [{
                "type": "histogram",
                "x": x_axis
            }],
            "layout": {
                "title": {"text": title},
                "xaxis": {"title": {"text": x_axis}},
                "yaxis": {"title": {"text": "Count"}},
                "template": "plotly_white"
            }
        }
    elif chart_type == "scatter":
        return {
            "data": [{
                "type": "scatter",
                "x": x_axis,
                "y": y_axis,
                "mode": "markers"
            }],
            "layout": {
                "title": {"text": title},
                "xaxis": {"title": {"text": x_axis}},
                "yaxis": {"title": {"text": y_axis}},
                "template": "plotly_white"
            }
        }
    elif chart_type == "line":
        return {
            "data": [{
                "type": "scatter",
                "x": x_axis,
                "y": y_axis,
                "mode": "lines+markers"
            }],
            "layout": {
                "title": {"text": title},
                "xaxis": {"title": {"text": x_axis}},
                "yaxis": {"title": {"text": y_axis}},
                "template": "plotly_white"
            }
        }
    else:
        return {
            "data": [{
                "type": "bar",
                "x": x_axis,
                "y": y_axis
            }],
            "layout": {
                "title": {"text": title},
                "xaxis": {"title": {"text": x_axis}},
                "yaxis": {"title": {"text": y_axis}},
                "template": "plotly_white"
            }
        }


def fallback_plotly_config(cols: List[str], data: List, user_intent: str = "") -> Dict[str, Any]:
    numerical_cols = []
    categorical_cols = []
    date_cols = []
    
    if data and len(data) > 0:
        first_row = data[0] if isinstance(data[0], list) else data
        for idx, col in enumerate(cols):
            if idx < len(first_row):
                val = first_row[idx]
                col_lower = col.lower()
                
                if any(d in col_lower for d in ["date", "time", "year", "month", "day"]):
                    date_cols.append(col)
                elif isinstance(val, (int, float)) and not isinstance(val, bool):
                    numerical_cols.append(col)
                else:
                    categorical_cols.append(col)
    
    chart_type = "bar"
    x_axis = cols[0] if cols else ""
    y_axis = numerical_cols[0] if numerical_cols else (cols[1] if len(cols) > 1 else "")
    
    if date_cols and numerical_cols:
        chart_type = "line"
        x_axis = date_cols[0]
        y_axis = numerical_cols[0]
    elif categorical_cols and numerical_cols:
        chart_type = "bar"
        x_axis = categorical_cols[0]
        y_axis = numerical_cols[0]
    elif len(numerical_cols) >= 2:
        chart_type = "scatter"
        x_axis = numerical_cols[0]
        y_axis = numerical_cols[1]
    
    title = f"{y_axis} by {x_axis}" if x_axis and y_axis else "Data Visualization"
    
    return {
        "reasoning": "Fallback recommendation based on data structure analysis",
        "chart_type": chart_type,
        "plotly_config": generate_basic_plotly_config(chart_type, x_axis, y_axis, title),
        "x_axis": x_axis,
        "y_axis": y_axis,
        "title": title,
        "data_columns": cols
    }


def generate_chart_config(columns: List[str], sample_data: List, user_intent: str = "") -> Dict[str, Any]:
    try:
        cols = columns
        data = sample_data
        
        sample_rows = data[:10] if len(data) > 10 else data
        
        prompt = PLOTLY_SCHEMA_PROMPT.format(
            columns=", ".join(cols),
            sample_data=json.dumps(sample_rows, indent=2),
            user_intent=user_intent if user_intent else "General data visualization"
        )
        
        llm = get_llm()
        logger.info(f"[CHART GENERATOR] Invoking LLM for Plotly chart recommendation")
        
        response = llm.invoke(prompt)
        response_text = response.content if hasattr(response, 'content') else str(response)
        
        logger.debug(f"[CHART GENERATOR] LLM Response: {response_text[:300]}...")
        
        try:
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            if start_idx != -1 and end_idx > start_idx:
                json_str = response_text[start_idx:end_idx]
                config = json.loads(json_str)
            else:
                raise ValueError("No JSON found in response")
        except json.JSONDecodeError:
            logger.warning("[CHART GENERATOR] Failed to parse LLM response, using fallback")
            config = fallback_plotly_config(cols, data, user_intent)
        
        if "plotly_config" not in config:
            config["plotly_config"] = generate_basic_plotly_config(
                config.get("chart_type", "bar"),
                config.get("x_axis", cols[0] if cols else ""),
                config.get("y_axis", cols[1] if len(cols) > 1 else ""),
                config.get("title", "Data Visualization")
            )
        
        required_fields = ["chart_type", "x_axis", "y_axis", "title", "data_columns", "plotly_config"]
        for field in required_fields:
            if field not in config:
                if field == "chart_type":
                    config[field] = "bar"
                elif field == "x_axis":
                    config[field] = cols[0] if cols else ""
                elif field == "y_axis":
                    config[field] = cols[1] if len(cols) > 1 else ""
                elif field == "title":
                    config[field] = "Data Visualization"
                elif field == "data_columns":
                    config[field] = cols
        
        logger.info(f"[CHART GENERATOR] Generated: {config['chart_type']} - {config.get('reasoning', '')[:50]}...")
        return config
        
    except Exception as e:
        logger.error(f"[CHART GENERATOR] Error: {str(e)}")
        config = fallback_plotly_config(columns, sample_data, user_intent)
        return config


def validate_plotly_config(config: Dict[str, Any]) -> Dict[str, Any]:
    errors = []
    warnings = []
    
    if "data" not in config:
        errors.append("Missing 'data' array in configuration")
    elif not isinstance(config["data"], list):
        errors.append("'data' must be an array of traces")
    elif len(config["data"]) == 0:
        errors.append("'data' array is empty")
    else:
        for idx, trace in enumerate(config["data"]):
            if "type" not in trace:
                errors.append(f"Trace {idx}: Missing 'type' field")
            elif trace["type"] not in PLOTLY_VALID_TYPES:
                warnings.append(f"Trace {idx}: Unknown type '{trace['type']}', may not render correctly")
            
            trace_type = trace.get("type", "")
            if trace_type == "pie":
                if "labels" not in trace and "values" not in trace:
                    errors.append(f"Trace {idx}: Pie chart requires 'labels' and 'values'")
            elif trace_type in ["scatter", "bar", "line"]:
                if "x" not in trace and "y" not in trace:
                    warnings.append(f"Trace {idx}: Missing 'x' or 'y' data")
    
    if "layout" not in config:
        warnings.append("Missing 'layout' object, default layout will be used")
    
    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings,
        "trace_count": len(config.get("data", []))
    }

