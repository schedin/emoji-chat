"""LLM client for content moderation and emoji generation."""

import logging
from typing import List, Tuple, Optional
from ollama import AsyncClient
from config import settings

# Ensure this logger uses the same configuration as main
logger = logging.getLogger(__name__)
# Make sure the logger propagates to the root logger
logger.propagate = True


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

        # Log initialization
        logger.info(f"LLMClient initialized with:")
        logger.info(f"  Base URL: {self.base_url}")
        logger.info(f"  Model: {self.model}")
        logger.info(f"  Moderation Model: {self.moderation_model}")
        logger.info(f"  Temperature: {self.temperature}")
        logger.info(f"  Max Tokens: {self.max_tokens}")

    async def _make_request(self, prompt: str, model: Optional[str] = None) -> Optional[str]:
        """Make a request to the LLM server using Ollama."""
        try:
            model_to_use = model or self.model
            logger.info(f"Making LLM request to {self.base_url} with model {model_to_use}")
            logger.debug(f"Request prompt: {prompt[:100]}...")  # Log first 100 chars of prompt

            response = await self.client.generate(
                model=model_to_use,
                prompt=prompt,
                options={
                    'temperature': self.temperature,
                    'num_predict': self.max_tokens,
                }
            )

            if response and 'response' in response:
                response_text = response['response'].strip()
                logger.info(f"LLM response received: {response_text[:100]}...")  # Log first 100 chars
                return response_text
            else:
                logger.error(f"Invalid response format from Ollama: {response}")
                return None

        except Exception as e:
            logger.error(f"LLM request failed: {str(e)}", exc_info=True)
            return None

    async def moderate_content(self, message: str) -> Tuple[bool, Optional[str]]:
        """
        Check if the message content is appropriate.

        Returns:
            Tuple of (is_safe, reason_if_not_safe)
        """
        # Content moderation is now always available when called
        # The decision to moderate is made at the API level

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

    def _is_emoji_modifier_only(self, text: str) -> bool:
        """
        Check if the text contains only emoji modifiers (variation selectors, joiners)
        without any actual emoji characters.
        """
        if not text:
            return True

        for char in text:
            code_point = ord(char)
            # If we find any character that's NOT a modifier, it's not modifier-only
            if not (0xFE00 <= code_point <= 0xFE0F or  # Variation selectors
                    code_point == 0x200D or            # Zero-width joiner
                    code_point == 0x200C):             # Zero-width non-joiner
                return False

        # All characters are modifiers
        return True

    def _split_emoji_string(self, text: str) -> List[str]:
        """
        Split a continuous string of emojis into individual emoji units.
        Uses a simpler approach that works better with complex emojis.
        """
        if not text:
            return []

        emojis = []
        current_emoji = ""
        i = 0

        while i < len(text):
            char = text[i]
            code_point = ord(char)

            # Check if this is a base emoji character (not a modifier)
            is_base_emoji = (
                0x1F600 <= code_point <= 0x1F64F or  # Emoticons
                0x1F300 <= code_point <= 0x1F5FF or  # Misc Symbols and Pictographs
                0x1F680 <= code_point <= 0x1F6FF or  # Transport and Map
                0x1F1E0 <= code_point <= 0x1F1FF or  # Regional indicators
                0x2600 <= code_point <= 0x26FF or   # Misc symbols
                0x2700 <= code_point <= 0x27BF      # Dingbats
            )

            # Check if this is a modifier
            is_modifier = (
                0xFE00 <= code_point <= 0xFE0F or  # Variation selectors
                code_point == 0x200D or            # Zero-width joiner
                code_point == 0x200C               # Zero-width non-joiner
            )

            if is_base_emoji:
                # If we already have a current emoji, save it and start a new one
                if current_emoji and not self._is_emoji_modifier_only(current_emoji):
                    emojis.append(current_emoji)
                current_emoji = char
            elif is_modifier and current_emoji:
                # Add modifier to current emoji
                current_emoji += char
            elif not is_modifier and not is_base_emoji:
                # Non-emoji character, save current emoji if any
                if current_emoji and not self._is_emoji_modifier_only(current_emoji):
                    emojis.append(current_emoji)
                current_emoji = ""
            # Skip other characters

            i += 1

        # Don't forget the last emoji
        if current_emoji and not self._is_emoji_modifier_only(current_emoji):
            emojis.append(current_emoji)

        return emojis

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
            # First try splitting by spaces to handle space-separated emojis
            potential_emojis = response.split()
            emojis = []

            for item in potential_emojis:
                # Clean the item and check if it's not empty
                cleaned_item = item.strip()
                if not cleaned_item:
                    continue

                # Check if the item contains emoji characters
                has_emoji = False
                for char in cleaned_item:
                    code_point = ord(char)
                    # Check for common emoji Unicode ranges
                    if (0x1F600 <= code_point <= 0x1F64F or  # Emoticons
                        0x1F300 <= code_point <= 0x1F5FF or  # Misc Symbols and Pictographs
                        0x1F680 <= code_point <= 0x1F6FF or  # Transport and Map
                        0x1F1E0 <= code_point <= 0x1F1FF or  # Regional indicators
                        0x2600 <= code_point <= 0x26FF or   # Misc symbols
                        0x2700 <= code_point <= 0x27BF or   # Dingbats
                        0xFE00 <= code_point <= 0xFE0F or   # Variation selectors
                        code_point == 0x200D):              # Zero-width joiner
                        has_emoji = True
                        break

                if has_emoji and not self._is_emoji_modifier_only(cleaned_item):
                    # If the item looks like it contains multiple emojis, split it
                    # We use a simple heuristic: if it's longer than 2 characters, it might be multiple emojis
                    if len(cleaned_item) > 2:
                        split_emojis = self._split_emoji_string(cleaned_item)
                        if len(split_emojis) > 1:
                            # Successfully split into multiple emojis
                            emojis.extend(split_emojis)
                        else:
                            # Couldn't split or only one emoji, add as is
                            emojis.append(cleaned_item)
                    else:
                        emojis.append(cleaned_item)

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

    async def generate_sample_sentence(self) -> str:
        """
        Generate a short inspirational sentence to use as inspiration for users.

        Returns:
            A short inspirational sentence
        """
        sample_prompt = """
You are a creative writing assistant. Generate a short, single sentence that would make good candiate for an emoji-reaction.

The sentence should be:
- 5-15 words long
- Suitable for all ages
- Not too specific to any particular situation

Examples of good inspirational sentences:
- "Today feels like a day full of possibilities!"
- "I'm grateful for the little moments that make me smile."
- "There's something magical about discovering new things."
- "I love how music can change my entire mood."
- "Sometimes the best adventures happen close to home."

Generate ONE inspirational sentence following these guidelines. Respond with only the sentence, no quotes or additional text.
"""

        try:
            response = await self._make_request(sample_prompt)
            if response is None:
                logger.warning("Sample generation failed, returning default sample")
                return "Today is a great day to share something positive!"

            # Clean up the response
            cleaned_response = response.strip()

            # Remove quotes if present
            if cleaned_response.startswith('"') and cleaned_response.endswith('"'):
                cleaned_response = cleaned_response[1:-1]
            elif cleaned_response.startswith("'") and cleaned_response.endswith("'"):
                cleaned_response = cleaned_response[1:-1]

            # Ensure it's not too long (fallback if LLM doesn't follow instructions)
            if len(cleaned_response) > 100:
                logger.warning("Generated sample too long, using fallback")
                return "Today is a great day to share something positive!"

            # Ensure it's not empty
            if not cleaned_response:
                logger.warning("Generated sample is empty, using fallback")
                return "Today is a great day to share something positive!"

            return cleaned_response

        except Exception as e:
            logger.error(f"Sample generation error: {str(e)}")
            return "Today is a great day to share something positive!"  # Fallback sample


# Global LLM client instance
llm_client = LLMClient()

