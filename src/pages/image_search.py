"""
==========================================================
IMAGE SEARCH PAGE
Multimodal Retail Assistant (Myntra AI)
==========================================================

Features

✔ AI Visual Search

✔ Gemini Vision

✔ Image Understanding

✔ Similar Product Retrieval

✔ FAISS + RAG

✔ AI Explanations

Author:
Noira Khan

==========================================================
"""

import json
from pathlib import Path

import google.generativeai as genai
import streamlit as st
from PIL import Image

from analytics_service import Analytics
from components.navbar import show_navbar
from rag_engine import RAGEngine

# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------

st.set_page_config(
    page_title="AI Visual Search",
    page_icon="📷",
    layout="wide"
)

# ---------------------------------------------------------
# LOAD CSS
# ---------------------------------------------------------

ROOT = Path(__file__).resolve().parents[1]

CSS = ROOT / "css" / "style.css"

if CSS.exists():

    with open(CSS, "r", encoding="utf-8") as f:

        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True,
        )

# ---------------------------------------------------------
# GEMINI
# ---------------------------------------------------------

genai.configure(
    api_key=st.secrets["GOOGLE_API_KEY"]
)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)

# ---------------------------------------------------------
# RAG ENGINE
# ---------------------------------------------------------

if "rag_engine" not in st.session_state:

    st.session_state.rag_engine = RAGEngine()

rag = st.session_state.rag_engine

analytics = Analytics()

# ---------------------------------------------------------
# NAVBAR
# ---------------------------------------------------------

show_navbar()

# ---------------------------------------------------------
# TITLE
# ---------------------------------------------------------

st.title("📷 AI Visual Search")

st.caption(
    "Upload a fashion image and discover visually similar products using AI."
)

st.divider()

# ---------------------------------------------------------
# IMAGE ANALYSIS
# ---------------------------------------------------------

def analyze_image(image):

    prompt = """
You are an expert Fashion AI.

Look carefully at the uploaded fashion image.

Return ONLY valid JSON.

{

"category":"",

"gender":"",

"article_type":"",

"primary_color":"",

"secondary_color":"",

"material":"",

"pattern":"",

"style":"",

"occasion":"",

"description":"",

"confidence":""

}

Rules:

Do not explain.

Return JSON only.

No markdown.
"""

    response = model.generate_content(
        [prompt, image]
    )

    text = response.text.strip()

    text = (
        text
        .replace("```json", "")
        .replace("```", "")
        .strip()
    )

    return json.loads(text)

# ---------------------------------------------------------
# IMAGE UPLOAD
# ---------------------------------------------------------

uploaded_file = st.file_uploader(

    "Upload Image",

    type=[
        "jpg",
        "jpeg",
        "png"
    ]

)

# ---------------------------------------------------------
# WAITING SCREEN
# ---------------------------------------------------------

if uploaded_file is None:

    st.info(

        "Upload a clothing, footwear, handbag or accessory image."

    )

    st.stop()

# ---------------------------------------------------------
# OPEN IMAGE
# ---------------------------------------------------------

image = Image.open(uploaded_file)

left, right = st.columns([1, 1])

with left:

    st.subheader("📷 Uploaded Image")

    st.image(

        image,

        use_container_width=True

    )

with right:

    st.subheader("🤖 AI Vision")

    st.info(

        """
Gemini will identify

• Category

• Colors

• Material

• Style

• Occasion

before searching similar products.
"""

    )

# ---------------------------------------------------------
# ANALYZE BUTTON
# ---------------------------------------------------------

analyze = st.button(

    "✨ Analyze Image",
    key="analyze_image_btn",

    use_container_width=True

)




# ---------------------------------------------------------
# SESSION STATE
# ---------------------------------------------------------

if "image_analysis" not in st.session_state:

    st.session_state.image_analysis = None

# ---------------------------------------------------------
# RUN GEMINI
# ---------------------------------------------------------

if analyze:

    with st.spinner(

        "Gemini is analyzing your image..."

    ):

        try:

            result = analyze_image(image)

            st.session_state.image_analysis = result

            st.success(

                "Image analyzed successfully."

            )

        except Exception as e:

            st.error(

                f"Gemini Error\n\n{e}"

            )

            st.stop()

# ---------------------------------------------------------
# SHOW ANALYSIS
# ---------------------------------------------------------

if st.session_state.image_analysis is not None:

    result = st.session_state.image_analysis

    st.divider()

    st.subheader("🤖 AI Analysis")

    col1, col2 = st.columns(2)

    with col1:

        st.metric(

            "Category",

            result["category"]

        )

        st.metric(

            "Gender",

            result["gender"]

        )

        st.metric(

            "Article Type",

            result["article_type"]

        )

        st.metric(

            "Material",

            result["material"]

        )

        st.metric(

            "Pattern",

            result["pattern"]

        )

    with col2:

        st.metric(

            "Primary Color",

            result["primary_color"]

        )

        st.metric(

            "Secondary Color",

            result["secondary_color"]

        )

        st.metric(

            "Style",

            result["style"]

        )

        st.metric(

            "Occasion",

            result["occasion"]

        )

        st.metric(

            "Confidence",

            result["confidence"]

        )

    st.divider()

    st.subheader("📝 AI Description")

    st.info(

        result["description"]

    )

    st.divider()

    st.success(

        "Ready to search similar products."

    )


# ---------------------------------------------------------
# SEARCH SIMILAR PRODUCTS
# ---------------------------------------------------------

