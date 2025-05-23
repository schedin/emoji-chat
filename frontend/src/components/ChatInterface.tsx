'use client';

import { useState, useRef, useEffect } from 'react';
import { useChat } from '../hooks/useChat';
import MessageBubble from './MessageBubble';
import SuggestionButton from './SuggestionButton';

export default function ChatInterface() {
  const [inputValue, setInputValue] = useState('');
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  const {
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
  } = useChat();

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Focus input on mount
  useEffect(() => {
    inputRef.current?.focus();
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputValue.trim() || isLoading) return;

    const message = inputValue;
    setInputValue('');
    await sendMessage(message);

    // Refocus the input field after sending
    setTimeout(() => {
      inputRef.current?.focus();
    }, 100);
  };

  const handleSuggestionClickWrapper = async (suggestion: string, index: number) => {
    setInputValue('');
    await handleSuggestionClick(suggestion, index);

    // Refocus the input field after clicking suggestion
    setTimeout(() => {
      inputRef.current?.focus();
    }, 0);
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e as any);
    }
  };

  return (
    <div className="chat-container">
      {/* Header */}
      <div className="chat-header">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-xl font-semibold text-gray-900">Emoji Chat</h1>
            <p className="text-sm text-gray-600">Express yourself with AI-generated emoji reactions</p>
          </div>
          <div className="text-2xl">💬</div>
        </div>
      </div>

      {/* Messages */}
      <div className="chat-messages">
        {messages.length === 0 && (
          <div className="text-center text-gray-500 mt-8">
            <div className="text-4xl mb-4">👋</div>
            <p className="text-lg mb-2">Welcome to Emoji Chat!</p>
            <p className="text-sm">Send a message or try one of the suggestions below.</p>
          </div>
        )}

        {messages.map((message) => (
          <MessageBubble key={message.id} message={message} />
        ))}

        {isLoading && (
          <div className="flex justify-start">
            <div className="message-bubble message-bot">
              <div className="flex items-center space-x-2">
                <div className="loading-spinner border-gray-400"></div>
                <span className="text-sm text-gray-600">Generating emojis...</span>
              </div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className="chat-input-area space-y-4">
        {/* Error Display */}
        {error && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-3 flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <span className="text-red-500">⚠️</span>
              <span className="text-sm text-red-700">{error}</span>
            </div>
            <button
              onClick={clearError}
              className="text-red-500 hover:text-red-700 text-sm"
            >
              ✕
            </button>
          </div>
        )}

        {/* Suggestions */}
        <div className="flex flex-wrap gap-2">
          {suggestions.map((suggestion, index) => (
            <SuggestionButton
              key={`${suggestion}-${index}`}
              suggestion={suggestion}
              onClick={(suggestion) => handleSuggestionClickWrapper(suggestion, index)}
              isLoading={loadingSuggestionIndex === index || isLoading}
            />
          ))}
        </div>

        {/* Input Form with Moderation */}
        <div className="space-y-2">
          <form onSubmit={handleSubmit} className="flex space-x-2">
            <input
              ref={inputRef}
              type="text"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Type your message here..."
              className="input-field"
              disabled={isLoading}
              maxLength={1000}
            />
            <button
              type="submit"
              disabled={!inputValue.trim() || isLoading}
              className="send-button"
            >
              {isLoading ? (
                <div className="loading-spinner"></div>
              ) : (
                'Send'
              )}
            </button>
          </form>

          {/* Moderation checkbox moved to footer */}
          <div className="flex justify-end">
            <label className="flex items-center space-x-2 text-xs text-gray-600 cursor-pointer">
              <input
                type="checkbox"
                checked={moderationEnabled}
                onChange={(e) => setModerationEnabled(e.target.checked)}
                className="rounded border-gray-300 text-primary-500 focus:ring-primary-500 w-3 h-3"
              />
              <span>Moderation</span>
            </label>
          </div>
        </div>
      </div>
    </div>
  );
}
