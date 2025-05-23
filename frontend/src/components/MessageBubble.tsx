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
            {message.emojis && message.emojis.length > 0 ? (
              <div className="emoji-display">
                {message.emojis.map((emoji, index) => (
                  <span
                    key={index}
                    className="inline-block cursor-help hover:scale-110 transition-transform duration-200"
                    title={`Emoji: ${emoji}`}
                  >
                    {emoji}
                  </span>
                ))}
              </div>
            ) : (
              <p className="text-sm text-gray-600">
                {message.content}
              </p>
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
