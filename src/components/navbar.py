import streamlit as st


def show_navbar():
    """Top Navigation"""

    st.markdown(
        """
        <style>

        .logo{
            font-size:32px;
            font-weight:800;
            color:#FF3F6C;
        }

        .logo span{
            color:#6C63FF;
        }

        .tagline{
            color:gray;
            font-size:14px;
            margin-top:-10px;
        }

        </style>
        """,
        unsafe_allow_html=True,
    )

    left, right = st.columns([2, 5])

    # ----------------------------
    # Logo
    # ----------------------------

    with left:

        st.markdown(
            """
            <div class="logo">
            🛍️ Multi<span>RAG</span>
            </div>

            <div class="tagline">
            AI Fashion Search Platform
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ----------------------------
    # Navigation
    # ----------------------------

    with right:

        c1, c2, c3, c4, c5 = st.columns(5)

        c1.button("👕 Men", use_container_width=True)

        c2.button("👗 Women", use_container_width=True)

        c3.button("👦 Kids", use_container_width=True)

        c4.button("💄 Beauty", use_container_width=True)

        c5.button("🎒 Accessories", use_container_width=True)

    st.write("")

    st.text_input(
        "",
        placeholder="🔍 Search for shirts, jeans, sneakers, handbags...",
        key="search_bar",
    )

    st.divider()