import streamlit as st


def show_feature_cards():

    st.markdown("## 🚀 AI Shopping Features")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown(
            """
### 🔍 Semantic Search

Search products using natural language.

Example:

> "Blue casual jeans"

> "Black sneakers"

> "Formal office shirts"
"""
        )

    with col2:

        st.markdown(
            """
### 🖼 Image Search

Upload any fashion image.

Our CLIP model retrieves visually similar products from the catalog.
"""
        )

    with col3:

        st.markdown(
            """
### 🤖 AI Fashion Assistant

Ask:

"What matches this shirt?"

"Suggest an outfit"

"Compare two products"
"""
        )

    st.write("")

    col4, col5, col6 = st.columns(3)

    with col4:

        st.success(
            """
🎤 Voice Search

Search using speech instead of typing.
"""
        )

    with col5:

        st.success(
            """
❤️ Personalized Recommendations

AI understands user preferences.
"""
        )

    with col6:

        st.success(
            """
⚡ Fast Retrieval

Vector Search + FAISS
"""
        )