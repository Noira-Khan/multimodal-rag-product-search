import streamlit as st

from chatbot import ShoppingAssistant


# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="AI Shopping Assistant",
    page_icon="🤖",
    layout="wide",
)


# ==========================================================
# SESSION STATE
# ==========================================================

if "assistant" not in st.session_state:
    st.session_state.assistant = ShoppingAssistant()

if "messages" not in st.session_state:
    st.session_state.messages = []

if "selected_product" not in st.session_state:
    st.session_state.selected_product = None

if "compare_products" not in st.session_state:
    st.session_state.compare_products = []

if "pending_query" not in st.session_state:
    st.session_state.pending_query = None


assistant = st.session_state.assistant


# ==========================================================
# HEADER
# ==========================================================

st.title("🛍️ AI Shopping Assistant")

st.caption(
    """
Ask naturally.

Examples

- Black running shoes under ₹3000
- Formal office shirts
- White sneakers
- Suggest an outfit for interviews
- Show sports shoes for women
"""
)

st.divider()


# ==========================================================
# SIDEBAR
# ==========================================================

with st.sidebar:
    st.title("🤖 Assistant")

    st.success("Gemini 2.5 Flash")
    st.info("Semantic Search + FAISS")
    st.info("Retrieval-Augmented Generation")

    st.metric(
        "Messages",
        assistant.total_messages(),
    )

    if st.button(
        "Clear Conversation",
        use_container_width=True,
    ):
        assistant.clear_history()
        st.session_state.messages = []
        st.session_state.selected_product = None
        st.session_state.compare_products = []
        st.session_state.pending_query = None
        st.rerun()


# ==========================================================
# SUGGESTED PROMPTS
# ==========================================================

st.subheader("Try asking")

col1, col2 = st.columns(2)

with col1:
    if st.button("Black running shoes", key="q1", use_container_width=True):
        st.session_state.pending_query = "Black running shoes"
        st.rerun()

    if st.button("Office shirts", key="q2", use_container_width=True):
        st.session_state.pending_query = "Office shirts"
        st.rerun()

    if st.button("Summer dresses", key="q3", use_container_width=True):
        st.session_state.pending_query = "Summer dresses"
        st.rerun()

with col2:
    if st.button("Laptop backpacks", key="q4", use_container_width=True):
        st.session_state.pending_query = "Laptop backpacks"
        st.rerun()

    if st.button("White sneakers", key="q5", use_container_width=True):
        st.session_state.pending_query = "White sneakers"
        st.rerun()

    if st.button("Sports shoes", key="q6", use_container_width=True):
        st.session_state.pending_query = "Sports shoes"
        st.rerun()

st.divider()


# ==========================================================
# CHAT HISTORY
# ==========================================================

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# ==========================================================
# USER INPUT
# ==========================================================

typed_query = st.chat_input("Ask me anything about fashion...")

user_query = typed_query

if user_query is None and st.session_state.pending_query:
    user_query = st.session_state.pending_query
    st.session_state.pending_query = None


# ==========================================================
# CHAT RESPONSE
# ==========================================================

if user_query:
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_query,
        }
    )

    with st.chat_message("user"):
        st.markdown(user_query)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            result = assistant.chat(user_query)
            answer = result["answer"]

            st.session_state.last_products = result["products"]
            st.session_state.last_explanations = result.get("explanations", [])
            st.session_state.last_result = result

            st.markdown(answer)
            st.markdown("---")
            st.caption("Suggested Questions")

            questions = assistant.suggest_followup_questions()

            for q in questions:
                if st.button(
                    q,
                    key=f"followup_{q}",
                    use_container_width=True,
                ):
                    st.session_state.pending_query = q
                    st.rerun()

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
        }
    )


# ==========================================================
# SELECTED PRODUCT DETAILS
# ==========================================================

if st.session_state.selected_product:
    product = st.session_state.selected_product

    st.divider()
    st.header("Product Details")

    c1, c2 = st.columns([1, 2])

    with c1:
        image_path = product.get("image_path")

        if image_path:
            st.image(
                image_path,
                use_container_width=True,
            )
        else:
            st.info("No image available")

    with c2:
        st.subheader(product.get("product_name", "Unknown Product"))
        st.write(f"Brand: {product.get('brand', 'N/A')}")
        st.write(f"Category: {product.get('category', 'N/A')}")
        st.write(f"Colour: {product.get('colour', 'N/A')}")
        st.write(f"Usage: {product.get('usage', 'N/A')}")

        similarity = product.get("similarity", 0)
        st.write(f"Similarity: {similarity:.2f}")


# ==========================================================
# PRODUCT RECOMMENDATIONS
# ==========================================================

if "last_products" in st.session_state and st.session_state.last_products:
    products = st.session_state.last_products

    st.divider()
    st.subheader("Recommended Products")
    st.caption("Retrieved using Semantic Search + FAISS + RAG")

    for i, product in enumerate(products):
        product_id = product.get("id", i)

        st.markdown("---")

        col1, col2 = st.columns([1, 3])

        with col1:
            image_path = product.get("image_path")

            if image_path:
                st.image(
                    image_path,
                    use_container_width=True,
                )
            else:
                st.info("No image")

        with col2:
            st.subheader(product.get("product_name", "Unknown Product"))

            st.write(f"**Brand:** {product.get('brand', 'N/A')}")
            st.write(f"**Category:** {product.get('category', 'N/A')}")
            st.write(f"**Colour:** {product.get('colour', 'N/A')}")
            st.write(f"**Usage:** {product.get('usage', 'N/A')}")

            similarity = product.get("similarity", 0) * 100

            st.progress(
                min(similarity / 100, 1.0)
            )

            st.caption(
                f"Semantic Similarity: {similarity:.1f}%"
            )

        with st.expander("Product Metadata"):
            st.text(product.get("document", "No metadata available"))

        b1, b2, b3 = st.columns(3)

        with b1:
            if st.button(
                "View",
                key=f"view_{product_id}",
                use_container_width=True,
            ):
                st.session_state.selected_product = product
                st.rerun()

        with b2:
            if st.button(
                "Compare",
                key=f"compare_{product_id}",
                use_container_width=True,
            ):
                if product not in st.session_state.compare_products:
                    st.session_state.compare_products.append(product)
                    st.success("Added for comparison.")

        with b3:
            if st.button(
                "Ask About This",
                key=f"ask_{product_id}",
                use_container_width=True,
            ):
                st.session_state.pending_query = (
                    f"Tell me more about {product.get('product_name', 'this product')}"
                )
                st.rerun()

    st.divider()

    st.subheader("Recommendation Summary")

    summary = st.session_state.last_result["summary"]

    st.info(summary)


# ==========================================================
# COMPARISON LIST
# ==========================================================

if len(st.session_state.compare_products):
    st.divider()
    st.header("Comparison List")

    for item in st.session_state.compare_products:
        st.write("-", item.get("product_name", "Unknown Product"))


# ==========================================================
# ASSISTANT STATUS
# ==========================================================

health = assistant.health()

with st.expander("Assistant Status"):
    st.json(health)


# ==========================================================
# FOOTER
# ==========================================================

st.divider()

st.caption(
    """
Built using

- Gemini
- FAISS
- Sentence Transformers
- Streamlit
- RAG
"""
)
