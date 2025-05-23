'use client';

import { ChatMessage } from '../types';

interface MessageBubbleProps {
  message: ChatMessage;
}

export default function MessageBubble({ message }: MessageBubbleProps) {
  const isUser = message.type === 'user';

  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} animate-slide-up`}>
      <div className={`message-bubble ${isUser ? 'message-user' : 'message-bot'}`}>
        {isUser ? (
          <p className="text-sm sm:text-base">{message.content}</p>
        ) : (
          <div className="space-y-2">
            <p className="text-sm text-gray-600">
              &ldquo;{message.content}&rdquo;
            </p>
            {message.emojis && message.emojis.length > 0 && (
              <div className="emoji-display">
                {message.emojis.map((emoji, index) => (
                  <span key={index} className="inline-block">
                    {emoji}
                  </span>
                ))}
              </div>
            )}
          </div>
        )}
        <div className="text-xs opacity-70 mt-1">
          {message.timestamp.toLocaleTimeString([], {
            hour: '2-digit',
            minute: '2-digit'
          })}
        </div>
      </div>
    </div>
  );
}
