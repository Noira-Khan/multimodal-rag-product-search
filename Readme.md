# Multimodal RAG Product Search

## 1. Project Overview

Multimodal RAG Product Search is an AI-powered Visual Search Engine that combines Computer Vision, Retrieval-Augmented Generation (RAG), Vector Search, and Large Language Models (LLMs) to help users discover visually similar products from an e-commerce catalog.

Instead of searching using keywords, users can upload a product image and retrieve similar products along with AI-generated explanations and source citations.


## 2. Business Problem

Traditional e-commerce search engines depend heavily on keyword matching.

### Challenges

1. Users may not know the exact product name.
2. Product descriptions may vary across platforms.
3. Keyword searches often miss visually similar products.
4. Product discovery becomes difficult for fashion and lifestyle items.

### Example Use Cases

| User Input             | Desired Output          |
| ---------------------- | ----------------------- |
| Upload Shoe Image      | Similar Shoes           |
| Upload Watch Image     | Similar Watches         |
| Upload T-Shirt Image   | Similar Apparel         |
| Upload Handbag Image   | Similar Bags            |
| Upload Fashion Product | Related Recommendations |


## 3. Solution

The system leverages:

1. OpenCLIP for image understanding.
2. FAISS for vector similarity search.
3. Product metadata for contextual retrieval.
4. LLMs for explainable recommendations.
5. RAG architecture for grounded responses.

## 4. Dataset

### Fashion Product Images Dataset

The dataset contains:

| Field              | Description               |
| ------------------ | ------------------------- |
| id                 | Unique Product Identifier |
| masterCategory     | Primary Category          |
| subCategory        | Secondary Category        |
| articleType        | Product Type              |
| baseColour         | Product Color             |
| season             | Target Season             |
| year               | Release Year              |
| usage              | Intended Usage            |
| productDisplayName | Product Name              |
| image              | Product Image             |

### Example Record

| Field        | Value              |
| ------------ | ------------------ |
| Product Name | Nike Running Shoes |
| Category     | Footwear           |
| Color        | Black              |
| Usage        | Sports             |
| Season       | Summer             |


## 5. Project Objectives

### Functional Requirements

1. Upload product image.
2. Generate image embeddings.
3. Retrieve visually similar products.
4. Search using metadata.
5. Generate grounded explanations.
6. Display source citations.
7. Return Top-K results.

### Non-Functional Requirements

1. Retrieval latency under 3 seconds.
2. Top-5 accuracy above 80%.
3. Scalable architecture.
4. Explainable recommendations.
5. Hallucination reduction.

## 6. System Architecture

User Uploads Product Image
            │
            ▼
      OpenCLIP Encoder
            │
            ▼
     Image Embeddings
            │
            ▼
        FAISS Index
            │
            ▼
     Top-K Retrieval
            │
            ▼
     Product Metadata
            │
            ▼
      Context Builder
            │
            ▼
             LLM
            │
            ▼
 Grounded Recommendation

## 7. Expected User Interface

### Home Screen

+------------------------------------------------+
| Multimodal RAG Product Search                  |
+------------------------------------------------+
| Upload Product Image                           |
| [Choose File]                                  |
|                                                |
| Optional Query                                |
| "Find similar products under Sports category" |
|                                                |
| [Search]                                       |
+------------------------------------------------+

### Search Results Screen

+------------------------------------------------+
| Similar Products Found                         |
+------------------------------------------------+

1. Nike Running Shoes
   Similarity Score: 96%
   Category: Footwear

2. Adidas Sports Shoes
   Similarity Score: 94%
   Category: Footwear

3. Puma Running Shoes
   Similarity Score: 92%
   Category: Footwear
```

### AI Explanation Screen

AI Recommendation

The uploaded image appears to be a sports shoe.
The closest matches belong to the Footwear category
and are primarily designed for athletic activities.

Sources:
PROD_1001
PROD_1015
PROD_1043
```


## 8. Core AI Concepts Implemented

| Concept                 | Purpose                     |
| ----------------------- | --------------------------- |
| Computer Vision         | Image Understanding         |
| OpenCLIP                | Image Embeddings            |
| Embeddings              | Vector Representation       |
| Vector Search           | Similarity Retrieval        |
| Cosine Similarity       | Ranking Similar Products    |
| FAISS                   | Vector Database             |
| Metadata Filtering      | Precision Improvement       |
| RAG                     | Grounded Responses          |
| Hallucination Reduction | Reliable Answers            |
| Source Attribution      | Explainability              |
| Re-ranking              | Improved Retrieval Accuracy |
| Evaluation Metrics      | Performance Measurement     |



## 9. Python Libraries Used

### Machine Learning

```python
torch
transformers
sentence-transformers
open-clip-torch
```

### Vector Database

faiss-cpu


### Backend

fastapi
uvicorn


### Frontend

streamlit

### Data Processing

pandas
numpy
pillow


### Evaluation

ragas


## 10. Retrieval-Augmented Generation (RAG)

The system reduces hallucinations by grounding responses in retrieved products and metadata.

### Workflow

1. Retrieve similar products.
2. Retrieve product metadata.
3. Build contextual prompt.
4. Send prompt to LLM.
5. Generate grounded response.
6. Display citations.



## 11. Hallucination Mitigation Strategy

| Technique         | Purpose                    |
| ----------------- | -------------------------- |
| RAG               | Grounded Generation        |
| Product Metadata  | Evidence-Based Responses   |
| Citations         | Traceability               |
| Similarity Search | Accurate Context           |
| Prompt Guardrails | Prevent Unsupported Claims |


## 12. Performance Targets

| Metric              | Target      |
| ------------------- | ----------- |
| Retrieval Latency   | < 3 Seconds |
| Top-5 Accuracy      | > 80%       |
| Availability        | 95%         |
| Citation Coverage   | 100%        |
| Response Generation | < 2 Seconds |


## 13. Project Roadmap

Problem Definition and Architecture

Dataset Ingestion and Metadata Pipeline

Image Embeddings and Text Processing

FAISS Vector Indexing and Hybrid Retrieval

LLM Integration and Hallucination Reduction

Evaluation using RAGAS, Precision@K and NDCG

Deployment, Monitoring, Re-ranking and Optimization



## 14. Repository Structure

multimodal-rag-product-search
│
├── data
├── docs
├── notebooks
├── src
│   └── app.py
├── tests
├── vector_store
├── README.md
├── requirements.txt
└── .gitignore

---



## 15. Future Enhancements

1. Hybrid Search (Image + Text).
2. Cross-Encoder Re-ranking.
3. Pinecone Vector Database.
4. Real-Time Index Refresh.
5. User Feedback Loop.
6. Personalized Recommendations.
7. Production Deployment on Cloud.
8. LangGraph Workflow Orchestration.
9. Multilingual Product Search.
10. Advanced Analytics Dashboard.
