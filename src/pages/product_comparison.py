"""
==========================================================
PRODUCT COMPARISON — PART 1 OF 4
Multimodal Retail Assistant (Myntra AI)
==========================================================

Responsibilities
----------------
✓ Page Configuration
✓ Imports
✓ Session State
✓ Recommendation Engine
✓ Product Selection UI

Upcoming
--------
Part 2
✓ Compare Button
✓ Comparison Table

Part 3
✓ AI Comparison
✓ Winner Card

Part 4
✓ History
✓ Clear Comparison
✓ Export
==========================================================
"""

import streamlit as st
import difflib
from recommendation_engine import RecommendationEngine
from analytics import Analytics
# ==========================================================
# Page Configuration
# ==========================================================

st.set_page_config(
    page_title="Product Comparison",
    page_icon="⚖",
    layout="wide"
)

st.title("⚖ AI Product Comparison")

st.caption(
    "Compare two fashion products using AI."
)

# ==========================================================
# Engine
# ==========================================================

@st.cache_resource
def load_engine():

    return RecommendationEngine()


engine = load_engine()
analytics = Analytics()
# ==========================================================
# Session State
# ==========================================================

if "comparison_history" not in st.session_state:

    st.session_state.comparison_history = []

# ==========================================================
# Product List
# ==========================================================

product_names = sorted(

    engine.product_names()

)


# ==========================================================
# Product Selection
# ==========================================================



left, right = st.columns(2)

# -------------------------
# PRODUCT A
# -------------------------

with left:

    st.subheader("🛍 Product A")

    query_a = st.text_input(
        "Search Product A",
        placeholder="Type product name..."
    )

    if query_a:

        suggestions_a = difflib.get_close_matches(
            query_a,
            product_names,
            n=20,
            cutoff=0.1
        )

    else:

        suggestions_a = product_names[:20]

    product_a = st.selectbox(
        "Matching Products",
        suggestions_a,
        key="product_a"
    )

# -------------------------
# PRODUCT B
# -------------------------

with right:

    st.subheader("🛍 Product B")

    query_b = st.text_input(
        "Search Product B",
        placeholder="Type product name..."
    )

    if query_b:

        suggestions_b = difflib.get_close_matches(
            query_b,
            product_names,
            n=20,
            cutoff=0.1
        )

    else:

        suggestions_b = product_names[:20]

    product_b = st.selectbox(
        "Matching Products",
        suggestions_b,
        key="product_b"
    )
# ==========================================================
# Compare Button
# ==========================================================

compare_button = st.button(

    "⚖ Compare Products",

    use_container_width=True,

    type="primary"

)

# ==========================================================
# Comparison
# ==========================================================

if compare_button:

    if product_a == product_b:

        st.warning(

            "Please select two different products."

        )

    else:

        with st.spinner(

            "Comparing products..."

        ):

            comparison = engine.compare_products(

                product_a,

                product_b

            )

        if comparison is None:

            st.error(

                "Unable to compare these products."

            )

        else:

            analytics.log_comparison(

                product_a,

                product_b

                )

    st.success(

        "Comparison completed."

    )

    st.session_state.comparison_history.append(

        {

            "product_a": product_a,

            "product_b": product_b

        }

    )

    st.subheader(

                "📊 Product Comparison"

            )

            st.dataframe(

                comparison,

                use_container_width=True,

                hide_index=True

            )
# ==========================================================
# AI Comparison
# ==========================================================

            st.divider()

            st.subheader("🤖 AI Comparison")

            with st.spinner(

                "Gemini is analysing both products..."

            ):

                ai_response = engine.ai_compare_products(

                    product_a,

                    product_b

                )

            st.markdown(ai_response)

# ==========================================================
# Comparison Summary
# ==========================================================

            st.divider()

            st.subheader("📌 Quick Summary")

            col1, col2 = st.columns(2)

            with col1:

                st.success(

                    f"Product A\n\n{product_a}"

                )

            with col2:

                st.info(

                    f"Product B\n\n{product_b}"

                )

# ==========================================================
# Save History
# ==========================================================

            st.session_state.comparison_history.append(

                {

                    "product_a": product_a,

                    "product_b": product_b,

                    "ai_summary": ai_response

                }

            )
    # ==========================================================
# Comparison History
# ==========================================================

st.divider()

st.subheader("🕒 Comparison History")

if st.session_state.comparison_history:

    for i, item in enumerate(

        reversed(st.session_state.comparison_history),

        start=1

    ):

        with st.expander(

            f"Comparison {i}"

        ):

            st.write(

                "**Product A:**",

                item["product_a"]

            )

            st.write(

                "**Product B:**",

                item["product_b"]

            )

            if "ai_summary" in item:

                st.markdown(

                    item["ai_summary"]

                )

else:

    st.info(

        "No comparisons yet."

    )

# ==========================================================
# Export Comparison
# ==========================================================

if st.session_state.comparison_history:

    export_text = ""

    for item in st.session_state.comparison_history:

        export_text += (

            f"Product A: {item['product_a']}\n"

            f"Product B: {item['product_b']}\n\n"

        )

        if "ai_summary" in item:

            export_text += (

                item["ai_summary"]

            )

        export_text += (

            "\n"

            + "=" * 70

            + "\n\n"

        )

    st.download_button(

        "📥 Download Comparison History",

        data=export_text,

        file_name="comparison_history.txt",

        mime="text/plain",

        use_container_width=True

    )

# ==========================================================
# Clear History
# ==========================================================

if st.button(

    "🗑 Clear Comparison History",

    use_container_width=True

):

    st.session_state.comparison_history = []

    st.success(

        "Comparison history cleared."

    )

    st.rerun()

# ==========================================================
# Assistant Status
# ==========================================================

st.divider()

with st.expander(

    "⚙ Engine Status"

):

    st.success(

        "Recommendation Engine Loaded"

    )

    st.write(

        "Products:",

        len(product_names)

    )

    st.write(

        "Previous Comparisons:",

        len(

            st.session_state.comparison_history

        )

    )
    