search_products = st.button(

    "🛍 Find Similar Products",

    use_container_width=True

)

# ---------------------------------------------------------
# SESSION STATE
# ---------------------------------------------------------

if "image_pipeline" not in st.session_state:

    st.session_state.image_pipeline = None

# ---------------------------------------------------------
# SEARCH USING RAG
# ---------------------------------------------------------

if search_products:

    with st.spinner(

        "Searching visually similar products..."

    ):

        try:

            description = result["description"]

            pipeline = rag.search_pipeline(

                description,

                10

            )

            st.session_state.image_pipeline = pipeline

            analytics.log_search(

                query=description,

                results=len(pipeline["results"]),

                response_time=0

            )

            st.success(

                f"{len(pipeline['results'])} similar products found."

            )

        except Exception as e:

            st.error(

                f"Search Error\n\n{e}"

            )

            st.stop()

# ---------------------------------------------------------
# DISPLAY PRODUCTS
# ---------------------------------------------------------

if st.session_state.image_pipeline is not None:

    pipeline = st.session_state.image_pipeline

    st.divider()

    st.subheader("🛍 Similar Products")

    st.caption(

        "Products retrieved using AI Vision + Vector Search."

    )

    # -----------------------------------------------------

    for product in pipeline["results"]:

        left, right = st.columns(

            [1,3]

        )

        with left:

            st.image(

                product["image_path"],

                use_container_width=True

            )

        with right:

            st.subheader(

                product["product_name"]

            )

            st.write(

                f"**Brand:** {product['brand']}"

            )

            st.write(

                f"**Category:** {product['category']}"

            )

            st.metric(

                "Similarity",

                f"{product['similarity']:.2f}"

            )

            st.write("### Why Recommended")

            for reason in product["explanation"]:

                st.write(

                    "✅",

                    reason

                )

            c1, c2, c3 = st.columns(3)

            with c1:

                st.button(

                    "👀 View",

                    key=f"img_view_{product['id']}"

                )

            with c2:

                st.button(

                    "⚖ Compare",

                    key=f"img_compare_{product['id']}"

                )

            with c3:

                st.button(

                    "🤖 Ask AI",

                    key=f"img_ai_{product['id']}"

                )

        st.divider()

# ---------------------------------------------------------
# AI PRODUCT INSIGHTS
# ---------------------------------------------------------

st.divider()

st.subheader("🧠 AI Product Insights")

if st.session_state.image_analysis is not None:
    result = st.session_state.image_analysis
    description = result["description"]
else:
    st.stop()

try:

    insight_prompt = f"""
You are a fashion shopping assistant.

A customer uploaded an image described as:

{description}

Give:

1. Overall fashion style
2. Best occasions
3. Matching colors
4. Outfit suggestion
5. One shopping recommendation

Keep each point short.
"""

    insight = model.generate_content(insight_prompt)

    st.success(insight.text)

except Exception:

    st.info("AI Insights unavailable.")


# ---------------------------------------------------------
# SEARCH SUMMARY
# ---------------------------------------------------------

if st.session_state.image_pipeline is not None:

    pipeline = st.session_state.image_pipeline

    st.divider()

    st.subheader("📊 Search Summary")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric(
            "Products Retrieved",
            len(pipeline["results"])
        )

    with c2:
        avg_similarity = (
            sum(p["similarity"] for p in pipeline["results"])
            / len(pipeline["results"])
        )

        st.metric(
            "Average Similarity",
            f"{avg_similarity:.2f}"
        )

    with c3:
        st.metric(
            "Search Method",
            "Gemini + FAISS"
        )
# ---------------------------------------------------------
# AI PIPELINE
# ---------------------------------------------------------

st.divider()

with st.expander("⚙️ AI Search Pipeline", expanded=False):

    st.markdown("""

### Image Search Workflow

📷 Image Upload

⬇

🤖 Gemini Vision Analysis

⬇

📝 Structured Fashion Description

⬇

🧠 Vector Embedding

⬇

📚 FAISS Vector Search

⬇

🛍 Similar Product Retrieval

⬇

✨ AI Explanation Generation

""")

# ---------------------------------------------------------
# WHY THIS IS RECOMMENDED
# ---------------------------------------------------------

st.divider()

st.subheader("💡 Why AI chose these products")

st.info(
"""
The uploaded image was converted into a structured fashion description using Gemini Vision.

Instead of matching raw pixels, the AI understands:

• Product category

• Material

• Colors

• Style

• Occasion

That description is converted into semantic embeddings and matched against the FAISS vector database to retrieve the most relevant products.
"""
)

# ---------------------------------------------------------
# SHOPPING TIPS
# ---------------------------------------------------------

st.divider()

st.subheader("🛒 AI Shopping Tips")

tips = [

"Choose products with high similarity scores.",

"Compare multiple recommendations before purchasing.",

"Use Product Search if you're looking for a specific brand.",

"Image Search works best with clear product photos."

]

for tip in tips:

    st.write("✅", tip)

# ---------------------------------------------------------
# FOOTER METRICS
# ---------------------------------------------------------

st.divider()

m1, m2, m3, m4 = st.columns(4)

with m1:

    st.metric(
        "Vision Model",
        "Gemini 2.5"
    )

with m2:

    st.metric(
        "Search Engine",
        "FAISS"
    )

with m3:

    st.metric(
        "AI Retrieval",
        "RAG"
    )

with m4:

    st.metric(
        "Recommendation",
        "Semantic"
    )