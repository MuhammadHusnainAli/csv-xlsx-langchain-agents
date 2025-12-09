# CSV/XLSX LangChain Agents

AI-powered data analysis API. Upload CSV/XLSX files, query data using natural language, and get automatic chart visualizations.

## Screenshots

![Upload Interface](https://github.com/user-attachments/assets/2bb95f47-07dd-4b13-899a-4d37751fa679)

![Chat Interface](https://github.com/user-attachments/assets/6f348f77-fb08-4ad9-b294-1f038923bce8)

## Architecture

```
┌────────────────────────────────────────────────────────────────┐
│                        Main Agent                              │
│                      (Orchestrator)                            │
├────────────────────────────────────────────────────────────────┤
│                             │                                  │
│              ┌──────────────┴──────────────┐                   │
│              ▼                             ▼                   │
│      ┌──────────────┐             ┌──────────────┐             │
│      │  SQL Agent   │             │ Chart Agent  │             │
│      └──────────────┘             └──────────────┘             │
│              │                             │                   │
│      ┌───────┴───────┐             ┌───────┴───────┐           │
│      │    Tools      │             │    Tools      │           │
│      ├───────────────┤             ├───────────────┤           │
│      │ - get_schema  │             │ - recommend   │           │
│      │ - validate    │             │ - validate    │           │
│      │ - run_query   │             └───────────────┘           │
│      │ - explore     │                                         │
│      └───────────────┘                                         │
└────────────────────────────────────────────────────────────────┘
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/files` | Upload CSV/XLSX file |
| POST | `/chat` | Query data with natural language |
| GET | `/` | Health check |

## Environment Variables

Create `.env` file:

```env
AZURE_OPENAI_API_KEY=your_key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_CHAT_API_VERSION=2024-02-15-preview
AZURE_OPENAI_CHAT_DEPLOYMENT_NAME_4O=gpt-4o
```

## Run with Uvicorn

```bash
# Install dependencies
pip install uv
uv sync

# Run server
cd src
uvicorn app.main:app --reload --port 8000
```

## Run with Docker

```bash
# Build
docker build -t csv-xlsx-agent .

# Run
docker run -p 8000:8000  csv-xlsx-agent
```

## Usage

**1. Upload file:**
```bash
curl -X POST http://localhost:8000/files \
  -F "file=@data.csv"
```

Response:
```json
{
  "session_id": "uuid",
  "tables": [{"table_name": "data", "columns": [...], "row_count": 100}]
}
```

**2. Query data:**
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "uuid",
    "message": "Show top 10 sales by category"
  }'
```

Response:
```json
{
  "response": "markdown table with results",
  "sql_queries": [{"query": "SELECT...", "result": {...}}],
  "chart_config": {"chart_type": "bar", "plotly_config": {...}}
}
```

## Project Structure

```
src/app/
├── main.py              # FastAPI app
├── config.py            # Settings
├── api/
│   ├── routers/         # Endpoints
│   └── schema/          # Pydantic models
├── agents/
│   ├── agent/           # Agent implementations
│   ├── prompt/          # System prompts
│   └── tools/           # Agent tools
├── services/            # Database service
├── core/                # LLM initialization
└── utils/               # Helpers & logging
```

## Features

- Upload CSV/XLSX files
- Auto-convert to SQLite database
- Natural language SQL queries
- SQL injection protection
- Auto chart generation (Plotly.js)
- Query validation
- Markdown table responses
