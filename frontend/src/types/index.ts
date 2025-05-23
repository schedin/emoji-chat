// API Types matching backend models
export interface MessageRequest {
  message: string;
}

export interface EmojiResponse {
  emojis: string[];
  message: string;
  moderation_passed?: boolean;
}

export interface SampleResponse {
  sample: string;
}

export interface ErrorResponse {
  error: string;
  detail?: string;
}

export interface HealthResponse {
  status: string;
  llm_url: string;
  llm_model: string;
  content_moderation_enabled: boolean;
  moderation_model?: string;
}

// Frontend-specific types
export interface ChatMessage {
  id: string;
  type: 'user' | 'bot';
  content: string;
  emojis?: string[];
  timestamp: Date;
}

export class ApiError extends Error {
  status?: number;

  constructor(message: string, status?: number) {
    super(message);
    this.name = 'ApiError';
    this.status = status;
  }
}
