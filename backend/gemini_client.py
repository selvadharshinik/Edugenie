import logging
from typing import Optional, Dict, Any, List, Union
from backend.config import settings
from backend.utils.json_parser import parse_json_from_llm

logger = logging.getLogger(__name__)

MODEL_CANDIDATES = [
    "gemini-3.5-flash",
    "gemini-3.8-flash",
    "gemini-3.6-flash",
    "gemini-flash-latest",
    "gemma-4-26b-a4b-it",
    "gemini-3.1-pro-preview"
]

class GeminiClient:
    """
    Centralized, resilient client abstraction for Google Gemini API.
    Features dynamic model fallback and live key reloading.
    """

    def __init__(self, api_key: Optional[str] = None, model_name: Optional[str] = None):
        self._custom_api_key = api_key
        self._custom_model_name = model_name
        self.working_model: Optional[str] = None
        self._genai_client = None

    @property
    def api_key(self) -> str:
        return self._custom_api_key or settings.GEMINI_API_KEY

    @property
    def model_name(self) -> str:
        return self._custom_model_name or settings.PRIMARY_MODEL

    def get_client(self):
        """Returns or re-initializes genai client dynamically."""
        key = self.api_key
        if not key or key == "your_gemini_api_key_here":
            return None
        
        from google import genai
        # Always return client instantiated with latest key
        return genai.Client(api_key=key)

    def is_ready(self) -> bool:
        """Returns True if a valid API key is configured."""
        key = self.api_key
        return bool(key and key != "your_gemini_api_key_here")

    def generate_text(
        self,
        prompt: str,
        temperature: float = settings.DEFAULT_TEMPERATURE,
        max_tokens: int = settings.MAX_OUTPUT_TOKENS,
    ) -> str:
        """
        Generates text using Gemini model with dynamic model candidate fallback.
        """
        if not self.is_ready():
            raise RuntimeError(
                "EduGenie AI key is missing or invalid. Please check that GEMINI_API_KEY in .env is configured."
            )

        client = self.get_client()
        if not client:
            raise RuntimeError("Failed to initialize Google Gemini client.")

        models_to_try = []
        if self.working_model:
            models_to_try.append(self.working_model)
        for m in [self.model_name] + MODEL_CANDIDATES:
            if m not in models_to_try:
                models_to_try.append(m)

        last_error = None
        for model in models_to_try:
            try:
                response = client.models.generate_content(
                    model=model,
                    contents=prompt,
                    config={
                        "temperature": temperature,
                        "max_output_tokens": max_tokens,
                    }
                )

                self.working_model = model

                if hasattr(response, "text") and response.text:
                    return response.text
                elif hasattr(response, "candidates") and response.candidates:
                    return response.candidates[0].content.parts[0].text
                else:
                    raise ValueError("Received empty content from Gemini API.")

            except Exception as err:
                error_str = str(err)
                logger.warning(f"Model '{model}' failed: {error_str}")
                last_error = err

                if "404" in error_str or "NOT_FOUND" in error_str or "503" in error_str or "UNAVAILABLE" in error_str:
                    continue
                elif "400" in error_str and ("API_KEY" in error_str or "API key" in error_str or "INVALID_ARGUMENT" in error_str):
                    raise RuntimeError(
                        f"The provided API key is invalid ({error_str}). Please ensure your GEMINI_API_KEY in .env is valid."
                    )
                elif "401" in error_str or "UNAUTHENTICATED" in error_str:
                    raise RuntimeError(
                        "Gemini API authentication failed. Please verify your GEMINI_API_KEY in .env."
                    )
                elif "429" in error_str or "RESOURCE_EXHAUSTED" in error_str or "quota" in error_str.lower():
                    continue

        raise RuntimeError(
            f"EduGenie couldn't generate a response right now ({last_error})."
        )

    def generate_json(
        self,
        prompt: str,
        temperature: float = settings.QUIZ_TEMPERATURE,
        max_tokens: int = settings.MAX_OUTPUT_TOKENS,
    ) -> Union[Dict[str, Any], List[Any]]:
        """
        Generates content from Gemini and parses it as clean JSON.
        """
        raw_output = self.generate_text(prompt, temperature=temperature, max_tokens=max_tokens)
        return parse_json_from_llm(raw_output)

gemini_client = GeminiClient()
