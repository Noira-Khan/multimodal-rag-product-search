"""
==========================================================
ANALYTICS DATABASE

Module:
    analytics_db.py

Responsibilities
----------------
✔ SQLite Connection
✔ Database Creation
✔ Table Creation

Author:
    Noira Khan

Project:
    Multimodal Retail Assistant
==========================================================
"""

from __future__ import annotations

import sqlite3

from pathlib import Path
from turtle import pd

# ==========================================================
# Database Location
# ==========================================================

DATABASE = Path(__file__).parent / "analytics.db"

# ==========================================================
# Analytics Database
# ==========================================================


class AnalyticsDB:

    """
    SQLite backend for analytics.
    """

    def __init__(self):

        self.connection = sqlite3.connect(

            DATABASE,

            check_same_thread=False

        )

        self.connection.row_factory = sqlite3.Row

        self.cursor = self.connection.cursor()

        self.create_tables()

    # ------------------------------------------------------

    def create_tables(self):

        """
        Create analytics tables.
        """

        # ----------------------------------------------
        # Searches
        # ----------------------------------------------

        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS searches(

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                query TEXT,

                results INTEGER,

                success INTEGER,

                response_time REAL,

                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP

            )
            """
        )

        # ----------------------------------------------
        # Chats
        # ----------------------------------------------

        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS chats(

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                query TEXT,

                response TEXT,

                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP

            )
            """
        )

        # ----------------------------------------------
        # Recommendations
        # ----------------------------------------------

        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS recommendations(

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                query TEXT,

                recommendation_count INTEGER,

                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP

            )
            """
        )

        # ----------------------------------------------
        # Comparisons
        # ----------------------------------------------

        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS comparisons(

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                product_a TEXT,

                product_b TEXT,

                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP

            )
            """
        )

        # ----------------------------------------------
        # Clicks
        # ----------------------------------------------

        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS clicks(

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                product_name TEXT,

                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP

            )
            """
        )

        self.connection.commit()


            # ------------------------------------------------------
    # Insert Search
    # ------------------------------------------------------

    def insert_search(

        self,

        query: str,

        results: int,

        success: bool,

        response_time: float,

    ):
        """
        Store a product search.
        """

        self.cursor.execute(

            """
            INSERT INTO searches(

                query,

                results,

                success,

                response_time

            )

            VALUES (?, ?, ?, ?)

            """,

            (

                query,

                results,

                int(success),

                response_time,

            )

        )

        self.connection.commit()

    # ------------------------------------------------------
    # Insert Chat
    # ------------------------------------------------------

    def insert_chat(

        self,

        query: str,

        response: str,

    ):
        """
        Store an AI conversation.
        """

        self.cursor.execute(

            """
            INSERT INTO chats(

                query,

                response

            )

            VALUES (?, ?)

            """,

            (

                query,

                response,

            )

        )

        self.connection.commit()

    # ------------------------------------------------------
    # Insert Recommendation
    # ------------------------------------------------------

    def insert_recommendation(

        self,

        query: str,

        recommendation_count: int,

    ):
        """
        Store recommendation event.
        """

        self.cursor.execute(

            """
            INSERT INTO recommendations(

                query,

                recommendation_count

            )

            VALUES (?, ?)

            """,

            (

                query,

                recommendation_count,

            )

        )

        self.connection.commit()

    # ------------------------------------------------------
    # Insert Comparison
    # ------------------------------------------------------

    def insert_comparison(

        self,

        product_a: str,

        product_b: str,

    ):
        """
        Store product comparison.
        """

        self.cursor.execute(

            """
            INSERT INTO comparisons(

                product_a,

                product_b

            )

            VALUES (?, ?)

            """,

            (

                product_a,

                product_b,

            )

        )

        self.connection.commit()

    # ------------------------------------------------------
    # Insert Click
    # ------------------------------------------------------

    def insert_click(

        self,

        product_name: str,

    ):
        """
        Store recommendation click.
        """

        self.cursor.execute(

            """
            INSERT INTO clicks(

                product_name

            )

            VALUES (?)

            """,

            (

                product_name,

            )

        )

        self.connection.commit()

            # ------------------------------------------------------
    # Total Searches
    # ------------------------------------------------------

    def total_searches(self):

        self.cursor.execute(

            "SELECT COUNT(*) AS total FROM searches"

        )

        return self.cursor.fetchone()["total"]

    # ------------------------------------------------------
    # Total Chats
    # ------------------------------------------------------

    def total_chats(self):

        self.cursor.execute(

            "SELECT COUNT(*) AS total FROM chats"

        )

        return self.cursor.fetchone()["total"]

    # ------------------------------------------------------
    # Total Recommendations
    # ------------------------------------------------------

    def total_recommendations(self):

        self.cursor.execute(

            "SELECT COUNT(*) AS total FROM recommendations"

        )

        return self.cursor.fetchone()["total"]

    # ------------------------------------------------------
    # Total Comparisons
    # ------------------------------------------------------

    def total_comparisons(self):

        self.cursor.execute(

            "SELECT COUNT(*) AS total FROM comparisons"

        )

        return self.cursor.fetchone()["total"]

    # ------------------------------------------------------
    # Total Clicks
    # ------------------------------------------------------

    def total_clicks(self):

        self.cursor.execute(

            "SELECT COUNT(*) AS total FROM clicks"

        )

        return self.cursor.fetchone()["total"]

    # ------------------------------------------------------
    # Search Success Rate
    # ------------------------------------------------------

    def search_success_rate(self):

        self.cursor.execute(

            """
            SELECT
                COUNT(*) AS total,
                SUM(success) AS successful
            FROM searches
            """

        )

        row = self.cursor.fetchone()

        total = row["total"]

        successful = row["successful"] or 0

        if total == 0:

            return 0

        return round(

            successful / total * 100,

            2

        )

    # ------------------------------------------------------
    # Average Response Time
    # ------------------------------------------------------

    def average_response_time(self):

        self.cursor.execute(

            """
            SELECT AVG(response_time) AS avg_time
            FROM searches
            """

        )

        row = self.cursor.fetchone()

        if row["avg_time"] is None:

            return 0

        return round(

            row["avg_time"],

            3

        )

    # ------------------------------------------------------
    # CTR
    # ------------------------------------------------------

    def ctr(self):

        recommendations = self.total_recommendations()

        if recommendations == 0:

            return 0

        return round(

            self.total_clicks()

            / recommendations

            * 100,

            2

        )

    # ------------------------------------------------------
    # Recommendation Acceptance
    # ------------------------------------------------------

    def recommendation_acceptance_rate(self):

        recommendations = self.total_recommendations()

        if recommendations == 0:

            return 0

        accepted = min(

            self.total_clicks(),

            recommendations

        )

        return round(

            accepted

            / recommendations

            * 100,

            2

        )

    # ------------------------------------------------------
    # North Star Metric
    # ------------------------------------------------------

    def north_star_metric(self):

        searches = self.total_searches()

        if searches == 0:

            return 0

        return round(

            self.total_recommendations()

            / searches

            * 100,

            2

        )
    
        # ------------------------------------------------------
    # Top Search Queries
    # ------------------------------------------------------

    def get_top_queries(

        self,

        limit: int = 10,

    ):
        """
        Return most searched queries.
        """

        self.cursor.execute(

            """
            SELECT

                query,

                COUNT(*) AS count

            FROM searches

            GROUP BY query

            ORDER BY count DESC

            LIMIT ?

            """,

            (limit,)

        )

        import pandas as pd

        rows = self.cursor.fetchall()

        return pd.DataFrame(

        rows,

        columns=[

        "query",

        "count"

            ]

            )

    # ------------------------------------------------------
    # Top Compared Products
    # ------------------------------------------------------

    def get_top_compared_products(

        self,

        limit: int = 10,

    ):
        """
        Return most compared products.
        """

        self.cursor.execute(

            """
            SELECT

                product,

                COUNT(*) AS count

            FROM (

                SELECT product_a AS product

                FROM comparisons

                UNION ALL

                SELECT product_b AS product

                FROM comparisons

            )

            GROUP BY product

            ORDER BY count DESC

            LIMIT ?

            """,

            (limit,)

        )

        return [

            (row["product"], row["count"])

            for row in self.cursor.fetchall()

        ]

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
        Build everything required
        for the dashboard.
        """

        return {

            "kpis":

                self.kpi_summary(),

            "top_queries":

                self.get_top_queries(),

            "top_compared":

                self.get_top_compared_products(),

        }

    # ------------------------------------------------------
    # Close Connection
    # ------------------------------------------------------

    def close(self):

        self.connection.close()
        