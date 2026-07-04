"""
==========================================================
PROMPTS - PART 1 OF 3
Multimodal Retail Assistant (Myntra AI)
==========================================================

Module:
    prompts.py

Current Part:
    Part 1 / 3

Status:
    Complete

Responsibilities
----------------
- System Prompt
- User Prompt
- Product Context Prompt
- Conversation Prompt
- Follow-up Prompt

Author:
    Noira Khan

Project:
    Multimodal Retail Assistant (Myntra AI)
==========================================================
"""


# ==========================================================
# SYSTEM PROMPT
# ==========================================================

def build_system_prompt():
    """
    Core behaviour of the AI Shopping Assistant.
    """

    return """
You are an intelligent AI Shopping Assistant for an online
fashion marketplace.

Your goals are:

- Help customers discover products.

- Recommend relevant products.

- Explain recommendations.

- Answer product-related questions.

- Never invent products.

- Use ONLY the provided product context.

- If the answer is unavailable,
  politely say that it was not found
  in the catalogue.

Your personality:

- Friendly

- Professional

- Fashion knowledgeable

- Helpful

- Concise

Always recommend products that best match
the customer's intent.

Always explain WHY a product is recommended.
"""


# ==========================================================
# PRODUCT CONTEXT
# ==========================================================

def build_product_context(context: str):
    """
    Inject retrieved RAG context.
    """

    return f"""
Available Product Information

--------------------------------

{context}

--------------------------------

Only use the above information when answering.
"""


# ==========================================================
# USER PROMPT
# ==========================================================

def build_user_prompt(query: str):
    """
    Format the customer query.
    """

    return f"""
Customer Question

{query}

Answer professionally.

Recommend products if appropriate.

Do not hallucinate.
"""


# ==========================================================
# CONVERSATION HISTORY
# ==========================================================

def build_history_prompt(history):
    """
    Build conversation memory.
    """

    if not history:
        return ""

    conversation = []

    for message in history:
        role = message["role"].upper()
        content = message["content"]

        conversation.append(f"{role}: {content}")

    return "\n".join(conversation)


# ==========================================================
# FOLLOW-UP QUESTIONS
# ==========================================================

def build_followup_prompt():
    """
    Suggest additional questions.
    """

    return """
Suggest three relevant follow-up questions.

Examples

- Show similar products

- Compare with another product

- Show cheaper alternatives

Return only the questions.
"""


# ==========================================================
# FINAL PROMPT
# ==========================================================

def build_chat_prompt(
    query: str,
    context: str,
    history: list,
):
    """
    Build the final complete prompt.
    """

    prompt = f"""
{build_system_prompt()}

==============================

Conversation History

{build_history_prompt(history)}

==============================

Product Context

{build_product_context(context)}

==============================

Customer Question

{build_user_prompt(query)}

==============================
"""

    return prompt


# ==========================================================
# TESTING
# ==========================================================

if __name__ == "__main__":

    sample_history = [
        {
            "role": "user",
            "content": "Suggest running shoes",
        },
        {
            "role": "assistant",
            "content": "Here are five recommendations.",
        },
    ]

    prompt = build_chat_prompt(
        query="Show black Nike shoes",
        context="""
Nike Black Running Shoes
Sports Shoes
Black
Men
""",
        history=sample_history,
    )

    print(prompt)

    