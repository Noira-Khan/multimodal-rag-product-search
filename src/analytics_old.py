"""
==========================================================
ANALYTICS — PART 1 OF 4
Multimodal Retail Assistant (Myntra AI)
==========================================================

Module:
    analytics.py

Current Part:
    Part 1 / 4

Responsibilities
----------------
✔ Analytics Engine
✔ Search Logs
✔ Chat Logs
✔ Recommendation Logs
✔ Comparison Logs
✔ Response Time Logs

Upcoming Parts
--------------
Part 2
✔ Logging Methods

Part 3
✔ KPI Calculations

Part 4
✔ Dashboard Pipeline
✔ Testing

Author:
    Noira Khan
==========================================================
"""

from __future__ import annotations

import logging
import time

from collections import Counter
from statistics import mean

# ==========================================================
# Logging
# ==========================================================

logging.basicConfig(

    level=logging.INFO,

    format="%(levelname)s | %(message)s"

)

logger = logging.getLogger(__name__)

# ==========================================================
# Analytics Engine
# ==========================================================


class Analytics:
    """
    Collects analytics across the entire application.

    Modules using this class

    • Product Search

    • AI Assistant

    • Recommendation Engine

    • Product Comparison

    • Dashboard

    • Customer Insights
    """

    # ------------------------------------------------------

    def __init__(self):

        logger.info(

            "Initializing Analytics Engine..."

        )

        # ----------------------------------------------
        # Search Logs
        # ----------------------------------------------

        self.search_logs = []

        # ----------------------------------------------
        # Chat Logs
        # ----------------------------------------------

        self.chat_logs = []

        # ----------------------------------------------
        # Recommendation Logs
        # ----------------------------------------------

        self.recommendation_logs = []

        # ----------------------------------------------
        # Comparison Logs
        # ----------------------------------------------

        self.comparison_logs = []

        # ----------------------------------------------
        # Response Time Logs
        # ----------------------------------------------

        self.response_times = []

        # ----------------------------------------------
        # Click Logs
        # ----------------------------------------------

        self.click_logs = []

        logger.info(

            "Analytics Engine Ready."

        )

        # ------------------------------------------------------
    # Log Search
    # ------------------------------------------------------

    def log_search(

            self,

            query: str,

            results: int,

            response_time: float,

    ):
        """
        Log a product search.
        """

        log = {

            "query": query,

            "results": results,

            "success": results > 0,

            "response_time": response_time,

            "timestamp": time.time()

        }

        self.search_logs.append(log)

        self.response_times.append(

            response_time

        )

    # ------------------------------------------------------
    # Log Chat
    # ------------------------------------------------------

    def log_chat(

            self,

            query: str,

            response: str,

    ):
        """
        Log an AI assistant interaction.
        """

        log = {

            "query": query,

            "response": response,

            "timestamp": time.time()

        }

        self.chat_logs.append(log)

    # ------------------------------------------------------
    # Log Recommendation
    # ------------------------------------------------------

    def log_recommendation(

            self,

            query: str,

            recommendations,

    ):
        """
        Log recommendation results.
        """

        log = {

            "query": query,

            "count": len(recommendations),

            "recommendations": recommendations,

            "timestamp": time.time()

        }

        self.recommendation_logs.append(log)

    # ------------------------------------------------------
    # Log Comparison
    # ------------------------------------------------------

    def log_comparison(

            self,

            product_a: str,

            product_b: str,

    ):
        """
        Log product comparison.
        """

        log = {

            "product_a": product_a,

            "product_b": product_b,

            "timestamp": time.time()

        }

        self.comparison_logs.append(log)

    # ------------------------------------------------------
    # Log Click
    # ------------------------------------------------------

    def log_click(

            self,

            product_name: str,

    ):
        """
        Log recommendation click.
        """

        log = {

            "product_name": product_name,

            "timestamp": time.time()

        }

        self.click_logs.append(log)

    # ------------------------------------------------------
    # Clear Logs
    # ------------------------------------------------------

    def clear_logs(self):
        """
        Remove every analytics log.
        """

        self.search_logs.clear()

        self.chat_logs.clear()

        self.recommendation_logs.clear()

        self.comparison_logs.clear()

        self.response_times.clear()

        self.click_logs.clear()

    # ------------------------------------------------------
    # Totals
    # ------------------------------------------------------

    def total_searches(self):

        return len(

            self.search_logs

        )

    # ------------------------------------------------------

    def total_chats(self):

        return len(

            self.chat_logs

        )

    # ------------------------------------------------------

    def total_recommendations(self):

        return len(

            self.recommendation_logs

        )

    # ------------------------------------------------------

    def total_comparisons(self):

        return len(

            self.comparison_logs

        )

    # ------------------------------------------------------

    def total_clicks(self):

        return len(

            self.click_logs

        )
        # ------------------------------------------------------
    # Search Success Rate
    # ------------------------------------------------------

    def search_success_rate(self):
        """
        Percentage of successful searches.
        """

        if self.total_searches() == 0:
            return 0

        successful = sum(

            1

            for log in self.search_logs

            if log["success"]

        )

        return round(

            successful / self.total_searches() * 100,

            2

        )

    # ------------------------------------------------------
    # Average Response Time
    # ------------------------------------------------------

    def average_response_time(self):
        """
        Average response time.
        """

        if not self.response_times:
            return 0

        return round(

            mean(self.response_times),

            3

        )

    # ------------------------------------------------------
    # Click Through Rate (CTR)
    # ------------------------------------------------------

    def ctr(self):
        """
        Simulated click-through rate.
        """

        if self.total_recommendations() == 0:
            return 0

        return round(

            self.total_clicks()

            / self.total_recommendations()

            * 100,

            2

        )

    # ------------------------------------------------------
    # Recommendation Acceptance Rate
    # ------------------------------------------------------

    def recommendation_acceptance_rate(self):
        """
        Simulated recommendation acceptance.
        """

        if self.total_recommendations() == 0:
            return 0

        accepted = min(

            self.total_clicks(),

            self.total_recommendations()

        )

        return round(

            accepted

            / self.total_recommendations()

            * 100,

            2

        )

    # ------------------------------------------------------
    # North Star Metric
    # ------------------------------------------------------

    def north_star_metric(self):
        """
        Percentage of searches that produced recommendations.
        """

        if self.total_searches() == 0:
            return 0

        return round(

            self.total_recommendations()

            / self.total_searches()

            * 100,

            2

        )

    # ------------------------------------------------------
    # Most Searched Queries
    # ------------------------------------------------------

    def most_searched_queries(

            self,

            top_n: int = 10,

    ):
        """
        Most frequent user searches.
        """

        queries = [

            log["query"]

            for log in self.search_logs

        ]

        return Counter(

            queries

        ).most_common(

            top_n

        )

    # ------------------------------------------------------
    # Most Compared Products
    # ------------------------------------------------------

    def most_compared_products(

            self,

            top_n: int = 10,

    ):
        """
        Most frequently compared products.
        """

        products = []

        for log in self.comparison_logs:

            products.append(

                log["product_a"]

            )

            products.append(

                log["product_b"]

            )

        return Counter(

            products

        ).most_common(

            top_n

        )

    # ------------------------------------------------------
    # KPI Summary
    # ------------------------------------------------------

    def kpi_summary(self):
        """
        Executive KPI summary.
        """

        return {

            "Total Searches":
                self.total_searches(),

            "Total Chats":
                self.total_chats(),

            "Total Recommendations":
                self.total_recommendations(),

            "Total Comparisons":
                self.total_comparisons(),

            "Total Clicks":
                self.total_clicks(),

            "Search Success Rate":
                self.search_success_rate(),

            "Average Response Time":
                self.average_response_time(),

            "CTR":
                self.ctr(),

            "Recommendation Acceptance":
                self.recommendation_acceptance_rate(),

            "North Star Metric":
                self.north_star_metric(),

        }
        # ------------------------------------------------------
    # Dashboard Pipeline
    # ------------------------------------------------------

    def dashboard_pipeline(self):
        """
        Everything required by the dashboard.
        """

        return {

            "kpis": self.kpi_summary(),

            "top_queries": self.most_searched_queries(),

            "top_compared": self.most_compared_products(),

            "search_logs": self.search_logs,

            "chat_logs": self.chat_logs,

            "recommendation_logs": self.recommendation_logs,

            "comparison_logs": self.comparison_logs,

            "click_logs": self.click_logs

        }
    

