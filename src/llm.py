"""
==========================================================
LLM SERVICE
Multimodal Retail Assistant (Myntra AI)
==========================================================

Module:
    llm.py

Responsibilities
----------------
✔ Initialize Gemini
✔ Generate Responses
✔ Health Check

Author:
    Noira Khan
==========================================================
"""

from __future__ import annotations

import logging

import google.generativeai as genai

from config import (
    GOOGLE_API_KEY,
    MODEL_NAME,
)

# ==========================================================
# Logging
# ==========================================================

logging.basicConfig(

    level=logging.INFO,

    format="%(levelname)s | %(message)s"

)

logger = logging.getLogger(__name__)

# ==========================================================
# Gemini Client
# ==========================================================


class GeminiClient:

    def __init__(self):

        logger.info(
            "Initializing Gemini Client..."
        )

        if not GOOGLE_API_KEY:

            raise ValueError(
                "GOOGLE_API_KEY not found."
            )

        genai.configure(
            api_key=GOOGLE_API_KEY
        )

        self.model = genai.GenerativeModel(
            MODEL_NAME
        )

        logger.info(
            "Gemini Ready."
        )

    # ------------------------------------------------------

    def generate(
        self,
        prompt: str,
    ):

        response = self.model.generate_content(
            prompt
        )

        return response.text.strip()

    # ------------------------------------------------------

    def health(self):

        return {

            "provider": "Google Gemini",

            "model": MODEL_NAME,

            "status": "Ready"

        }


# ==========================================================
# Testing
# ==========================================================

if __name__ == "__main__":

    client = GeminiClient()

    print(

        client.generate(

            "Say hello."

        )

    )

    print(

        client.health()

    )

    