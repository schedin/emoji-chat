import { MessageRequest, EmojiResponse, SampleResponse, ApiError } from '../types';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// Debug: Log the API URL being used
console.log('API_BASE_URL:', API_BASE_URL);

class ApiService {
  private async fetchWithErrorHandling<T>(
    url: string,
    options?: RequestInit
  ): Promise<T> {
    try {
      const response = await fetch(url, {
        ...options,
        headers: {
          'Content-Type': 'application/json',
          ...options?.headers,
        },
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new ApiError(
          errorData.detail || errorData.error || `HTTP ${response.status}`,
          response.status
        );
      }

      return await response.json();
    } catch (error) {
      if (error instanceof ApiError) {
        throw error;
      }

      // Network or other errors
      throw new ApiError(
        error instanceof Error ? error.message : 'Network error occurred'
      );
    }
  }

  async generateEmojis(message: string, disableModeration: boolean = false): Promise<EmojiResponse> {
    const request: MessageRequest = {
      message,
      disable_moderation: disableModeration
    };

    return this.fetchWithErrorHandling<EmojiResponse>(
      `${API_BASE_URL}/api/emojis`,
      {
        method: 'POST',
        body: JSON.stringify(request),
      }
    );
  }

  async getSampleSentence(): Promise<SampleResponse> {
    return this.fetchWithErrorHandling<SampleResponse>(
      `${API_BASE_URL}/api/sample`
    );
  }

  async healthCheck(): Promise<boolean> {
    try {
      await this.fetchWithErrorHandling(`${API_BASE_URL}/health`);
      return true;
    } catch {
      return false;
    }
  }
}

// Create and export a singleton instance
export const apiService = new ApiService();

// Export the ApiError class for use in components
export { ApiError };
