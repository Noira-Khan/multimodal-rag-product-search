import streamlit as st
from google import genai

st.title("Gemini Test")

client = genai.Client(
    api_key=st.secrets["GOOGLE_API_KEY"]
)

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Say hello in one sentence."
)

st.success(response.text)
