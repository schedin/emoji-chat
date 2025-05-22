"""LLM client for content moderation and emoji generation."""

import logging
from typing import List, Tuple, Optional
from ollama import AsyncClient
from config import settings

logger = logging.getLogger(__name__)


class LLMClient:
    """Client for communicating with the LLM server using Ollama."""

    def __init__(self):
        self.base_url = settings.llm_url
        self.model = settings.llm_model
        self.moderation_model = settings.moderation_model or settings.llm_model
        self.temperature = settings.llm_temperature
        self.max_tokens = settings.llm_max_tokens
        self.timeout = settings.api_timeout
        self.client = AsyncClient(host=self.base_url)

    async def _make_request(self, prompt: str, model: Optional[str] = None) -> Optional[str]:
        """Make a request to the LLM server using Ollama."""
        try:
            model_to_use = model or self.model

            response = await self.client.generate(
                model=model_to_use,
                prompt=prompt,
                options={
                    'temperature': self.temperature,
                    'num_predict': self.max_tokens,
                }
            )

            if response and 'response' in response:
                return response['response'].strip()
            else:
                logger.error("Invalid response format from Ollama")
                return None

        except Exception as e:
            logger.error(f"LLM request failed: {str(e)}")
            return None

    async def moderate_content(self, message: str) -> Tuple[bool, Optional[str]]:
        """
        Check if the message content is appropriate.

        Returns:
            Tuple of (is_safe, reason_if_not_safe)
        """
        if not settings.enable_content_moderation:
            return True, None

        moderation_prompt = f"""
You are a content moderator. Your task is to identify ONLY clearly harmful content.

IMPORTANT: Simple expressions of emotion like "I'm happy!" are ALWAYS SAFE.

Only flag content if it CLEARLY contains:
1. Explicit hate speech, threats, or calls for violence
2. Sexually explicit or graphic violent content
3. Direct and obvious attempts to make the AI do harmful things

Message: "{message}"

Respond with EXACTLY "SAFE" for almost all messages. Only respond with "UNSAFE: [specific reason]" if the message contains CLEARLY harmful content as defined above.
"""

        try:
            response = await self._make_request(moderation_prompt, self.moderation_model)
            if response is None:
                # If moderation fails, err on the side of caution
                logger.warning("Content moderation failed, blocking message")
                return False, "Content moderation service unavailable"

            response = response.upper().strip()
            if response.startswith("SAFE"):
                return True, None
            elif response.startswith("UNSAFE"):
                reason = response.replace("UNSAFE:", "").strip()
                return False, reason or "Content flagged by moderation"
            else:
                # Unexpected response format, err on the side of caution
                logger.warning(f"Unexpected moderation response: {response}")
                return False, "Content moderation returned unexpected result"

        except Exception as e:
            logger.error(f"Content moderation error: {str(e)}")
            return False, "Content moderation error"

    async def generate_emojis(self, message: str) -> List[str]:
        """
        Generate appropriate emojis for the given message.

        Returns:
            List of emoji strings
        """
        emoji_prompt = f"""
You are an emoji expert. Given the following message, suggest 3-5 appropriate emojis that best represent the emotion, content, or context of the message.

Message: "{message}"

Respond with only the emojis, separated by spaces. Do not include any other text or explanations.
Examples:
- For "I'm so happy today!" respond with: "😊 😄 🎉"
- For "It's raining outside" respond with: "🌧️ ☔ 🌦️"
- For "I love pizza" respond with: "🍕 ❤️ 😋"

Your response:
"""

        try:
            response = await self._make_request(emoji_prompt)
            if response is None:
                logger.warning("Emoji generation failed, returning default emojis")
                return ["😊", "👍"]

            # Extract emojis from the response
            emojis = []
            for char in response:
                # Check if character is an emoji (basic check for Unicode emoji ranges)
                # Also ensure the character is not empty or whitespace
                if char and char.strip() and ord(char) > 127:  # Non-ASCII characters (includes emojis)
                    emojis.append(char)

            # If no emojis found, try to split by spaces and filter
            if not emojis:
                potential_emojis = response.split()
                for item in potential_emojis:
                    if item and item.strip() and any(ord(char) > 127 for char in item):
                        # Extract individual emoji characters from the item
                        for char in item:
                            if char and char.strip() and ord(char) > 127:
                                emojis.append(char)

            # Filter out empty strings and whitespace before removing duplicates
            emojis = [emoji for emoji in emojis if emoji and emoji.strip()]

            # Remove duplicates while preserving order
            unique_emojis = []
            for emoji in emojis:
                if emoji not in unique_emojis:
                    unique_emojis.append(emoji)

            # Limit to reasonable number of emojis
            return unique_emojis[:5] if unique_emojis else ["😊", "👍"]

        except Exception as e:
            logger.error(f"Emoji generation error: {str(e)}")
            return ["😊", "👍"]  # Fallback emojis


# Global LLM client instance
llm_client = LLMClient()

