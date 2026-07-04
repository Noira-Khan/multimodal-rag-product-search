"""
==========================================================
DASHBOARD COMPONENTS
Multimodal Retail Assistant (Myntra AI)

Part 1 / 4

Contains
--------
✓ Imports
✓ Dashboard Header
✓ Section Header
✓ Dashboard Container

Upcoming
--------
Part 2
✓ KPI Cards
✓ KPI Grid

Part 3
✓ Plotly Charts

Part 4
✓ AI Insight Cards
✓ Summary Cards
==========================================================
"""

import streamlit as st


# ==========================================================
# Dashboard Header
# ==========================================================

def dashboard_header(
    title: str,
    subtitle: str,
):

    st.markdown(
        f"""
<div style="
padding:32px;
border-radius:22px;
background:linear-gradient(
135deg,
#312E81,
#2563EB,
#06B6D4
);
margin-bottom:30px;
box-shadow:0 12px 28px rgba(0,0,0,.20);
">

<h1 style="
margin:0;
font-size:42px;
font-weight:700;
color:white;
">

📊 {title}

</h1>

<p style="
margin-top:12px;
font-size:18px;
color:white;
">

{subtitle}

</p>

</div>
""",
        unsafe_allow_html=True
    )


# ==========================================================
# Section Header
# ==========================================================

def section_header(
    title: str,
    icon="✨"
):

    st.markdown(
        f"""
<div style="margin-top:30px;margin-bottom:18px;">

<h2 style="
font-size:28px;
font-weight:700;
color:#111827;
">

{icon} {title}

</h2>

</div>
""",
        unsafe_allow_html=True
    )


# ==========================================================
# Dashboard Container
# ==========================================================

def dashboard_container():

    st.markdown(
        """
<style>

.block-container{

padding-top:2rem;
padding-bottom:2rem;
padding-left:3rem;
padding-right:3rem;

}

</style>
""",
        unsafe_allow_html=True
    )

def kpi_card(

    title: str,

    value,

    delta=None,

    icon="📊",

):

    delta_html = ""

    # ----------------------------------------------------------
    # Format Numbers
    # ----------------------------------------------------------

    if isinstance(value, (int, float)):

        display_value = f"{value:,}"

    else:

        display_value = str(value)

    if delta is not None:

        delta_html = f"""
<p style="
margin-top:12px;
margin-bottom:0;
font-size:15px;
font-weight:600;
color:#10B981;
">

▲ {delta}

</p>
"""

    st.markdown(

        f"""
<div style="
background:#F8FAFC;
padding:24px;
border-radius:20px;
box-shadow:0 10px 30px rgba(15,23,42,.08);
border:1px solid rgba(148,163,184,.18);
min-height:170px;
">

<div style="
font-size:42px;
">

{icon}

</div>

<div style="
margin-top:15px;
font-size:13px;
font-weight:600;
letter-spacing:1px;
text-transform:uppercase;
color:#64748B;
">

{title}

</div>

<div style="
margin-top:12px;
font-size:38px;
font-weight:700;
color:#111827;
white-space:nowrap;
">

{display_value}

</div>

{delta_html}

</div>
""",

        unsafe_allow_html=True

    )


# ==========================================================
# KPI Grid
# ==========================================================

def kpi_grid(
    metrics,
):

    columns = st.columns(len(metrics))

    for column, metric in zip(columns, metrics):

        with column:

            kpi_card(

                title=metric["title"],

                value=metric["value"],

                delta=metric.get("delta"),

                icon=metric.get("icon", "📊")

            )


# ==========================================================
# Metric Divider
# ==========================================================

def metric_divider():

    st.markdown("<br>", unsafe_allow_html=True)

# ==========================================================
# Imports for Charts
# ==========================================================

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


# ==========================================================
# Common Plotly Theme
# ==========================================================

def dashboard_layout(fig):
    """
    Apply a consistent dashboard theme.
    """

    fig.update_layout(

        template="plotly_white",

        paper_bgcolor="rgba(0,0,0,0)",

        plot_bgcolor="rgba(0,0,0,0)",

        font=dict(

            family="Segoe UI",

            size=14,

            color="#374151"

        ),

        

        margin=dict(

            l=20,
            r=20,
            t=60,
            b=20

        ),

        legend=dict(

            orientation="h",

            y=1.05

        )

    )

    return fig


# ==========================================================
# Vertical Bar Chart
# ==========================================================

def bar_chart(

    data,

    x,

    y,

    title,

    color="#2563EB"

):

    fig = px.bar(

        data,

        x=x,

        y=y,

        text=y,

        title=title,

        color_discrete_sequence=[color]

    )

    fig.update_traces(

        textposition="outside",

        marker_line_width=0

    )

    st.plotly_chart(

        dashboard_layout(fig),

        use_container_width=True

    )


# ==========================================================
# Horizontal Ranking Chart
# ==========================================================

def horizontal_bar_chart(
    data,
    x,
    y,
    title=None,
    color="#10B981"
):

    fig = px.bar(
        data_frame=data,
        x=x,
        y=y,
        orientation="h",
        text=x,
        color_discrete_sequence=[color],
    )

    # Remove title completely if not provided
    if title:
        fig.update_layout(title=title)

    fig.update_traces(
        textposition="outside",
        marker_line_width=0,
    )

    fig.update_layout(
        height=420,
        showlegend=False,
        xaxis_title="Count",
        yaxis_title="",
        margin=dict(l=20, r=20, t=20, b=20),
    )

    st.plotly_chart(
        dashboard_layout(fig),
        width="stretch",
    )

