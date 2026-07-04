"""
==========================================================
CONFIG
Multimodal Retail Assistant (Myntra AI)
==========================================================
"""

from pathlib import Path
import os
import os

try:
    import streamlit as st

    GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]

except Exception:
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

MODEL_NAME = "gemini-2.5-flash"

MAX_HISTORY = 10

TOP_K = 5

TEMPERATURE = 0.3



