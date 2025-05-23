# Emoji Chat Frontend

A React/Next.js web application that provides a chat interface for emoji-based responses powered by an AI backend.

## Features

- **Chat Interface**: Clean, responsive chat interface with message bubbles
- **Emoji Responses**: AI-generated emoji responses to user messages
- **Smart Suggestions**: 3 clickable sentence suggestions that refresh individually
- **Content Moderation Control**: User-controllable content moderation toggle
- **Emoji Tooltips**: Hover over emojis to see their names (e.g., "Wrench", "Heart")
- **Real-time Updates**: Instant message sending and response display
- **Error Handling**: Graceful error handling with user-friendly messages
- **Responsive Design**: Works seamlessly on mobile and desktop devices

## Technology Stack

- **Framework**: Next.js 14 with App Router
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **State Management**: React Hooks (useState, useEffect, custom hooks)
- **API Integration**: Fetch API with custom service layer

## Getting Started

### Prerequisites

- Node.js 18+
- npm, yarn, or pnpm

### Installation

1. Install dependencies:
```bash
npm install
# or
yarn install
# or
pnpm install
```

2. Set up environment variables:
```bash
cp .env.local.example .env.local
```

Edit `.env.local` and set:
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Development

Run the development server:

```bash
npm run dev
# or
yarn dev
# or
pnpm dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

### Building for Production

Build the application:

```bash
npm run build
# or
yarn build
# or
pnpm build
```

This creates an optimized production build in the `out` directory, ready for static hosting.

### Docker Deployment

The application is configured for static export and can be served using the provided nginx configuration:

```bash
# Build the static export
npm run build

# The output will be in the 'out' directory
# This is copied to nginx in the Docker container
```

## API Integration

The frontend integrates with the backend API endpoints:

- `POST /api/emojis` - Generate emojis for user messages
- `GET /api/sample` - Get sample inspirational sentences
- `GET /health` - Health check endpoint

## Project Structure

```
src/
├── app/                 # Next.js App Router pages
│   ├── layout.tsx      # Root layout
│   ├── page.tsx        # Home page
│   └── globals.css     # Global styles
├── components/         # React components
│   ├── ChatInterface.tsx
│   ├── MessageBubble.tsx
│   └── SuggestionButton.tsx
├── hooks/              # Custom React hooks
│   └── useChat.ts
├── services/           # API service layer
│   └── api.ts
└── types/              # TypeScript type definitions
    └── index.ts
```

## Configuration

### Environment Variables

- `NEXT_PUBLIC_API_URL`: Backend API URL (default: http://localhost:8000)

### Next.js Configuration

The app is configured for static export in `next.config.js` to work with nginx deployment.

## Contributing

1. Follow the existing code style and patterns
2. Use TypeScript for all new code
3. Add proper error handling for API calls
4. Test on both mobile and desktop viewports
5. Follow React best practices (hooks, functional components)
