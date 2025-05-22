# Emoji Chat Backend

A FastAPI-based backend server that generates emojis based on user messages using an LLM.

## Features

- **Message Validation**: Validates message size and content
- **Content Moderation**: Optional content filtering and jailbreak detection
- **Emoji Generation**: Uses LLM to generate appropriate emojis for messages
- **ASGI Support**: Built with FastAPI and Uvicorn for high performance
- **Environment Configuration**: Configurable via environment variables

## API Endpoints

### POST /api/emojis
Generate emojis for a message.

**Request Body:**
```json
{
  "message": "I'm so happy today!"
}
```

**Response:**
```json
{
  "emojis": ["😊", "😄", "🎉"],
  "message": "I'm so happy today!",
  "moderation_passed": true
}
```

### GET /health
Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "llm_url": "http://llm-server:8000",
  "content_moderation_enabled": true
}
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

## Running the Server

### Development
```bash
cd backend/src
python main.py
```

### Production
```bash
cd backend/src
python start.py
```

### With Docker
The server is designed to work with the existing Docker setup in `backend/images/api/`.

## Dependencies

- FastAPI: Web framework
- Uvicorn: ASGI server
- Ollama: Python client for Ollama LLM server
- httpx: HTTP client for additional requests
- Pydantic: Data validation
- python-dotenv: Environment variable management

## Model Configuration

The backend uses Ollama to communicate with LLM models. You can configure:

- **Model Selection**: Set `LLM_MODEL` to any model available in your Ollama instance
- **Separate Moderation Model**: Optionally use a different model for content moderation via `MODERATION_MODEL`
- **Model Parameters**: Configure temperature and max tokens for fine-tuning responses

### Supported Models

Any model supported by Ollama can be used, including:
- `gemma3:1b-it-qat` (default, lightweight, quantized)
- `gemma2:2b` (lightweight)
- `llama3.1:8b` (more capable)
- `mistral:7b` (good balance)
- `qwen2.5:7b` (multilingual support)

Make sure the model is pulled in your Ollama instance before using it.
