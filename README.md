# Emoji Chat

Emoji Chat is an interactive web application that uses AI to generate emoji reactions based on user input. Users enter a sentence on the web interface, and the application responds with relevant emojis that capture the sentiment and context of the message.

## Overview

The application consists of three main components:
- **Frontend**: A responsive React/Next.js web interface
- **Backend API**: A Python FastAPI service/AI agent that processes requests and communicates with the LLM
- **LLM Service**: A lightweight LLM (Large Language Model) running locally for text processing

### How It Works

1. **User Input**: Users type a message in the web interface and submit it
2. **Content Moderation**: The Python backend sends the message to the LLM for content moderation
   - The LLM evaluates if the content is appropriate
   - Users can optionally disable moderation via a checkbox
3. **Emoji Generation**: If moderation passes (or is disabled), the backend sends another request to the LLM
   - The LLM analyzes the message sentiment and context
   - The LLM returns 3-5 relevant emojis
4. **Response Display**: The frontend displays the emojis as a response in the chat interface

https://github.com/user-attachments/assets/1516805b-a23d-48d2-bc6e-34588bd7e507

## Technical Architecture

- **Frontend**: Next.js 14 with TypeScript and Tailwind CSS
- **Backend**: Python FastAPI service with async request handling
- **LLM**: Gemma3 1B-IT-QAT model running on Ollama
- **Communication**: RESTful API endpoints between frontend and backend
- **Deployment**: Containerized with Kubernetes orchestration

## Deployment

Use Helm to deploy the application to a Kubernetes cluster. For example:

```bash
helm upgrade --install emoji-chat ./charts/emoji-chat \
    --namespace emoji-chat --create-namespace
```
