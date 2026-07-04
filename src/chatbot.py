from __future__ import annotations

import logging
from typing import Dict, List

from llm import GeminiClient

from config import GOOGLE_API_KEY, MODEL_NAME, MAX_HISTORY
from prompts import build_chat_prompt
from rag_engine import RAGEngine


logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s | %(message)s",
)

logger = logging.getLogger(__name__)


class ShoppingAssistant:
    def __init__(self):
        logger.info("Initializing Shopping Assistant...")
        self.rag = RAGEngine()
        self.history: List[Dict[str, str]] = []
        self.llm = GeminiClient()
        logger.info("Shopping Assistant Ready.")

    

    def add_message(self, role: str, content: str):
        self.history.append(
            {
                "role": role,
                "content": content,
            }
        )

        if len(self.history) > MAX_HISTORY:
            self.history = self.history[-MAX_HISTORY:]

    def clear_history(self):
        self.history = []
        logger.info("Conversation Cleared.")

    def reset(self):
        self.clear_history()

    def get_history(self):
        return self.history

    def last_message(self):
        if len(self.history) == 0:
            return None

        return self.history[-1]

    def total_messages(self):
        return len(self.history)

    def show_history(self):
        print()
        print("=" * 70)
        print("Conversation History")
        print("=" * 70)

        for message in self.history:
            print()
            print(message["role"].upper())
            print(message["content"])

        print()

    def retrieve_products(self, query: str, top_k: int = 5):
        logger.info(f"Searching products for: {query}")

        pipeline = self.rag.search_pipeline(
            query=query,
            top_k=top_k,
        )

        return pipeline

    def build_prompt(self, query: str, pipeline: dict):
        context = pipeline["context"]
        history = self.get_history()

        prompt = build_chat_prompt(
            query=query,
            context=context,
            history=history,
        )

        return prompt

    def generate_response(self, prompt: str):
        logger.info("Generating Gemini response...")

        return self.llm.generate(
        prompt
                )
    

    def explain_products(self, pipeline: dict):
        return pipeline["results"]

    def total_products(self, pipeline: dict):
        return len(pipeline["results"])

    def recommendation_summary(self, pipeline: dict):
        products = pipeline["results"]

        if not products:
            return "No products found."

        names = []

        for product in products:
            names.append(product["product_name"])

        return ", ".join(names)

    def average_similarity(self, pipeline: dict):
        products = pipeline["results"]

        if len(products) == 0:
            return 0

        total = 0

        for product in products:
            total += product["similarity"]

        return round(total / len(products), 3)

    def search_statistics(self, pipeline: dict):
        return {
            "products_found": self.total_products(pipeline),
            "average_similarity": self.average_similarity(pipeline),
        }

    def health(self):
        return {
            "model": MODEL_NAME,
            "messages": self.total_messages(),
            "rag_loaded": self.rag is not None,
            "llm_loaded": self.llm is not None,
        }
    

    def export_chat(self):
        return {
            "history": self.get_history(),
        }

    def suggest_followup_questions(self):
        return [
            "Show similar products",
            "Show cheaper alternatives",
            "Only black colour",
            "Only Nike",
            "Recommend premium brands",
            "Compare these products",
        ]

    def chat(self, query: str, top_k: int = 5):
        logger.info(f"User Query: {query}")

        self.add_message(
            role="user",
            content=query,
        )

        pipeline = self.retrieve_products(
            query=query,
            top_k=top_k,
        )

        prompt = self.build_prompt(
            query=query,
            pipeline=pipeline,
        )

        answer = self.generate_response(prompt)

        self.add_message(
            role="assistant",
            content=answer,
        )

        return {
            "answer": answer,
            "products": pipeline["results"],
            "statistics": self.search_statistics(pipeline),
            "summary": self.recommendation_summary(pipeline),
            "followups": self.suggest_followup_questions(),
            "history": self.get_history(),
        }

    def ask(self, query: str):
        return self.chat(query)

    def restart(self):
        self.clear_history()
        logger.info("Assistant restarted.")

    def status(self):
        return {
            "messages": self.total_messages(),
            "history_loaded": len(self.history),
            "rag_ready": self.rag is not None,
            "llm_ready": self.model is not None,
        }

    def last_response(self):
        history = self.get_history()

        for message in reversed(history):
            if message["role"] == "assistant":
                return message["content"]

        return None

    def last_user_message(self):
        history = self.get_history()

        for message in reversed(history):
            if message["role"] == "user":
                return message["content"]

        return None


def print_chat_result(result):
    print("\n" + "=" * 70)
    print("AI Shopping Assistant")
    print("=" * 70)

    print("\nAnswer\n")
    print(result["answer"])

    print("\n" + "-" * 70)
    print("Recommended Products")
    print("-" * 70)

    products = result["products"]

    if len(products) == 0:
        print("No matching products found.")
    else:
        for i, product in enumerate(products, start=1):
            print()
            print(f"{i}. {product['product_name']}")
            print("Similarity:", round(product["similarity"], 3))

    print("\n" + "-" * 70)
    print("Summary")
    print(result["summary"])

    print("\n" + "-" * 70)
    print("Statistics")

    for key, value in result["statistics"].items():
        print(f"{key}: {value}")

    print("\n" + "-" * 70)
    print("Suggested Follow-up Questions")

    for question in result["followups"]:
        print("-", question)

    print("=" * 70)


def console_chat():
    bot = ShoppingAssistant()

    print()
    print("=" * 70)
    print("Multimodal Retail Assistant")
    print("=" * 70)
    print()
    print("Type 'exit' anytime to quit.")

    while True:
        print()

        query = input("You : ")

        if query.lower() in ["exit", "quit", "bye"]:
            break

        result = bot.chat(query)

        print_chat_result(result)

    print()
    print("=" * 70)
    print("Conversation Ended")
    print("=" * 70)
    print()
    print("Total Messages:", bot.total_messages())
    print()

    bot.show_history()


if __name__ == "__main__":
    console_chat()
    