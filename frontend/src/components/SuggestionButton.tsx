'use client';

interface SuggestionButtonProps {
  suggestion: string;
  onClick: (suggestion: string) => void;
  isLoading?: boolean;
}

export default function SuggestionButton({ 
  suggestion, 
  onClick, 
  isLoading = false 
}: SuggestionButtonProps) {
  return (
    <button
      className="suggestion-button"
      onClick={() => onClick(suggestion)}
      disabled={isLoading}
    >
      {suggestion}
    </button>
  );
}
