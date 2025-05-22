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

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `LLM_URL` | `http://llm-server:8000` | URL of the LLM server |
| `ENABLE_CONTENT_MODERATION` | `true` | Enable/disable content moderation |
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
- httpx: HTTP client for LLM communication
- Pydantic: Data validation
- python-dotenv: Environment variable management
