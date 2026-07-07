"""
==========================================================
ANALYTICS SERVICE

This module provides a clean interface between the
application pages and the SQLite analytics database.

Project:
    Multimodal Retail Assistant
==========================================================
"""

from __future__ import annotations

import logging

from analytics_db import AnalyticsDB

# ==========================================================
# Logging
# ==========================================================

logging.basicConfig(

    level=logging.INFO,

    format="%(levelname)s | %(message)s"

)

logger = logging.getLogger(__name__)

# ==========================================================
# Analytics Service
# ==========================================================


class Analytics:

    """
    Analytics service used throughout the application.

    Pages never talk directly to SQLite.
    They only call Analytics().
    """

    def __init__(self):

        self.db = AnalyticsDB()

        logger.info(

            "Analytics Service Ready."

        )

    # ------------------------------------------------------
    # Search
    # ------------------------------------------------------

    def log_search(

        self,

        query,

        results,

        response_time,

    ):

        self.db.insert_search(

            query=query,

            results=results,

            success=results > 0,

            response_time=response_time,

        )

    # ------------------------------------------------------
    # Chat
    # ------------------------------------------------------

    def log_chat(

        self,

        query,

        response,

    ):

        self.db.insert_chat(

            query,

            response

        )

    # ------------------------------------------------------
    # Recommendation
    # ------------------------------------------------------

    def log_recommendation(

        self,

        query,

        recommendations,

    ):

        self.db.insert_recommendation(

            query,

            len(recommendations)

        )

    # ------------------------------------------------------
    # Comparison
    # ------------------------------------------------------

    def log_comparison(

        self,

        product_a,

        product_b,

    ):

        self.db.insert_comparison(

            product_a,

            product_b

        )

    # ------------------------------------------------------
    # Click
    # ------------------------------------------------------

    def log_click(

        self,

        product_name,

    ):

        self.db.insert_click(

            product_name

        )

    # ------------------------------------------------------
    # KPI Summary
    # ------------------------------------------------------

    def kpi_summary(self):

        return self.db.kpi_summary()

    # ------------------------------------------------------
    # Dashboard
    # ------------------------------------------------------

    def dashboard_pipeline(self):

        return self.db.dashboard_pipeline()

    # ------------------------------------------------------
    # Close
    # ------------------------------------------------------

    def close(self):

        self.db.close()


# ==========================================================
# Testing
# ==========================================================

if __name__ == "__main__":

    analytics = Analytics()

    analytics.log_search(

        query="nike shoes",

        results=8,

        response_time=0.31

    )

    analytics.log_chat(

        "Need running shoes",

        "Nike Pegasus"

    )

    analytics.log_recommendation(

        "nike shoes",

        [

            "Nike Pegasus",

            "Nike Revolution"

        ]

    )

    analytics.log_comparison(

        "Nike Pegasus",

        "Nike Revolution"

    )

    analytics.log_click(

        "Nike Pegasus"

    )

    print()

    print("=" * 60)

    print("KPI SUMMARY")

    print("=" * 60)

    for key, value in analytics.kpi_summary().items():

        print(f"{key:35} {value}")

    print()

    print("=" * 60)

    print("DASHBOARD")

    print("=" * 60)

    print(analytics.dashboard_pipeline())

    analytics.close()

    