# ==========================================================
# Trend Line Chart
# ==========================================================

def line_chart(

    data,

    x,

    y,

    title,

    color="#F97316"

):

    fig = px.line(

        data,

        x=x,

        y=y,

        markers=True,

        title=title

    )

    fig.update_traces(

        line_width=4,

        marker_size=9,

        line_color=color

    )

    st.plotly_chart(

        dashboard_layout(fig),

        use_container_width=True

    )


# ==========================================================
# Donut Chart
# ==========================================================

def donut_chart(

    data,

    names,

    values,

    title

):

    fig = px.pie(

        data,

        names=names,

        values=values,

        hole=.65,

        title=title

    )

    fig.update_traces(

        textposition="inside",

        textinfo="percent+label"

    )

    st.plotly_chart(

        dashboard_layout(fig),

        use_container_width=True

    )


# ==========================================================
# Gauge KPI Chart
# ==========================================================

def gauge_chart(

    value,

    title,

    maximum=100

):

    fig = go.Figure(

        go.Indicator(

            mode="gauge+number",

            value=value,

            title={"text": title},

            gauge={

                "axis": {

                    "range": [0, maximum]

                },

                "bar": {

                    "color": "#2563EB"

                },

                "steps": [

                    {

                        "range": [0, 50],

                        "color": "#FEE2E2"

                    },

                    {

                        "range": [50, 80],

                        "color": "#FEF3C7"

                    },

                    {

                        "range": [80, maximum],

                        "color": "#DCFCE7"

                    }

                ]

            }

        )

    )

    st.plotly_chart(

        dashboard_layout(fig),

        use_container_width=True

    )

# ==========================================================
# AI Insight Card
# ==========================================================

def insight_card(

    title: str,

    insight: str,

    icon="💡",

):

    st.markdown(

        f"""
<div style="
background:linear-gradient(135deg,#EFF6FF,#DBEAFE);
padding:22px;
border-radius:18px;
border-left:6px solid #2563EB;
margin-top:15px;
margin-bottom:15px;
box-shadow:0 6px 18px rgba(0,0,0,.08);
">

<h3 style="
margin:0;
color:#1E3A8A;
">

{icon} {title}

</h3>

<p style="
margin-top:12px;
font-size:16px;
color:#374151;
line-height:1.7;
">

{insight}

</p>

</div>
""",

        unsafe_allow_html=True

    )


# ==========================================================
# Executive Summary Card
# ==========================================================

def summary_card(

    title,

    summary,

):

    st.markdown(

        f"""
<div style="
background:white;
padding:25px;
border-radius:18px;
border:1px solid #E5E7EB;
box-shadow:0 8px 20px rgba(0,0,0,.08);
margin-top:15px;
">

<h3 style="
margin:0;
color:#111827;
">

📋 {title}

</h3>

<hr>

<p style="
font-size:16px;
line-height:1.8;
color:#4B5563;
">

{summary}

</p>

</div>
""",

        unsafe_allow_html=True

    )


# ==========================================================
# Status Badge
# ==========================================================

def status_badge(

    text,

    color="#10B981",

):

    st.markdown(

        f"""
<span style="
background:{color};
padding:8px 16px;
border-radius:20px;
color:white;
font-weight:600;
font-size:14px;
">

{text}

</span>
""",

        unsafe_allow_html=True

    )


# ==========================================================
# Empty State
# ==========================================================

def empty_state(

    message="No data available.",

):

    st.info(

        "📭 " + message

    )


# ==========================================================
# Dashboard Footer
# ==========================================================

def dashboard_footer():

    st.markdown(

        """
<br><br>

<hr>

<center>

<p style="color:gray;font-size:14px;">

Built with ❤️ using
Streamlit • Plotly • Gemini AI • RAG • FAISS

</p>

</center>

""",

        unsafe_allow_html=True

    )


# ==========================================================
# Test Dashboard
# ==========================================================

if __name__ == "__main__":

    dashboard_container()

    dashboard_header(

        "AI Product Dashboard",

        "Executive analytics for the Multimodal Retail Assistant."

    )

    section_header(

        "Business KPIs",

        "📈"

    )

    kpi_grid(

        [

            {

                "title":"Searches",

                "value":"12,540",

                "delta":"+18%",

                "icon":"🔍"

            },

            {

                "title":"CTR",

                "value":"81%",

                "delta":"+5%",

                "icon":"🎯"

            },

            {

                "title":"North Star",

                "value":"87%",

                "delta":"+4%",

                "icon":"⭐"

            },

            {

                "title":"AI Chats",

                "value":"2,431",

                "delta":"+24%",

                "icon":"🤖"

            }

        ]

    )

    insight_card(

        "AI Insight",

        "Searches for running shoes increased by 23% this week. Nike products generated the highest engagement and recommendation acceptance."

    )

    summary_card(

        "Executive Summary",

        "Customer engagement is increasing steadily. Recommendation acceptance remains above the target threshold, while search success rate exceeds 90%. Product discovery continues to improve with AI-powered recommendations."

    )

    status_badge(

        "System Healthy"

    )

    dashboard_footer()

