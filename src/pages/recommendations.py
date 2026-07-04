"""
==========================================================
RECOMMENDATIONS PAGE
Multimodal Retail Assistant (Myntra AI)
==========================================================
"""

import streamlit as st

from recommendation_engine import RecommendationEngine


# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------

st.set_page_config(
    page_title="AI Recommendations",
    page_icon="🎯",
    layout="wide"
)

st.title("🎯 AI Product Recommendations")

st.write(
    "Get personalized recommendations powered by "
    "RAG + Gemini."
)

# ---------------------------------------------------------
# LOAD ENGINE
# ---------------------------------------------------------

@st.cache_resource
def load_engine():
    return RecommendationEngine()


engine = load_engine()

# ---------------------------------------------------------
# SESSION
# ---------------------------------------------------------

if "recommendations" not in st.session_state:
    st.session_state.recommendations = None

if "last_query" not in st.session_state:
    st.session_state.last_query = ""

# ---------------------------------------------------------
# SEARCH
# ---------------------------------------------------------

st.divider()

query = st.text_input(
    "🔍 Describe what you're looking for",
    placeholder="Example: black running shoes"
)

top_k = st.slider(
    "Number of Recommendations",
    min_value=3,
    max_value=10,
    value=5
)

col1, col2 = st.columns([1, 1])

with col1:

    recommend_clicked = st.button(
        "✨ Recommend Products",
        use_container_width=True
    )

with col2:

    clear_clicked = st.button(
        "🗑 Clear",
        use_container_width=True
    )

# ---------------------------------------------------------
# CLEAR
# ---------------------------------------------------------

if clear_clicked:

    st.session_state.recommendations = None
    st.session_state.last_query = ""

    st.rerun()

# ---------------------------------------------------------
# GENERATE RECOMMENDATIONS
# ---------------------------------------------------------

if recommend_clicked:

    if not query.strip():

        st.warning(
            "Please enter a search query."
        )

    else:

        with st.spinner(
            "Finding the best recommendations..."
        ):

            pipeline = engine.recommendation_pipeline(
                query=query,
                top_k=top_k
            )

        st.session_state.recommendations = pipeline
        st.session_state.last_query = query
# ---------------------------------------------------------
# DISPLAY RECOMMENDATIONS
# ---------------------------------------------------------

if st.session_state.recommendations:

    pipeline = st.session_state.recommendations

    recommendations = pipeline["recommendations"]

    explanations = pipeline["explanations"]

    st.divider()

    st.subheader(
        f"🎯 Results for '{st.session_state.last_query}'"
    )

    st.caption(
        f"{len(recommendations)} products recommended"
    )

    # -----------------------------------------------------

    for product, explanation in zip(

        recommendations,

        explanations,

    ):

        with st.container(border=True):

            col1, col2 = st.columns([1, 3])

            # ---------------------------------------------

            with col1:

                image_path = product.get(
                    "image_path",
                    ""
                )

                if image_path:

                    st.image(
                        image_path,
                        use_container_width=True,
                    )

                else:

                    st.image(
                        "https://placehold.co/300x400?text=No+Image",
                        use_container_width=True,
                    )

            # ---------------------------------------------

            with col2:

                st.markdown(

                    f"### {product['product_name']}"

                )

                if "similarity" in product:

                    st.progress(

                        min(

                            float(product["similarity"]),

                            1.0

                        )

                    )

                    st.caption(

                        f"Similarity Score: {product['similarity']:.3f}"

                    )

                st.markdown(

                    "**Product Information**"

                )

                st.code(

                    product["document"]

                )

                st.success(

                    "🤖 AI Recommendation"

                )

                st.write(

                    explanation

                )

                b1, b2, b3 = st.columns(3)

                with b1:

                    st.button(

                        "👀 View",

                        key=f"view_{product['id']}"

                    )

                with b2:

                    st.button(

                        "⚖ Compare",

                        key=f"compare_{product['id']}"

                    )

                with b3:

                    st.button(

                        "❤ Save",

                        key=f"save_{product['id']}"

                    )

        st.markdown("<br>", unsafe_allow_html=True)
    # ---------------------------------------------------------
# RECOMMENDATION ANALYTICS
# ---------------------------------------------------------

if st.session_state.recommendations:

    pipeline = st.session_state.recommendations

    recommendations = pipeline["recommendations"]

    st.divider()

    st.subheader("📊 Recommendation Analytics")

    c1, c2, c3 = st.columns(3)

    with c1:

        st.metric(
            "Products Found",
            len(recommendations)
        )

    with c2:

        similarities = []

        for product in recommendations:

            if "similarity" in product:

                similarities.append(
                    product["similarity"]
                )

        if similarities:

            avg = sum(similarities) / len(similarities)

            st.metric(
                "Average Similarity",
                f"{avg:.2f}"
            )

        else:

            st.metric(
                "Average Similarity",
                "N/A"
            )

    with c3:

        st.metric(
            "Search Query",
            st.session_state.last_query
        )

# ---------------------------------------------------------
# AI INSIGHTS
# ---------------------------------------------------------

if st.session_state.recommendations:

    st.divider()

    st.subheader("🧠 AI Insights")

    st.info(
        """
These recommendations are generated using:

• Semantic Search

• Sentence Transformers

• FAISS Vector Search

• Retrieval-Augmented Generation (RAG)

• Gemini AI

Products are retrieved using vector similarity,
then ranked and explained by the AI assistant.
"""
    )

# ---------------------------------------------------------
# SAVE FAVOURITES
# ---------------------------------------------------------

if "saved_products" not in st.session_state:

    st.session_state.saved_products = []

# ---------------------------------------------------------
# DISPLAY SAVED PRODUCTS
# ---------------------------------------------------------

if len(st.session_state.saved_products):

    st.divider()

    st.subheader("❤️ Saved Products")

    for item in st.session_state.saved_products:

        st.write("•", item)

# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------

with st.sidebar:

    st.header("⚡ Recommendation Engine")

    st.success("Semantic Search")

    st.success("Vector Database")

    st.success("RAG")

    st.success("Gemini AI")

    st.success("Explainable AI")

    st.divider()

    st.metric(

        "Catalogue",

        engine.total_products()

    )

    st.metric(

        "Current Results",

        len(

            st.session_state.recommendations["recommendations"]

        )

        if st.session_state.recommendations

        else 0

    )

    st.divider()

    st.caption(
        """
Multimodal Retail Assistant

AI Product Management Portfolio

Built using

• Streamlit

• FAISS

• Sentence Transformers

• Gemini
"""
    )

# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------

st.divider()

st.caption(
    """
© 2026 Noira Khan

Multimodal Retail Assistant

Recommendation Engine

Powered by RAG + Gemini
"""
)