# ==========================================================
# Testing
# ==========================================================

if __name__ == "__main__":

    analytics = Analytics()

    # --------------------------------------------------
    # Searches
    # --------------------------------------------------

    analytics.log_search(

        query="black running shoes",

        results=5,

        response_time=0.41

    )

    analytics.log_search(

        query="nike shoes",

        results=8,

        response_time=0.33

    )

    analytics.log_search(

        query="formal shirts",

        results=0,

        response_time=0.52

    )

    # --------------------------------------------------
    # Chat
    # --------------------------------------------------

    analytics.log_chat(

        "Suggest office shoes",

        "Nike Air Max"

    )

    analytics.log_chat(

        "Need backpacks",

        "Wildcraft Backpack"

    )

    # --------------------------------------------------
    # Recommendations
    # --------------------------------------------------

    analytics.log_recommendation(

        "running shoes",

        [

            "Nike Air Max",

            "Adidas Ultraboost",

            "Puma Velocity"

        ]

    )

    analytics.log_recommendation(

        "office shirts",

        [

            "Arrow Shirt",

            "Van Heusen Shirt"

        ]

    )

    # --------------------------------------------------
    # Comparisons
    # --------------------------------------------------

    analytics.log_comparison(

        "Nike Air Max",

        "Adidas Ultraboost"

    )

    analytics.log_comparison(

        "Nike Air Max",

        "Puma Velocity"

    )

    # --------------------------------------------------
    # Clicks
    # --------------------------------------------------

    analytics.log_click(

        "Nike Air Max"

    )

    analytics.log_click(

        "Arrow Shirt"

    )

    # --------------------------------------------------
    # Dashboard
    # --------------------------------------------------

    dashboard = analytics.dashboard_pipeline()

    print()

    print("=" * 70)

    print("AI PRODUCT ANALYTICS")

    print("=" * 70)

    print()

    print("KPI SUMMARY")

    print()

    for key, value in dashboard["kpis"].items():

        print(

            f"{key:35}",

            value

        )

    print()

    print("-" * 70)

    print("MOST SEARCHED QUERIES")

    print("-" * 70)

    print()

    for query, count in dashboard["top_queries"]:

        print(

            query,

            "->",

            count

        )

    print()

    print("-" * 70)

    print("MOST COMPARED PRODUCTS")

    print("-" * 70)

    print()

    for product, count in dashboard["top_compared"]:

        print(

            product,

            "->",

            count

        )

    print()

    print("=" * 70)

    