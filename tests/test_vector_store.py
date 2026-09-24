"""Tests for vector store lite Phase 12."""
from packages.legal.rag_agent import LegalRAGAgent
from packages.legal.vector_store import VectorStoreLite, cosine, embed


def test_embed_deterministic():
    e1 = embed("data minimization")
    e2 = embed("data minimization")
    assert e1 == e2
    assert len(e1) == 64

def test_embed_normalized():
    import math
    e = embed("hello world test")
    norm = math.sqrt(sum(x*x for x in e))
    assert abs(norm - 1.0) < 1e-6 or norm == 0.0

def test_cosine_identical():
    e = embed("GDPR data minimization")
    assert abs(cosine(e, e) - 1.0) < 1e-6

def test_cosine_different():
    e1 = embed("GDPR data minimization")
    e2 = embed("financial reporting internal controls")
    # Different texts should have lower similarity than identical
    assert cosine(e1, e2) < 1.0

def test_vector_store_search():
    store = VectorStoreLite()
    store.add_docs([
        {"id": "A", "text": "data minimization requires processing only necessary personal data"},
        {"id": "B", "text": "internal controls over financial reporting must be assessed annually"},
    ])
    hits = store.search("data minimization personal data", k=1)
    assert len(hits) >= 1
    assert hits[0]["id"] == "A"
    assert hits[0]["method"] == "vector"

def test_vector_store_empty():
    store = VectorStoreLite()
    hits = store.search("anything", k=3)
    assert hits == []

def test_vector_store_fallback_lexical():
    # LegalRAGAgent should fallback to lexical when vector fails
    agent = LegalRAGAgent(use_vector=True)
    # Clear vector store to force fallback
    agent.vstore.clear()
    ans = agent.answer("data minimization")
    assert ans["citations"]
    assert ans["retrieval_method"] in ("lexical", "vector")

def test_rag_vector_method():
    agent = LegalRAGAgent(use_vector=True)
    ans = agent.answer("suspicious transaction reporting AML")
    assert ans["citations"]
    assert "retrieval_method" in ans
    assert ans["retrieval_method"] in ("vector", "lexical")
    assert "scores" in ans

def test_rag_lexical_still_works():
    agent = LegalRAGAgent(use_vector=False)
    ans = agent.answer("consumers have right to delete personal information")
    assert any("CCPA" in c for c in ans["citations"])
