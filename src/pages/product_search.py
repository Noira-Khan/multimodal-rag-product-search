"""
==========================================================
PRODUCT SEARCH PAGE
Multimodal Retail Assistant (Myntra AI)
==========================================================

Features

✔ Semantic Search

✔ Product Cards

✔ Similarity Scores

✔ AI Recommendations

✔ Product Filters

✔ Session State

Author:
Noira Khan
==========================================================
"""

import streamlit as st
from pathlib import Path

from components.sidebar import show_sidebar
from rag_engine import RAGEngine
from analytics import Analytics
import time
st.set_page_config(
    page_title="AI Product Search",
    page_icon="🛍️",
    layout="wide"
)

ROOT = Path(__file__).resolve().parents[1]
CSS = ROOT / "css" / "style.css"

if CSS.exists():
    with open(CSS, "r", encoding="utf-8") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True,
        )






# ---------------------------------------------------------

st.title("🔍 AI Product Search")

st.caption(

    "Search products naturally using AI."

)

# ---------------------------------------------------------
# Examples
# ---------------------------------------------------------

st.info(

"""
Examples

• Black running shoes under ₹3000

• Women's handbags for office

• White sneakers

• Casual shirts

"""
)

# ---------------------------------------------------------
# Search Bar
# ---------------------------------------------------------

query = st.text_input(

    "Search",

    placeholder="Search naturally..."

)

top_k = st.slider(

    "Number of Results",

    1,

    20,

    5

)

# ---------------------------------------------------------

if "rag_engine" not in st.session_state:

    st.session_state.rag_engine = RAGEngine()

rag = st.session_state.rag_engine

analytics = Analytics()
# ---------------------------------------------------------

search_button = st.button(

    "🔍 Search",

    use_container_width=True

)

# ---------------------------------------------------------

if search_button:

    if query.strip() == "":

        st.warning(

            "Enter a search query."

        )

    else:
        start_time = time.time()
        with st.spinner(

            "Searching..."

        ):

            pipeline = rag.search_pipeline(

                query,

                top_k

            )
            response_time = time.time() - start_time

            analytics.log_search(

            query=query,

            results=len(pipeline["results"]),

            response_time=response_time,

            )
        st.success(

            f"{len(pipeline['results'])} products found."

        )

        st.divider()

        # -------------------------------------------------

        for product in pipeline["results"]:

            col1, col2 = st.columns(

                [1, 3]

            )

            with col1:

                st.image(

                    product["image_path"],

                    use_container_width=True

                )

            with col2:

                st.subheader(

                    product["product_name"]

                )

                st.write(

                    f"**Category:** {product['category']}"

                )

                st.write(

                    f"**Brand:** {product['brand']}"

                )

                st.write(

                    f"**Similarity:** {product['similarity']:.2f}"

                )

                st.write("### Why Recommended")

                for item in product["explanation"]:

                    st.write(

                        "✅",

                        item

                    )

                c1, c2, c3 = st.columns(

                    3

                )

                with c1:

                    st.button(

                        "👀 View",

                        key=f"view{product['id']}"

                    )

                with c2:

                    st.button(

                        "⚖ Compare",

                        key=f"compare{product['id']}"

                    )

                with c3:

                    st.button(

                        "🤖 Ask AI",

                        key=f"ask{product['id']}"

                    )

            st.divider()

# ---------------------------------------------------------

with st.expander(

    "Retrieved Context"

):

    if search_button and query:

        st.text(

            pipeline["context"]

        )