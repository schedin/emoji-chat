import { find } from 'node-emoji';

/**
 * Get the name of an emoji character
 * @param emoji - The emoji character (e.g., '🔧')
 * @returns The emoji name (e.g., 'wrench') or the emoji itself if not found
 */
export function getEmojiName(emoji: string): string {
  try {
    const emojiData = find(emoji);
    if (emojiData && emojiData.key) {
      // Convert snake_case to readable format
      return emojiData.key
        .replace(/_/g, ' ')
        .replace(/\b\w/g, l => l.toUpperCase());
    }
    
    // Fallback: return the emoji itself if name not found
    return emoji;
  } catch (error) {
    // If anything goes wrong, just return the emoji
    return emoji;
  }
}
