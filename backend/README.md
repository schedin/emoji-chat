# Emoji Chat Backend

A FastAPI-based backend server that generates emojis based on user messages using an LLM.



## Run locally

### Setup virtual environment

#### Linux/MacOS
```bash
python -m venv .venv
source .venv/bin/activate
```

#### Windows
```cmd
python -m venv .venv
.venv\Scripts\activate.bat
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Download LLM model
```bash
ollama pull gemma3:1b-it-qat
```


### Start the server

```bash
python src/main.py
```

## Environment variables for backend Python server

| Variable | Default | Description |
|----------|---------|-------------|
| `LLM_URL` | `http://llm-server:11434` | URL of the Ollama server |
| `LLM_MODEL` | `gemma3:1b-it-qat` | Ollama model to use for emoji generation |
| `LLM_TEMPERATURE` | `0.7` | Temperature for LLM responses (0.0-1.0) |
| `LLM_MAX_TOKENS` | `100` | Maximum tokens for LLM responses |
| `ENABLE_CONTENT_MODERATION` | `true` | Enable/disable content moderation |
| `MODERATION_MODEL` | _(empty)_ | Model for content moderation (uses main model if empty) |
| `MAX_MESSAGE_LENGTH` | `1000` | Maximum message length |
| `MIN_MESSAGE_LENGTH` | `1` | Minimum message length |
| `HOST` | `0.0.0.0` | Server host |
| `PORT` | `8000` | Server port |
| `API_TIMEOUT` | `30` | LLM API timeout in seconds |
| `DEVELOPMENT_MODE` | `false` | Enable development mode with auto-reload |
