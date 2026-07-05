# ==========================================================
# app.py
# MultiRAG Product Search
# ==========================================================

import streamlit as st
from pathlib import Path

# ----------------------------------------------------------
# PAGE CONFIGURATION
# ----------------------------------------------------------

st.set_page_config(
    page_title="MultiRAG Product Search",
    page_icon="🛍️",
    layout="wide",
)

# ----------------------------------------------------------
# LOAD GLOBAL CSS
# ----------------------------------------------------------

ROOT = Path(__file__).resolve().parent
CSS = ROOT / "css" / "style.css"

if CSS.exists():
    with open(CSS, "r", encoding="utf-8") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True,
        )

# ----------------------------------------------------------
# DEFINE PAGES
# ----------------------------------------------------------

home = st.Page(
    "pages/home.py",
    title="Home",
    icon="🏠",
    default=True,
)

product_search = st.Page(
    "pages/product_search.py",
    title="Product Search",
    icon="🔍",
)

ai_assistant = st.Page(
    "pages/AI_assistance.py",
    title="AI Assistant",
    icon="🤖",
)

recommendations = st.Page(
    "pages/recommendations.py",
    title="Recommendations",
    icon="✨",
)

comparison = st.Page(
    "pages/product_comparison.py",
    title="Comparison",
    icon="⚖️",
)

analytics = st.Page(
    "pages/analytics.py",
    title="Analytics",
    icon="📊",
)

customers = st.Page(
    "pages/customer_insights.py",
    title="Customers",
    icon="👥",
)



# ----------------------------------------------------------
# TOP NAVIGATION
# ----------------------------------------------------------

navigation = st.navigation(
    [
        home,
        product_search,
        ai_assistant,
        recommendations,
        comparison,
        analytics,
        customers,
    ],
    position="top",
)

# ----------------------------------------------------------
# RUN SELECTED PAGE
# ----------------------------------------------------------

navigation.run()