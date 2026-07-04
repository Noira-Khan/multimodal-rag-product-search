"""
==========================================================
RAG Engine
Multimodal Retail Assistant (Myntra AI)
==========================================================

Part 1
------
✔ Load metadata
✔ Load embedding model
✔ Generate embeddings
✔ Cache embeddings
✔ Load cached embeddings
✔ Create FAISS vector index
✔ Save FAISS vector index
✔ Load FAISS vector index
✔ Semantic search
✔ Retrieve products
✔ Build RAG context
✔ Explain retrieved products

Author: Noira Khan
==========================================================
"""

from pathlib import Path
import pickle
import logging

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

from metadata import MetadataManager


# ----------------------------------------------------------
# Logging
# ----------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)


# ----------------------------------------------------------
# Project Paths
# ----------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

VECTOR_STORE = BASE_DIR / "vector_store"

EMBEDDING_CACHE = VECTOR_STORE / "embeddings.pkl"
FAISS_INDEX = VECTOR_STORE / "product_index.faiss"


# ----------------------------------------------------------
# RAG Engine
# ----------------------------------------------------------

class RAGEngine:
    """
    Handles embedding generation and semantic retrieval.
    """

    def __init__(self):
        logger.info("Initializing RAG Engine...")

        self.metadata = MetadataManager()

        self.products = self.metadata.get_all_products()
        self.documents = self.metadata.get_documents()

        self.model_name = "sentence-transformers/all-MiniLM-L6-v2"
        self.model = self.load_embedding_model()

        self.embeddings = None
        self.index = None

    # ------------------------------------------------------

    def load_embedding_model(self):
        """
        Load Sentence Transformer.
        """

        logger.info("Loading embedding model...")

        model = SentenceTransformer(self.model_name)

        logger.info("Embedding model loaded successfully.")

        return model

    # ------------------------------------------------------

    def generate_embeddings(self):
        """
        Generate embeddings for every product document.
        """

        logger.info("Generating document embeddings...")

        embeddings = self.model.encode(
            self.documents,
            show_progress_bar=True,
            convert_to_numpy=True,
            normalize_embeddings=True
        )

        self.embeddings = embeddings

        logger.info(
            f"Generated {len(embeddings)} embeddings."
        )

        return embeddings

    # ------------------------------------------------------

    def save_embeddings(self):
        """
        Save embeddings to disk.

        Prevents recomputing every app launch.
        """

        if self.embeddings is None:
            raise ValueError("No embeddings available to save.")

        VECTOR_STORE.mkdir(
            parents=True,
            exist_ok=True
        )

        with open(EMBEDDING_CACHE, "wb") as file:
            pickle.dump(
                self.embeddings,
                file
            )

        logger.info(
            f"Embeddings saved to:\n{EMBEDDING_CACHE}"
        )

    # ------------------------------------------------------

    def load_embeddings(self):
        """
        Load cached embeddings.
        """

        if not EMBEDDING_CACHE.exists():
            logger.warning("Embedding cache not found.")
            return None

        with open(EMBEDDING_CACHE, "rb") as file:
            embeddings = pickle.load(file)

        self.embeddings = embeddings

        logger.info("Embeddings loaded from cache.")

        return embeddings

    # ------------------------------------------------------

    def get_embeddings(self):
        """
        Return embeddings.

        If cache exists, load it.
        Otherwise generate embeddings.
        """

        if self.embeddings is not None:
            return self.embeddings

        embeddings = self.load_embeddings()

        if embeddings is not None:
            return embeddings

        embeddings = self.generate_embeddings()

        self.save_embeddings()

        return embeddings

    # ------------------------------------------------------

    def create_vector_index(self):
        """
        Create a FAISS vector index from embeddings.
        """

        logger.info("Creating FAISS vector index...")

        embeddings = self.get_embeddings()

        dimension = embeddings.shape[1]

        index = faiss.IndexFlatIP(dimension)

        index.add(
            embeddings.astype("float32")
        )

        self.index = index

        logger.info(
            f"FAISS index created with {index.ntotal} vectors."
        )

        return index

    # ------------------------------------------------------

    def save_vector_index(self):
        """
        Save FAISS index to disk.
        """

        if self.index is None:
            raise ValueError("No FAISS index available to save.")

        VECTOR_STORE.mkdir(
            parents=True,
            exist_ok=True
        )

        faiss.write_index(
            self.index,
            str(FAISS_INDEX)
        )

        logger.info(
            f"FAISS index saved:\n{FAISS_INDEX}"
        )

    # ------------------------------------------------------

    def load_vector_index(self):
        """
        Load FAISS index if available.
        """

        if not FAISS_INDEX.exists():
            logger.warning("FAISS index not found.")
            return None

        self.index = faiss.read_index(
            str(FAISS_INDEX)
        )

        logger.info(
            f"Loaded FAISS index with {self.index.ntotal} vectors."
        )

        return self.index

    # ------------------------------------------------------

    def get_vector_index(self):
        """
        Return a usable FAISS index.

        If the index exists, load it.
        Otherwise create and save a new one.
        """

        if self.index is not None:
            return self.index

        index = self.load_vector_index()

        if index is not None:
            return index

        logger.info("Generating a new FAISS index...")

        index = self.create_vector_index()

        self.save_vector_index()

        return index

    # ------------------------------------------------------

    def vector_dimension(self):
        """
        Return embedding dimension.
        """

        embeddings = self.get_embeddings()

        return embeddings.shape[1]

    # ------------------------------------------------------

    def total_vectors(self):
        """
        Return total indexed vectors.
        """

        index = self.get_vector_index()

        return index.ntotal

    # ------------------------------------------------------

    def validate_vector_store(self):
        """
        Validate FAISS index consistency.
        """

        embeddings = self.get_embeddings()
        index = self.get_vector_index()

        if len(embeddings) != index.ntotal:
            raise ValueError(
                "Embedding count and FAISS index do not match."
            )

        logger.info("Vector store validation successful.")

        return True

    # ------------------------------------------------------

    def encode_query(self, query: str):
        """
        Convert user query into an embedding vector.
        """

        query_embedding = self.model.encode(
            [query],
            convert_to_numpy=True,
            normalize_embeddings=True
        )

        return query_embedding.astype("float32")

    # ------------------------------------------------------

    def semantic_search(self, query: str, top_k: int = 5):
        """
        Search the vector database.
        """

        index = self.get_vector_index()

        query_vector = self.encode_query(query)

        scores, indices = index.search(
            query_vector,
            top_k
        )

        return scores[0], indices[0]

    # ------------------------------------------------------

    def retrieve_products(self, query: str, top_k: int = 5):
        """
        Retrieve relevant products.
        """

        scores, indices = self.semantic_search(
            query,
            top_k
        )

        results = []

        for score, idx in zip(scores, indices):
            if idx < 0:
                continue

            product = self.products[idx].copy()

            product["similarity"] = round(
                float(score),
                3
            )

            results.append(product)

        return results

    # ------------------------------------------------------

    def search(self, query: str, top_k: int = 5):
        """
        Public search function.
        """

        logger.info(
            f"Searching: {query}"
        )

        return self.retrieve_products(
            query,
            top_k
        )

    # ------------------------------------------------------

    def display_results(self, results):
        """
        Print retrieved products.
        """

        print()
        print("=" * 70)
        print("Retrieved Products")
        print("=" * 70)

        for i, product in enumerate(results, 1):
            print()
            print(f"{i}.")
            print(product["product_name"])
            print("Category :", product["category"])
            print("Similarity:", product["similarity"])

    # ------------------------------------------------------

    def build_context(self, products):
        """
        Converts retrieved products into a context string for the LLM.
        """

        context = []

        for product in products:
            context.append(product["document"])

        return "\n\n".join(context)

    # ------------------------------------------------------

    def explain_product(self, product):
        """
        Generate a rule-based explanation for why the product was retrieved.
        """

        explanation = []

        if product.get("category"):
            explanation.append(
                f"Category: {product['category']}"
            )

        if product.get("colour"):
            explanation.append(
                f"Colour: {product['colour']}"
            )

        if product.get("season"):
            explanation.append(
                f"Season: {product['season']}"
            )

        if product.get("usage"):
            explanation.append(
                f"Usage: {product['usage']}"
            )

        explanation.append(
            f"Similarity Score: {product['similarity']:.2f}"
        )

        return explanation

    # ------------------------------------------------------

    def explain_results(self, results):
        """
        Adds explanation to every retrieved product.
        """

        for product in results:
            product["explanation"] = self.explain_product(product)

        return results

    # ------------------------------------------------------

    def retrieve_context(self, query, top_k=5):
        """
        Main RAG retrieval function.

        Used by chatbot.py.
        """

        products = self.retrieve_products(
            query,
            top_k
        )

        context = self.build_context(
            products
        )

        return {
            "query": query,
            "products": products,
            "context": context
        }

    # ------------------------------------------------------

    def search_pipeline(self, query, top_k=5):
        """
        Complete retrieval pipeline.
        """

        products = self.retrieve_products(
            query,
            top_k
        )

        products = self.explain_results(
            products
        )

        context = self.build_context(
            products
        )

        return {
            "query": query,
            "results": products,
            "context": context
        }

    # ------------------------------------------------------

    def print_pipeline(self, pipeline):
        """
        Display pipeline output.
        """

        print()
        print("=" * 70)
        print("USER QUERY")
        print("=" * 70)
        print(pipeline["query"])

        print()
        print("=" * 70)
        print("TOP RETRIEVED PRODUCTS")
        print("=" * 70)

        for i, product in enumerate(
            pipeline["results"],
            start=1
        ):
            print()
            print(f"{i}. {product['product_name']}")
            print()

            for item in product["explanation"]:
                print("•", item)

        print()
        print("=" * 70)
        print("RAG CONTEXT")
        print("=" * 70)
        print(
            pipeline["context"][:1000]
        )
        print()
        print("=" * 70)

        return True


# ----------------------------------------------------------
# Testing
# ----------------------------------------------------------

if __name__ == "__main__":
    rag = RAGEngine()

    rag.get_vector_index()

    query = input(
        "\nSearch Product: "
    )

    pipeline = rag.search_pipeline(
        query,
        top_k=5
    )

    rag.print_pipeline(
        pipeline
    )