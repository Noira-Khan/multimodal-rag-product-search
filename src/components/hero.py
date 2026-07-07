import streamlit as st


def show_hero():
    left, right = st.columns([2, 1], gap="large")

    with left:
        st.markdown("### 🛍️ AI Fashion Discovery")

        st.title("Find Your Perfect Style with AI")

        st.markdown(
            """
Search products using **Text**, **Image**, or **Voice**.

Our Multimodal AI understands fashion, retrieves visually similar
products, and recommends outfits instantly.
"""
        )

        st.write("")

        c1, c2, c3 = st.columns(3)

        with c1:
            st.success("🤖 AI Powered")

        with c2:
            st.info("🖼 Image Search")

        with c3:
            st.warning("🎤 Voice Search")

        st.write("")

        b1, b2 = st.columns(2)

        with b1:
            if st.button(
                "🛒 Start Shopping",
                width="stretch"
            ):
                st.switch_page("pages/product_search.py")

        with b2:
            if st.button(
                "📷 Image Search",
                width="stretch"
            ):
                st.switch_page("pages/image_search.py")

    with right:
        st.metric("Products", "44K+")
        st.metric("Categories", "7")
        st.metric("Article Types", "143")
        st.metric("Search Modes", "3")

    st.divider()