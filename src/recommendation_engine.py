"""
==========================================================
RECOMMENDATION ENGINE - PART 1 OF 4
Multimodal Retail Assistant (Myntra AI)
==========================================================

Module:
    recommendation_engine.py

Current Part:
    Part 1 / 4

Status:
    Complete

Responsibilities
----------------
- Load Product Metadata
- Initialize Recommendation Engine
- Reuse Existing RAG Engine
- Product Lookup
- Utility Functions

Upcoming Parts
--------------
Part 2
- Similar Products
- Content-Based Recommendations
- Top-K Recommendations

Part 3
- Customers Also Bought
- Personalized Recommendations
- Trending Products

Part 4
- AI Product Comparison
- Recommendation Pipeline
- Explainable AI

Author:
    Noira Khan

Project:
    Multimodal Retail Assistant (Myntra AI)
==========================================================
"""

from __future__ import annotations

import logging
from typing import Dict
from typing import Optional

from llm import GeminiClient
from rag_engine import RAGEngine


# ==========================================================
# Logging
# ==========================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s | %(message)s",
)

logger = logging.getLogger(__name__)


# ==========================================================
# Recommendation Engine
# ==========================================================


class RecommendationEngine:
    """
    Recommendation Engine

    Responsibilities:
    - Product lookup
    - Similar products
    - Product comparison
    - Personalized recommendations
    - AI recommendation pipeline
    """

    # ------------------------------------------------------

    def __init__(self):
        logger.info("Initializing Recommendation Engine...")

        # Reuse the existing RAG Engine.
        self.rag = RAGEngine()

        # Metadata already loaded inside RAG.
        self.products = self.rag.products
        self.llm = GeminiClient()

        logger.info("Recommendation Engine Ready.")

    # ------------------------------------------------------

    def total_products(self):
        """
        Total products in catalogue.
        """
        return len(self.products)

    # ------------------------------------------------------

    def get_product(self, product_id: int) -> Optional[Dict]:
        """
        Find product using ID.
        """
        for product in self.products:
            if product["id"] == product_id:
                return product

        return None

    # ------------------------------------------------------

    def get_product_by_name(self, product_name: str) -> Optional[Dict]:
        """
        Find product by name.
        """
        product_name = product_name.lower()

        for product in self.products:
            if product_name in product["product_name"].lower():
                return product

        return None

    # ------------------------------------------------------

    def product_exists(self, product_name: str):
        """
        Check if product exists.
        """
        return self.get_product_by_name(product_name) is not None

    # ------------------------------------------------------

    def all_products(self):
        """
        Return complete catalogue.
        """
        return self.products

    # ------------------------------------------------------

    def product_names(self):
        """
        Return all product names.
        """
        names = []

        for product in self.products:
            names.append(product["product_name"])

        return names

    # ------------------------------------------------------

    def search_product(self, query: str):
        """
        Search using existing RAG pipeline.

        Returns the highest-ranked product.
        """
        pipeline = self.rag.search_pipeline(
            query=query,
            top_k=1,
        )

        results = pipeline["results"]

        if len(results) == 0:
            return None

        return results[0]

    # ------------------------------------------------------

    def health(self):
        """
        Engine status.
        """
        return {
            "engine": "Recommendation Engine",
            "products_loaded": self.total_products(),
            "rag_loaded": self.rag is not None,
        }

    # ------------------------------------------------------

    def similar_products(
        self,
        query: str,
        top_k: int = 5,
    ):
        """
        Recommend products similar to a search query.

        Reuses the existing RAG search pipeline.
        """
        pipeline = self.rag.search_pipeline(
            query=query,
            top_k=top_k,
        )

        return pipeline["results"]

    # ------------------------------------------------------

    def recommend_from_product(
        self,
        product_name: str,
        top_k: int = 5,
    ):
        """
        Recommend products similar to an existing product.
        """
        product = self.get_product_by_name(product_name)

        if product is None:
            return []

        return self.similar_products(
            product["product_name"],
            top_k=top_k,
        )

    # ------------------------------------------------------

    def recommend_from_query(
        self,
        query: str,
        top_k: int = 5,
    ):
        """
        Public recommendation method.
        """
        return self.similar_products(
            query=query,
            top_k=top_k,
        )

    # ------------------------------------------------------

    def top_recommendations(
        self,
        query: str,
        top_k: int = 5,
    ):
        """
        Alias for recommendation API.
        """
        return self.recommend_from_query(
            query=query,
            top_k=top_k,
        )

    # ------------------------------------------------------

    def print_recommendations(
        self,
        query: str,
        top_k: int = 5,
    ):
        """
        Print recommendations in the console.
        """
        recommendations = self.top_recommendations(
            query=query,
            top_k=top_k,
        )

        print()
        print("=" * 70)
        print("Recommendations")
        print("=" * 70)

        if len(recommendations) == 0:
            print("No products found.")
            return

        for i, product in enumerate(recommendations, start=1):
            print()
            print(f"{i}.")
            print("Name :", product["product_name"])

            if "score" in product:
                print(
                    "Similarity :",
                    round(product["score"], 4),
                )

            print("Image :", product["image_path"])
            print("-" * 70)

    # ------------------------------------------------------

    def customers_also_bought(
        self,
        product_name: str,
        top_k: int = 5,
    ):
        """
        Simulated 'Customers Also Bought'.

        Since purchase history is unavailable, we return similar products while
        excluding the selected product itself.
        """
        recommendations = self.recommend_from_product(
            product_name,
            top_k=top_k + 2,
        )

        filtered = []

        for item in recommendations:
            if item["product_name"] != product_name:
                filtered.append(item)

            if len(filtered) >= top_k:
                break

        return filtered

    # ------------------------------------------------------

    def trending_products(
        self,
        top_k: int = 10,
    ):
        """
        Simulated trending products.

        Returns the first N products. Can later be replaced with real analytics
        data.
        """
        return self.products[:top_k]

    # ------------------------------------------------------

    def personalized_recommendations(
        self,
        interests,
        top_k: int = 5,
    ):
        """
        Recommend products using multiple user interests.

        Example:
            interests = [
                "running shoes",
                "black",
                "nike",
            ]
        """
        recommendations = []
        seen = set()

        for interest in interests:
            results = self.recommend_from_query(
                interest,
                top_k=top_k,
            )

            for product in results:
                if product["id"] not in seen:
                    recommendations.append(product)
                    seen.add(product["id"])

                if len(recommendations) >= top_k:
                    return recommendations

        return recommendations

    # ------------------------------------------------------

    def random_products(
        self,
        top_k: int = 5,
    ):
        """
        Random discovery products.
        """
        import random

        total = min(
            top_k,
            len(self.products),
        )

        return random.sample(
            self.products,
            total,
        )

    # ------------------------------------------------------

    def recommendation_summary(
        self,
        query: str,
        top_k: int = 5,
    ):
        """
        Return complete recommendation package.
        """
        return {
            "query": query,
            "recommendations": self.recommend_from_query(
                query,
                top_k,
            ),
            "trending": self.trending_products(5),
            "random": self.random_products(5),
        }

    # ------------------------------------------------------

    def print_summary(
        self,
        query: str,
    ):
        """
        Print recommendation summary.
        """
        summary = self.recommendation_summary(query)

        print()
        print("=" * 70)
        print("Recommendation Summary")
        print("=" * 70)
        print()
        print("Query:")
        print(summary["query"])
        print()
        print("Recommendations:")

        for item in summary["recommendations"]:
            print("-", item["product_name"])

        print()
        print("Trending:")

        for item in summary["trending"]:
            print("-", item["product_name"])

        print()
        print("Discover:")

        for item in summary["random"]:
            print("-", item["product_name"])

    # ------------------------------------------------------

    def compare_products(
        self,
        product_a: str,
        product_b: str,
    ):
        """
        Compare two products.
        """
        first = self.get_product_by_name(product_a)
        second = self.get_product_by_name(product_b)

        if first is None or second is None:
            return None

        import pandas as pd

        comparison = pd.DataFrame(
            {
                "Feature": [
                    "Product Name",
                    "Category",
                    "Colour",
                    "Usage",
                ],
                first["product_name"]: [
                    first["product_name"],
                    first.get("category", "-"),
                    first.get("colour", "-"),
                    first.get("usage", "-"),
                ],
                second["product_name"]: [
                    second["product_name"],
                    second.get("category", "-"),
                    second.get("colour", "-"),
                    second.get("usage", "-"),
                ],
            }
        )

        return comparison

    # ------------------------------------------------------

    def ai_compare_products(
        self,
        product_a: str,
        product_b: str,
    ):
        """
        Generate an AI comparison using Gemini.
        """
        comparison = self.compare_products(
            product_a,
            product_b,
        )

        if comparison is None:
            return "Unable to compare products."

        prompt = f"""
You are an AI Shopping Assistant.

Compare the following two products.

{comparison}

Explain

- Similarities
- Differences
- Best use cases
- Which customer should choose Product A
- Which customer should choose Product B

Keep the answer concise.
"""
        return self.llm.generate(prompt)

    # ------------------------------------------------------

    def explain_recommendation(
        self,
        product: dict,
    ):
        """
        Human-readable explanation.
        """
        explanation = []

        explanation.append(
            f"{product['product_name']} was recommended because:"
        )

        if product.get("category"):
            explanation.append(f"- Category: {product['category']}")

        if product.get("colour"):
            explanation.append(f"- Colour: {product['colour']}")

        if product.get("usage"):
            explanation.append(f"- Usage: {product['usage']}")

        if product.get("similarity"):
            explanation.append(f"- Similarity Score: {product['similarity']}")

        return "\n".join(explanation)

    # ------------------------------------------------------

    def recommendation_pipeline(
        self,
        query: str,
        top_k: int = 5,
    ):
        """
        Complete recommendation pipeline.
        """
        recommendations = self.recommend_from_query(
            query,
            top_k,
        )

        explanations = []

        for product in recommendations:
            explanations.append(
                self.explain_recommendation(product)
            )

        return {
            "query": query,
            "recommendations": recommendations,
            "explanations": explanations,
            "statistics": {
                "products_found": len(recommendations),
            },
        }

    # ------------------------------------------------------

    def print_pipeline(
        self,
        query: str,
    ):
        """
        Display recommendation pipeline.
        """
        pipeline = self.recommendation_pipeline(query)

        print()
        print("=" * 70)
        print("Recommendation Pipeline")
        print("=" * 70)
        print()
        print("Query:")
        print(pipeline["query"])
        print()

        for i, product in enumerate(
            pipeline["recommendations"],
            start=1,
        ):
            print(f"{i}.")
            print(product["product_name"])
            print()
            print(pipeline["explanations"][i - 1])
            print("-" * 60)


# ==========================================================
# Testing
# ==========================================================

if __name__ == "__main__":
    engine = RecommendationEngine()

    print()
    print("=" * 70)
    print("Recommendation Engine")
    print("=" * 70)

    engine.print_pipeline("black running shoes")

    print()

    comparison = engine.ai_compare_products(
        "Nike Men Black Roshe Run Sports Shoes",
        "Puma Men Black Sports Shoes",
    )

    print()
    print("=" * 70)
    print("AI PRODUCT COMPARISON")
    print("=" * 70)
    print(comparison)
