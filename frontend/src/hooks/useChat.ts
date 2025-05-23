'use client';

import { useState, useCallback, useEffect } from 'react';
import { ChatMessage, ApiError } from '../types';
import { apiService } from '../services/api';

export function useChat() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [suggestions, setSuggestions] = useState<string[]>([]);
  const [loadingSuggestionIndex, setLoadingSuggestionIndex] = useState<number | null>(null);

  // Generate initial suggestions on mount
  useEffect(() => {
    const loadInitialSuggestions = async () => {
      try {
        const suggestionPromises = Array(3).fill(null).map(() =>
          apiService.getSampleSentence()
        );
        const responses = await Promise.all(suggestionPromises);
        setSuggestions(responses.map(response => response.sample));
      } catch (error) {
        console.error('Failed to load initial suggestions:', error);
        // Fallback suggestions
        setSuggestions([
          "I'm feeling excited about today!",
          "What a beautiful morning this is.",
          "I'm grateful for all the good things in my life."
        ]);
      }
    };

    loadInitialSuggestions();
  }, []);

  const sendMessage = useCallback(async (messageText: string) => {
    if (!messageText.trim() || isLoading) return;

    setError(null);
    setIsLoading(true);

    // Add user message immediately
    const userMessage: ChatMessage = {
      id: Date.now().toString(),
      type: 'user',
      content: messageText.trim(),
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);

    try {
      // Call the API to generate emojis
      const response = await apiService.generateEmojis(messageText.trim());

      // Add bot response with only emojis (no redundant message text)
      const botMessage: ChatMessage = {
        id: (Date.now() + 1).toString(),
        type: 'bot',
        content: '', // Empty content since we only want to show emojis
        emojis: response.emojis,
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      setError(error instanceof ApiError ? error.message : 'Failed to send message');

      // Add error message as bot response
      const errorMessage: ChatMessage = {
        id: (Date.now() + 1).toString(),
        type: 'bot',
        content: 'Sorry, I encountered an error processing your message.',
        emojis: ['😔', '🔧'],
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  }, [isLoading]);

  const replaceSuggestion = useCallback(async (index: number) => {
    if (loadingSuggestionIndex !== null) return;

    setLoadingSuggestionIndex(index);

    try {
      const response = await apiService.getSampleSentence();
      setSuggestions(prev => {
        const newSuggestions = [...prev];
        newSuggestions[index] = response.sample;
        return newSuggestions;
      });
    } catch (error) {
      console.error('Failed to replace suggestion:', error);
      // Keep the existing suggestion on error
    } finally {
      setLoadingSuggestionIndex(null);
    }
  }, [loadingSuggestionIndex]);

  const handleSuggestionClick = useCallback(async (suggestion: string, index: number) => {
    // Send the message
    await sendMessage(suggestion);

    // Replace only the clicked suggestion
    await replaceSuggestion(index);
  }, [sendMessage, replaceSuggestion]);

  const clearError = useCallback(() => {
    setError(null);
  }, []);

  return {
    messages,
    isLoading,
    error,
    suggestions,
    loadingSuggestionIndex,
    sendMessage,
    handleSuggestionClick,
    clearError,
  };
}
