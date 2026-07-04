import streamlit as st


def show_sidebar():

    with st.sidebar:

        st.markdown("# 🛍️ MultiRAG")
        st.caption("AI Fashion Search Engine")

        st.divider()

        # ============================
        # Navigation
        # ============================

        if st.button("🏠 Home", use_container_width=True):
            st.switch_page("app.py")

        if st.button("🔍 Product Search", use_container_width=True):
            st.switch_page("pages/1_product_search.py")

        if st.button("🤖 AI Assistance", use_container_width=True):
            st.switch_page("pages/2_AI_assistance.py")

        if st.button("✨ Recommendations", use_container_width=True):
            st.switch_page("pages/5_recommendations.py")

        if st.button("⚖️ Product Comparison", use_container_width=True):
            st.switch_page("pages/6_product_comparison.py")

        if st.button("📊 Analytics", use_container_width=True):
            st.switch_page("pages/7_analytics.py")

        if st.button("👥 Customer Insights", use_container_width=True):
            st.switch_page("pages/8_customer_insights.py")

        if st.button("🗺️ Roadmap", use_container_width=True):
            st.switch_page("pages/9_roadmap.py")

        if st.button("ℹ️ About", use_container_width=True):
            st.switch_page("pages/10_about.py")

        st.divider()

        st.subheader("✨ AI Features")

        st.write("✔ Semantic Search")
        st.write("✔ AI Shopping Assistant")
        st.write("✔ Product Recommendations")
        st.write("✔ Product Comparison")
        st.write("✔ Analytics Dashboard")
        st.write("✔ Customer Insights")

        st.divider()

        st.info(
            """
### Dataset

📦 Fashion Products

👕 44K+ Products

🤖 AI Powered

🧠 Multimodal Retail Assistant
"""
        )