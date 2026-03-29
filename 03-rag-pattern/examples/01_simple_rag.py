"""
Module 03 - Example 1: Simple RAG from Scratch
================================================
Build a complete RAG pipeline using only Python + OpenAI.
No frameworks — understand every component.

Pain Point Solved: LLM hallucination and knowledge cutoff.

Requirements:
    pip install openai numpy
"""

import sys
import os
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from utils.llm_client import get_client, get_model, get_embedding_model

client = get_client()

# ============================================
# STEP 1: Our "Knowledge Base" — simple documents
# ============================================
KNOWLEDGE_BASE = [
    {
        "id": 1,
        "title": "Company Leave Policy",
        "content": """Annual Leave Policy (Updated January 2025):
        - Full-time employees receive 20 days of paid annual leave per year.
        - Leave accrues at 1.67 days per month.
        - Unused leave can carry over up to 5 days to the next year.
        - Leave requests must be submitted at least 2 weeks in advance.
        - During peak season (November-December), leave is limited to 3 days.""",
    },
    {
        "id": 2,
        "title": "Remote Work Policy",
        "content": """Remote Work Policy (Updated March 2025):
        - Employees may work remotely up to 3 days per week.
        - Core hours are 10 AM to 3 PM in your local timezone.
        - A stable internet connection (minimum 50 Mbps) is required.
        - Remote workers must be available on Slack during core hours.
        - Team meetings on Tuesdays and Thursdays are mandatory in-office.""",
    },
    {
        "id": 3,
        "title": "Expense Reimbursement",
        "content": """Expense Policy (Updated February 2025):
        - Meals during business travel: up to $75 per day.
        - Hotel accommodation: up to $200 per night (domestic), $300 (international).
        - Flight bookings must be economy class for trips under 6 hours.
        - All expenses must be submitted within 30 days with receipts.
        - Home office equipment allowance: $1,000 per year.""",
    },
    {
        "id": 4,
        "title": "Performance Review Process",
        "content": """Performance Review Cycle (2025):
        - Reviews are conducted bi-annually in June and December.
        - Self-assessment is due 2 weeks before the review meeting.
        - Rating scale: 1 (Needs Improvement) to 5 (Exceptional).
        - Promotion eligibility requires a rating of 4+ for two consecutive cycles.
        - 360-degree feedback is collected from at least 3 peers.""",
    },
]


# ============================================
# STEP 2: Create embeddings for documents
# ============================================
def get_embedding(text: str) -> list[float]:
    """Convert text to a vector embedding using OpenAI."""
    response = client.embeddings.create(
        model=get_embedding_model(),
        input=text,
    )
    return response.data[0].embedding


def cosine_similarity(a: list[float], b: list[float]) -> float:
    """Calculate cosine similarity between two vectors."""
    a, b = np.array(a), np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


# ============================================
# STEP 3: Build the vector store (in-memory)
# ============================================
class SimpleVectorStore:
    """A minimal vector store — just a list of documents with embeddings."""

    def __init__(self):
        self.documents = []
        self.embeddings = []

    def add_document(self, doc: dict, embedding: list[float]):
        self.documents.append(doc)
        self.embeddings.append(embedding)

    def search(self, query_embedding: list[float], top_k: int = 2) -> list[dict]:
        """Find the most similar documents to the query."""
        similarities = [
            cosine_similarity(query_embedding, doc_emb)
            for doc_emb in self.embeddings
        ]
        # Get indices of top-K most similar documents
        top_indices = np.argsort(similarities)[-top_k:][::-1]
        return [
            {**self.documents[i], "similarity": similarities[i]}
            for i in top_indices
        ]


# ============================================
# STEP 4: RAG query function
# ============================================
def rag_query(question: str, vector_store: SimpleVectorStore) -> str:
    """Complete RAG pipeline: retrieve → augment → generate."""

    # Step 4a: Embed the question
    query_embedding = get_embedding(question)

    # Step 4b: Retrieve relevant documents
    relevant_docs = vector_store.search(query_embedding, top_k=2)

    # Step 4c: Build augmented prompt
    context = "\n\n".join(
        f"[Source: {doc['title']}]\n{doc['content']}" for doc in relevant_docs
    )

    augmented_prompt = f"""Answer the question based ONLY on the provided context. 
If the answer is not in the context, say "I don't have information about that."
Always cite which source document you used.

Context:
{context}

Question: {question}

Answer:"""

    # Step 4d: Generate answer using LLM
    response = client.chat.completions.create(
        model=get_model(),
        messages=[{"role": "user", "content": augmented_prompt}],
        temperature=0.0,
    )

    answer = response.choices[0].message.content

    # Include retrieval info for transparency
    sources = [f"  - {doc['title']} (similarity: {doc['similarity']:.3f})"
               for doc in relevant_docs]

    return f"{answer}\n\n📚 Sources retrieved:\n" + "\n".join(sources)


# ============================================
# STEP 5: Main — Put it all together
# ============================================
def main():
    print("=" * 60)
    print("BUILDING RAG PIPELINE")
    print("=" * 60)

    # Index documents
    print("\n📥 Indexing documents...")
    store = SimpleVectorStore()
    for doc in KNOWLEDGE_BASE:
        embedding = get_embedding(doc["content"])
        store.add_document(doc, embedding)
        print(f"  ✅ Indexed: {doc['title']}")

    # Test queries
    questions = [
        "How many days of annual leave do I get?",
        "Can I work from home? What are the rules?",
        "What's the maximum hotel cost for international travel?",
        "How do promotions work here?",
        "What's the company's policy on cryptocurrency investments?",  # Not in KB
    ]

    for question in questions:
        print(f"\n{'=' * 60}")
        print(f"❓ Question: {question}")
        print("-" * 60)
        answer = rag_query(question, store)
        print(answer)

    print(f"\n{'=' * 60}")
    print("KEY TAKEAWAYS:")
    print("=" * 60)
    print("""
    ✅ Answers are grounded in actual documents
    ✅ Sources are cited for transparency
    ✅ "I don't know" for questions outside the knowledge base
    ✅ No hallucination — facts come from real documents
    
    ❌ But RAG is read-only — it can't UPDATE documents
    ❌ One-shot retrieval — can't do follow-up searches
    ❌ Can't take actions — just reads and answers
    
    → Module 04 (Tools) and Module 05 (ReAct) solve these!
    """)


if __name__ == "__main__":
    main()
