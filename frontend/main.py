import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go

API_BASE_URL = "http://localhost:8000"

st.set_page_config(
    page_title="Data Analysis Agent",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .stApp {
        background: #0a0a0a;
    }
    .main-header {
        font-family: 'SF Mono', 'Fira Code', monospace;
        font-size: 1.5rem;
        font-weight: 600;
        color: #ffffff;
        padding: 0.5rem 0;
        border-bottom: 1px solid #262626;
        margin-bottom: 1rem;
    }
    .section-title {
        font-size: 0.8rem;
        font-weight: 600;
        color: #a3a3a3;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.75rem;
        margin-top: 1rem;
    }
    .chat-message {
        padding: 0.75rem 1rem;
        border-radius: 6px;
        margin: 0.5rem 0;
        font-size: 0.9rem;
    }
    .user-message {
        background: #1a1a1a;
        border-left: 2px solid #3b82f6;
        color: #e5e5e5;
    }
    .assistant-message {
        background: #0f0f0f;
        border-left: 2px solid #10b981;
        color: #d4d4d4;
    }
    .sql-query-box {
        background: #0a0a0a;
        border: 1px solid #262626;
        border-radius: 4px;
        padding: 0.75rem;
        font-family: 'SF Mono', 'Fira Code', monospace;
        font-size: 0.8rem;
        color: #4ade80;
        overflow-x: auto;
    }
    div[data-testid="stFileUploader"] {
        background: transparent;
    }
    div[data-testid="stFileUploader"] > div {
        padding: 0.5rem;
    }
    div[data-testid="stFileUploader"] label {
        display: none;
    }
    div[data-testid="stFileUploader"] section {
        padding: 0.75rem;
        border: 1px dashed #404040;
        border-radius: 8px;
        background: #0f0f0f;
    }
    .stButton > button {
        background: #ffffff;
        color: #0a0a0a;
        border: none;
        border-radius: 4px;
        padding: 0.4rem 1rem;
        font-weight: 500;
        font-size: 0.8rem;
        width: 100%;
    }
    .stButton > button:hover {
        background: #e5e5e5;
        color: #0a0a0a;
    }
    .stTextInput > div > div > input {
        background: #0f0f0f;
        border: 1px solid #262626;
        color: #ffffff;
        border-radius: 4px;
        font-size: 0.9rem;
    }
    .stTextInput > div > div > input:focus {
        border-color: #3b82f6;
        box-shadow: none;
    }
    .status-dot {
        display: inline-block;
        width: 8px;
        height: 8px;
        border-radius: 50%;
        margin-right: 8px;
    }
    .status-active {
        background: #10b981;
        box-shadow: 0 0 6px #10b981;
    }
    .status-inactive {
        background: #525252;
    }
    .session-id {
        font-family: 'SF Mono', monospace;
        font-size: 0.7rem;
        color: #525252;
        word-break: break-all;
        margin-top: 0.25rem;
    }
    [data-testid="stSidebar"] {
        background: #0a0a0a;
        border-right: 1px solid #1a1a1a;
        min-width: 320px;
    }
    [data-testid="stSidebar"] > div {
        padding: 1rem 1.5rem;
    }
    .stDataFrame {
        background: #0a0a0a;
    }
    .table-card {
        background: #111111;
        border: 1px solid #262626;
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 0.75rem;
    }
    .table-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.75rem;
    }
    .table-name {
        font-family: 'SF Mono', monospace;
        font-size: 0.95rem;
        font-weight: 600;
        color: #ffffff;
    }
    .table-rows {
        font-size: 0.75rem;
        color: #737373;
        background: #1a1a1a;
        padding: 0.2rem 0.5rem;
        border-radius: 4px;
    }
    .columns-title {
        font-size: 0.7rem;
        color: #525252;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.5rem;
    }
    .column-tag {
        display: inline-block;
        background: #1a1a1a;
        border: 1px solid #262626;
        border-radius: 4px;
        padding: 0.2rem 0.5rem;
        margin: 0.15rem;
        font-family: 'SF Mono', monospace;
        font-size: 0.75rem;
        color: #a3a3a3;
    }
    .columns-container {
        max-height: 200px;
        overflow-y: auto;
        padding-right: 0.5rem;
    }
    .columns-container::-webkit-scrollbar {
        width: 4px;
    }
    .columns-container::-webkit-scrollbar-track {
        background: #0a0a0a;
    }
    .columns-container::-webkit-scrollbar-thumb {
        background: #262626;
        border-radius: 2px;
    }
    div[data-testid="stExpander"] {
        background: #0f0f0f;
        border: 1px solid #1a1a1a;
        border-radius: 6px;
    }
    div[data-testid="stExpander"] details {
        border: none;
    }
    div[data-testid="stExpander"] summary {
        font-size: 0.85rem;
        color: #a3a3a3;
    }
