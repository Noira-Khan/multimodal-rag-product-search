from pathlib import Path
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[2]
CSV_PATH = ROOT / "data" / "styles_cleaned.csv"

@st.cache_data
def load_data():
    return pd.read_csv(CSV_PATH)


def show_metrics():

    df = load_data()

    total_products = len(df)
    total_categories = df["masterCategory"].nunique()
    total_subcategories = df["subCategory"].nunique()
    total_article_types = df["articleType"].nunique()

    st.markdown("## 📊 Fashion Dataset")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Products", f"{total_products:,}")
    c2.metric("Categories", total_categories)
    c3.metric("Sub Categories", total_subcategories)
    c4.metric("Article Types", total_article_types)

    st.divider()

    left, right = st.columns(2)

    with left:
        st.info(
            f"### Top Category\n\n{df['masterCategory'].mode()[0]}"
        )

    with right:
        st.info(
            f"### Most Common Product\n\n{df['articleType'].mode()[0]}"
        )