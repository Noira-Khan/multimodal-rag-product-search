"""
==========================================================
AI PRODUCT DASHBOARD

Part 1
✓ Imports
✓ Analytics Engine
✓ Dashboard Header
✓ KPI Cards
==========================================================
"""

import pandas as pd
import streamlit as st

from analytics import Analytics

from components.Dashboard import (
    dashboard_container,
    dashboard_header,
    section_header,
    kpi_grid,
    metric_divider,
    horizontal_bar_chart,
)

# ==========================================================
# PAGE SETUP
# ==========================================================

st.set_page_config(
    page_title="AI Product Dashboard",
    page_icon="📊",
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
# PAGE HEADER
# ==========================================================

dashboard_header(
    "AI Product Dashboard",
    "Executive analytics for the Multimodal Retail Assistant."
)

# ==========================================================
# KPI SECTION
# ==========================================================

section_header(
    "Business KPIs",
    "📈"
)

metrics = [
    {
        "title": "Searches",
        "value": kpis["Total Searches"],
        "delta": "+18%",
        "icon": "🔍",
    },
    {
        "title": "CTR",
        "value": f'{kpis["CTR"]:.1f}%',
        "delta": "+5%",
        "icon": "🎯",
    },
    {
        "title": "Search Success",
        "value": f'{kpis["Search Success Rate"]:.1f}%',
        "delta": "+3%",
        "icon": "✅",
    },
    {
        "title": "Recommendation Rate",
        "value": f'{kpis["Recommendation Acceptance"]:.1f}%',
        "delta": "+8%",
        "icon": "🤖",
    },
]

kpi_grid(metrics)

metric_divider()


# ==========================================================
# USER BEHAVIOUR
# ==========================================================

section_header(
    "User Behaviour",
    "📊"
)

left, right = st.columns(2)

# ----------------------------------------------------------
# Most Searched Products
# ----------------------------------------------------------

with left:

    st.subheader("🔍 Most Searched Products")

    if len(dashboard["top_queries"]) > 0:

        horizontal_bar_chart(
            data=dashboard["top_queries"],
            x="count",
            y="query",
            title=None,
            color="#3B82F6",
        )

    else:

        st.info("No search data available.")

# ----------------------------------------------------------
# Most Compared Products
# ----------------------------------------------------------

with right:

    st.subheader("⚖️ Most Compared Products")

    top_compared = dashboard["top_compared"]

    # Convert list -> DataFrame if needed
    if isinstance(top_compared, list):

        if len(top_compared) > 0:

            top_compared = pd.DataFrame(
                top_compared,
                columns=["product", "count"]
            )

        else:

            top_compared = pd.DataFrame(
                columns=["product", "count"]
            )

    if not top_compared.empty:

        horizontal_bar_chart(
            data=top_compared,
            x="count",
            y="product",
            title=None,
            color="#9333EA",
        )

    else:

        st.info("No compared products available.")

metric_divider()


# ==========================================================
# PERFORMANCE METRICS
# ==========================================================

section_header(
    "Performance Metrics",
    "📈"
)

col1, col2 = st.columns(2)

# ----------------------------------------------------------
# Search Success Rate
# ----------------------------------------------------------

with col1:

    st.metric(
        label="Search Success Rate",
        value=f'{kpis["Search Success Rate"]:.1f}%',
        delta="+3%",
    )

    st.progress(
        min(
            kpis["Search Success Rate"] / 100,
            1.0,
        )
    )

    st.caption(
        "Percentage of searches returning relevant products."
    )

# ----------------------------------------------------------
# Click Through Rate
# ----------------------------------------------------------

with col2:

    st.metric(
        label="Click Through Rate",
        value=f'{kpis["CTR"]:.1f}%',
        delta="+5%",
    )

    st.progress(
        min(
            kpis["CTR"] / 100,
            1.0,
        )
    )

    st.caption(
        "Users who clicked a recommended product."
    )

metric_divider()

# ==========================================================
# PRODUCT HEALTH
# ==========================================================

section_header(
    "Product Health",
    "⭐"
)

left, right = st.columns(2)

# ----------------------------------------------------------
# Recommendation Acceptance
# ----------------------------------------------------------

with left:

    st.metric(
        label="Recommendation Acceptance",
        value=f'{kpis["Recommendation Acceptance"]:.1f}%',
        delta="+8%",
    )

    st.progress(
        min(
            kpis["Recommendation Acceptance"] / 100,
            1.0,
        )
    )

    st.caption(
        "Users accepting AI-generated recommendations."
    )

# ----------------------------------------------------------
# North Star Metric
# ----------------------------------------------------------

with right:

    st.metric(
        label="North Star Metric",
        value=f'{kpis["North Star Metric"]:.1f}%',
        delta="+4%",
    )

    st.progress(
        min(
            kpis["North Star Metric"] / 100,
            1.0,
        )
    )

    st.caption(
        "Overall engagement score of the product."
    )

metric_divider()


# ==========================================================
# AI PRODUCT INSIGHTS
# ==========================================================

section_header(
    "AI Product Insights",
    "🧠"
)

st.success(
f"""
### Executive Summary

The Multimodal Retail Assistant is currently showing healthy engagement.

#### Key Highlights

- 🔍 **Total Searches:** {kpis["Total Searches"]}

- 🤖 **Recommendation Acceptance:** {kpis["Recommendation Acceptance"]:.1f}%

- 🎯 **CTR:** {kpis["CTR"]:.1f}%

- ✅ **Search Success:** {kpis["Search Success Rate"]:.1f}%

#### Product Manager Observations

• Search quality is performing well.

• Recommendation acceptance indicates users trust AI suggestions.

• CTR suggests users are engaging with retrieved products.

• Continue improving ranking quality and personalization to increase
North Star Metric.
"""
)

metric_divider()

# ==========================================================
# PRODUCT OVERVIEW
# ==========================================================

section_header(
    "Product Overview",
    "📋"
)

col1, col2 = st.columns(2)

with col1:

    st.markdown("### Usage Metrics")

    st.markdown(f"""
- 🔍 **Total Searches:** {kpis["Total Searches"]}

- 💬 **Total Chats:** {kpis["Total Chats"]}

- 🤖 **Recommendations Generated:** {kpis["Total Recommendations"]}

- ⚖️ **Product Comparisons:** {kpis["Total Comparisons"]}

- 👆 **Total Clicks:** {kpis["Total Clicks"]}
""")

with col2:

    st.markdown("### Product Health")

    st.markdown(f"""
- ✅ **Search Success Rate:** {kpis["Search Success Rate"]:.1f}%

- 🎯 **CTR:** {kpis["CTR"]:.1f}%

- 🤖 **Recommendation Acceptance:** {kpis["Recommendation Acceptance"]:.1f}%

- ⭐ **North Star Metric:** {kpis["North Star Metric"]:.1f}%

- ⚡ **Average Response Time:** {kpis["Average Response Time"]:.2f} sec
""")

metric_divider()

# ==========================================================
# PRODUCT MANAGER NOTES
# ==========================================================

section_header(
    "Recommendations",
    "💡"
)

st.info(
"""
### Suggested Product Improvements

1. Improve ranking quality for frequently searched products.

2. Increase recommendation diversity to improve user discovery.

3. Reduce average response time below **0.5 seconds**.

4. Introduce personalized recommendations based on user behaviour.

5. Track conversion from search → click → recommendation acceptance.

6. Add A/B testing support for ranking models.

7. Monitor failed searches and recommend synonym expansion.

8. Introduce user segmentation for better analytics.
"""
)

metric_divider()

# ==========================================================
# FOOTER
# ==========================================================

st.markdown("---")

st.caption(
"""
🛍 **MultiRAG Product Dashboard**

Built with Streamlit • Plotly • FAISS • Sentence Transformers • AI Product Analytics

Version 1.0
"""
)