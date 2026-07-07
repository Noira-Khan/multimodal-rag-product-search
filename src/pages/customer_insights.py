"""
==========================================================
CUSTOMER INSIGHTS

Part 1

✓ Imports
✓ Analytics Engine
✓ Header
✓ Executive Summary
==========================================================
"""

import streamlit as st

from analytics_service import Analytics

from components.Dashboard import (
    dashboard_container,
    dashboard_header,
    section_header,
    metric_divider,
)

# ==========================================================
# PAGE SETUP
# ==========================================================

st.set_page_config(
    page_title="Customer Insights",
    page_icon="🧠",
    layout="wide",
)

dashboard_container()

# ==========================================================
# LOAD ANALYTICS
# ==========================================================

analytics = Analytics()

dashboard = analytics.dashboard_pipeline()

kpis = dashboard["kpis"]

# ==========================================================
# HEADER
# ==========================================================

dashboard_header(

    "Customer Insights",

    "Understand customer behaviour using AI-powered product analytics."

)

# ==========================================================
# EXECUTIVE SUMMARY
# ==========================================================

section_header(

    "Executive Summary",

    "📊"

)

col1, col2 = st.columns(2)

with col1:

    st.metric(

        "Total Searches",

        kpis["Total Searches"]

    )

    st.metric(

        "Total Chats",

        kpis["Total Chats"]

    )

with col2:

    st.metric(

        "Recommendation Acceptance",

        f'{kpis["Recommendation Acceptance"]:.1f}%'

    )

    st.metric(

        "Search Success",

        f'{kpis["Search Success Rate"]:.1f}%'

    )

metric_divider()


# ==========================================================
# CUSTOMER BEHAVIOUR
# ==========================================================

section_header(

    "Customer Behaviour",

    "👥"

)

left, right = st.columns(2)

# ----------------------------------------------------------
# Search Behaviour
# ----------------------------------------------------------

with left:

    st.markdown(
        """
### 🔍 Search Behaviour

Customers primarily discover products through
semantic search.

Search activity indicates the first step of the
shopping journey and reflects user intent.

Higher search volume generally increases
recommendation opportunities.
"""
    )

    st.metric(

        "Search Success Rate",

        f'{kpis["Search Success Rate"]:.1f}%'

    )

# ----------------------------------------------------------
# Recommendation Behaviour
# ----------------------------------------------------------

with right:

    st.markdown(
        """
### 🤖 Recommendation Behaviour

Recommendations help customers discover
similar products without issuing additional
searches.

A higher recommendation acceptance rate
indicates stronger personalization quality.
"""
    )

    st.metric(

        "Recommendation Acceptance",

        f'{kpis["Recommendation Acceptance"]:.1f}%'

    )

metric_divider()

# ==========================================================
# USER JOURNEY
# ==========================================================

section_header(

    "AI Shopping Journey",

    "🛒"

)

st.markdown(
"""
### Typical Customer Flow

1️⃣ User searches for a product

⬇

2️⃣ Semantic Search retrieves relevant products

⬇

3️⃣ Customer views recommendations

⬇

4️⃣ Customer compares products

⬇

5️⃣ Customer interacts with AI Assistant

⬇

6️⃣ Customer makes a purchasing decision

---

This represents the ideal engagement funnel for the
Multimodal Retail Assistant.
"""
)

metric_divider()

# ==========================================================
# AI PRODUCT INSIGHTS
# ==========================================================

section_header(

    "AI Product Insights",

    "🧠"

)

col1, col2 = st.columns(2)

# ----------------------------------------------------------
# Customer Insights
# ----------------------------------------------------------

with col1:

    st.info(
"""
### 📈 Customer Behaviour Insights

• Users begin their shopping journey through semantic search.

• Recommendation quality directly influences product discovery.

• Product comparison reduces purchase uncertainty.

• AI conversations help customers understand product differences before making a decision.

• Higher recommendation acceptance generally indicates better personalization.
"""
    )

# ----------------------------------------------------------
# Product Opportunities
# ----------------------------------------------------------

with col2:

    st.success(
"""
### 🚀 Product Opportunities

• Improve recommendation diversity.

• Add image-based recommendations.

• Increase click-through rate using personalized ranking.

• Improve search quality for long-tail queries.

• Introduce seasonal and trending recommendations.
"""
    )

metric_divider()

# ==========================================================
# PM RECOMMENDATIONS
# ==========================================================

section_header(

    "Product Manager Recommendations",

    "🎯"

)

st.warning(
"""
### Suggested Next Steps

**Priority 1**

Improve recommendation quality using user interaction signals.

---

**Priority 2**

Reduce search abandonment by improving semantic retrieval.

---

**Priority 3**

Increase engagement with AI Assistant through contextual suggestions.

---

**Priority 4**

Introduce personalized recommendations based on previous searches.

---

**Priority 5**

Track user behaviour using event analytics to continuously improve search quality.
"""
)

metric_divider()


# ==========================================================
# EXECUTIVE HEALTH SCORE
# ==========================================================

section_header(

    "Executive Health Score",

    "🏆"

)

health_score = (

    kpis["Search Success Rate"] * 0.40 +

    kpis["CTR"] * 0.25 +

    kpis["Recommendation Acceptance"] * 0.20 +

    kpis["North Star Metric"] * 0.15

)

health_score = round(

    health_score,

    1

)

left, right = st.columns([1, 2])

with left:

    st.metric(

        "Overall Health",

        f"{health_score}%"

    )

with right:

    if health_score >= 80:

        st.success(

            "🟢 Product health is excellent. Customer engagement and AI performance are meeting business expectations."

        )

    elif health_score >= 60:

        st.warning(

            "🟡 Product health is stable. There are opportunities to improve engagement and recommendation quality."

        )

    else:

        st.error(

            "🔴 Product health requires attention. Focus on improving search quality and recommendation effectiveness."

        )

metric_divider()

# ==========================================================
# BUSINESS IMPACT
# ==========================================================

section_header(

    "Business Impact",

    "💼"

)

impact_left, impact_right = st.columns(2)

with impact_left:

    st.markdown(
"""
### 📈 Product Outcomes

- Better product discovery

- Faster customer decision-making

- Improved shopping experience

- Higher recommendation engagement

- AI-assisted product exploration
"""
    )

with impact_right:

    st.markdown(
"""
### 🎯 Product KPIs

- Increase Search Success Rate

- Improve Recommendation Acceptance

- Reduce Product Comparison Time

- Increase Customer Engagement

- Improve AI Assistant Adoption
"""
    )

metric_divider()

# ==========================================================
# FUTURE ROADMAP
# ==========================================================

section_header(

    "Future Product Opportunities",

    "🚀"

)

st.markdown(
"""
| Priority | Opportunity | Expected Impact |
|----------|-------------|-----------------|
| High | Personalized Recommendations | Higher CTR |
| High | Image Search Ranking | Better Discovery |
| Medium | Voice Commerce | Improved Accessibility |
| Medium | Customer Preference Profiles | Better Personalization |
| Low | Trend Prediction | Seasonal Recommendations |
"""
)

metric_divider()

# ==========================================================
# FOOTER
# ==========================================================

st.caption(
"""
Customer Insights Dashboard

Multimodal Retail Assistant (Myntra AI)

Built using Streamlit • RAG • FAISS • Gemini AI • Product Analytics
"""
)