</style>
""", unsafe_allow_html=True)

if "session_id" not in st.session_state:
    st.session_state.session_id = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "tables" not in st.session_state:
    st.session_state.tables = []

with st.sidebar:
    st.markdown('<div class="section-title">Upload File</div>', unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "file",
        type=["csv", "xlsx"],
        label_visibility="collapsed"
    )
    
    if uploaded_file is not None:
        if st.button("Process File"):
            with st.spinner("Processing..."):
                try:
                    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                    response = requests.post(f"{API_BASE_URL}/files", files=files)
                    
                    if response.status_code == 200:
                        data = response.json()
                        st.session_state.session_id = data["session_id"]
                        st.session_state.tables = data["tables"]
                        st.session_state.chat_history = []
                        st.rerun()
                    else:
                        st.error(response.text)
                except Exception as e:
                    st.error(str(e))
    
    st.markdown('<div class="section-title">Session</div>', unsafe_allow_html=True)
    if st.session_state.session_id:
        st.markdown(f'<span class="status-dot status-active"></span><span style="color:#e5e5e5;font-size:0.85rem;">Active</span>', unsafe_allow_html=True)
        st.markdown(f'<div class="session-id">{st.session_state.session_id}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<span class="status-dot status-inactive"></span><span style="color:#525252;font-size:0.85rem;">No active session</span>', unsafe_allow_html=True)
    
    if st.session_state.tables:
        st.markdown('<div class="section-title">Database Schema</div>', unsafe_allow_html=True)
        
        for table in st.session_state.tables:
            column_tags = "".join([f'<span class="column-tag">{col}</span>' for col in table["columns"]])
            
            table_html = f'''
            <div class="table-card">
                <div class="table-header">
                    <span class="table-name">{table["table_name"]}</span>
                    <span class="table-rows">{table["row_count"]} rows</span>
                </div>
                <div class="columns-title">Columns ({len(table["columns"])})</div>
                <div class="columns-container">
                    {column_tags}
                </div>
            </div>
            '''
            st.markdown(table_html, unsafe_allow_html=True)

st.markdown('<div class="main-header">Data Analysis</div>', unsafe_allow_html=True)

chat_container = st.container()

with chat_container:
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(f'<div class="chat-message user-message">{msg["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-message assistant-message">{msg["content"]}</div>', unsafe_allow_html=True)
            
            if "sql_queries" in msg and msg["sql_queries"]:
                with st.expander("SQL Queries"):
                    for q in msg["sql_queries"]:
                        st.markdown(f'<div class="sql-query-box">{q["query"]}</div>', unsafe_allow_html=True)
                        if q.get("result") and q["result"].get("rows"):
                            df = pd.DataFrame(q["result"]["rows"], columns=q["result"]["columns"])
                            st.dataframe(df, use_container_width=True, height=200)
            
            if "chart_config" in msg and msg["chart_config"]:
                chart = msg["chart_config"]
                if chart.get("plotly_config"):
                    try:
                        fig = go.Figure(chart["plotly_config"])
                        fig.update_layout(
                            paper_bgcolor="#0a0a0a",
                            plot_bgcolor="#0f0f0f",
                            font_color="#d4d4d4",
                            margin=dict(l=40, r=40, t=40, b=40)
                        )
                        st.plotly_chart(fig, use_container_width=True)
                    except Exception:
                        pass

if st.session_state.session_id:
    col1, col2 = st.columns([6, 1])
    with col1:
        user_input = st.text_input(
            "query",
            placeholder="Ask about your data...",
            label_visibility="collapsed"
        )
    with col2:
        send_clicked = st.button("Send")
    
    if send_clicked and user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        
        with st.spinner(""):
            try:
                history_for_api = [
                    {"role": h["role"], "content": h["content"]} 
                    for h in st.session_state.chat_history[:-1]
                ]
                
                payload = {
                    "session_id": st.session_state.session_id,
                    "message": user_input,
                    "history": history_for_api
                }
                
                response = requests.post(f"{API_BASE_URL}/chat", json=payload)
                
                if response.status_code == 200:
                    data = response.json()
                    assistant_msg = {
                        "role": "assistant",
                        "content": data["response"],
                        "sql_queries": data.get("sql_queries", []),
                        "chart_config": data.get("chart_config")
                    }
                    st.session_state.chat_history.append(assistant_msg)
                    st.rerun()
                else:
                    st.error(response.text)
            except Exception as e:
                st.error(str(e))
else:
    st.markdown('<p style="color:#525252;font-size:0.9rem;text-align:center;margin-top:2rem;">Upload a file to start</p>', unsafe_allow_html=True)

if st.session_state.chat_history:
    st.markdown("---")
    if st.button("Clear Chat", use_container_width=False):
        st.session_state.chat_history = []
        st.rerun()
