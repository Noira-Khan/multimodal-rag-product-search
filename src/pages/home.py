# ==========================================================
# home.py
# Multimodal RAG Product Search
# ==========================================================

import streamlit as st

# ----------------------------------------------------------
# PAGE CONFIGURATION
# ----------------------------------------------------------


# ----------------------------------------------------------
# LOAD CSS
# ----------------------------------------------------------

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSS = ROOT / "css" / "style.css"

if CSS.exists():
    with open(CSS, "r", encoding="utf-8") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True,
        )
else:
    st.warning(f"CSS file not found: {CSS}")

# ----------------------------------------------------------
# IMPORT COMPONENTS
# ----------------------------------------------------------

from components.navbar import show_navbar
from components.hero import show_hero
from components.sidebar import show_sidebar
from components.cards import show_feature_cards
from components.metrics import show_metrics
from components.footer import show_footer

# ----------------------------------------------------------
# SIDEBAR
# ----------------------------------------------------------



# ----------------------------------------------------------
# NAVBAR
# ----------------------------------------------------------

show_navbar()

# ----------------------------------------------------------
# HERO
# ----------------------------------------------------------

show_hero()

st.markdown("<br>", unsafe_allow_html=True)

# ----------------------------------------------------------
# METRICS
# ----------------------------------------------------------

show_metrics()

st.markdown("---")

# ----------------------------------------------------------
# SHOP BY CATEGORY
# ----------------------------------------------------------

st.header("🛍 Shop by Category")

c1, c2, c3, c4, c5 = st.columns(5)

with c1:
    st.markdown(
        """
        <div class="category-card">
            👕
            <h4>Men</h4>
        </div>
        """,
        unsafe_allow_html=True,
    )

with c2:
    st.markdown(
        """
        <div class="category-card">
            👗
            <h4>Women</h4>
        </div>
        """,
        unsafe_allow_html=True,
    )

with c3:
    st.markdown(
        """
        <div class="category-card">
            👟
            <h4>Footwear</h4>
        </div>
        """,
        unsafe_allow_html=True,
    )

with c4:
    st.markdown(
        """
        <div class="category-card">
            🎒
            <h4>Accessories</h4>
        </div>
        """,
        unsafe_allow_html=True,
    )

with c5:
    st.markdown(
        """
        <div class="category-card">
            💄
            <h4>Beauty</h4>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("---")

# ----------------------------------------------------------
# AI FEATURES
# ----------------------------------------------------------

st.header("🤖 AI Shopping Experience")

show_feature_cards()

st.markdown("---")

# ----------------------------------------------------------
# TRENDING COLLECTIONS
# ----------------------------------------------------------

st.header("🔥 Trending Collections")

col1, col2, col3 = st.columns(3)

with col1:
    st.info(
        """
### ☀️ Summer Collection

Lightweight styles

Trending this week
"""
    )

with col2:
    st.success(
        """
### 💼 Office Wear

Minimal

Professional

Comfort Fit
"""
    )

with col3:
    st.warning(
        """
### ✨ Festive Collection

Premium Ethnic

Designer Picks

Limited Edition
"""
    )

st.markdown("---")

# ----------------------------------------------------------
# HOW IT WORKS
# ----------------------------------------------------------

st.header("🚀 How AI Search Works")

s1, s2, s3, s4 = st.columns(4)

with s1:
    st.metric("Step 1", "Search")

with s2:
    st.metric("Step 2", "Retrieve")

with s3:
    st.metric("Step 3", "Rank")

with s4:
    st.metric("Step 4", "Recommend")

st.markdown(
"""
Our AI combines:

- Semantic Search
- CLIP Image Retrieval
- Vector Embeddings
- FAISS Search
- Retrieval-Augmented Generation (RAG)
- Large Language Models

to deliver intelligent fashion recommendations.
"""
)

st.markdown("---")

# ----------------------------------------------------------
# WHY CHOOSE US
# ----------------------------------------------------------

st.header("❤️ Why You'll Love It")

left, right = st.columns(2)

with left:
    st.markdown("""
### Smart Shopping

- ✅ Text Search
- ✅ Image Search
- ✅ Voice Search
- ✅ Similar Products
- ✅ AI Recommendations
""")

with right:
    st.markdown("""
### Fashion Intelligence

- ✅ Outfit Suggestions
- ✅ Personalized Search
- ✅ Fast Discovery
- ✅ AI Stylist
- ✅ Multimodal Retrieval
""")

st.markdown("---")

# ----------------------------------------------------------
# TECHNOLOGY STACK
# ----------------------------------------------------------

st.header("⚡ Powered By")

t1, t2, t3, t4, t5 = st.columns(5)

with t1:
    st.success("Streamlit")

with t2:
    st.success("FAISS")

with t3:
    st.success("CLIP")

with t4:
    st.success("Sentence Transformers")

with t5:
    st.success("OpenAI")

st.markdown("---")

# ----------------------------------------------------------
# FOOTER
# ----------------------------------------------------------

show_footer()