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
  const [moderationEnabled, setModerationEnabled] = useState<boolean>(true);

  // Generate initial suggestions on mount
  useEffect(() => {
    const loadInitialSuggestions = async () => {
      try {
        console.log('Loading initial suggestions...');
        const suggestionPromises = Array(3).fill(null).map(() =>
          apiService.getSampleSentence()
        );
        const responses = await Promise.all(suggestionPromises);
        const newSuggestions = responses.map(response => response.sample);
        console.log('Loaded suggestions:', newSuggestions);
        setSuggestions(newSuggestions);
      } catch (error) {
        console.error('Failed to load initial suggestions:', error);
        // Clear any existing error state and use fallback suggestions
        setError(null);
        setSuggestions([
          "I'm feeling excited about today!",
          "What a beautiful morning this is.",
          "I'm grateful for all the good things in my life."
        ]);
        console.log('Using fallback suggestions');
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
      console.log('Sending message to API:', messageText.trim());
      const response = await apiService.generateEmojis(messageText.trim(), !moderationEnabled);
      console.log('Received response:', response);

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
      console.error('Failed to send message:', error);

      let errorMessage = 'Failed to send message';
      if (error instanceof ApiError) {
        errorMessage = error.message;
      } else if (error instanceof Error) {
        if (error.message.includes('fetch') || error.message.includes('NetworkError')) {
          errorMessage = 'Unable to connect to server. Please check your connection.';
        } else {
          errorMessage = error.message;
        }
      }

      setError(errorMessage);

      // Add error message as bot response
      const errorBotMessage: ChatMessage = {
        id: (Date.now() + 1).toString(),
        type: 'bot',
        content: 'Sorry, I encountered an error processing your message.',
        emojis: ['😔', '🔧'],
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, errorBotMessage]);
    } finally {
      setIsLoading(false);
    }
  }, [isLoading, moderationEnabled]);

  const replaceSuggestion = useCallback(async (index: number) => {
    if (loadingSuggestionIndex !== null) return;

    setLoadingSuggestionIndex(index);

    try {
      console.log('Replacing suggestion at index:', index);
      const response = await apiService.getSampleSentence();
      console.log('New suggestion received:', response.sample);
      setSuggestions(prev => {
        const newSuggestions = [...prev];
        newSuggestions[index] = response.sample;
        return newSuggestions;
      });
    } catch (error) {
      console.error('Failed to replace suggestion:', error);
      // Keep the existing suggestion on error
      // Don't show error to user for suggestion replacement failures
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
    moderationEnabled,
    setModerationEnabled,
    sendMessage,
    handleSuggestionClick,
    clearError,
  };
}
