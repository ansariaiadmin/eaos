from packages.legal.rag_agent import LegalRAGAgent

def test_rag_cites():
    a = LegalRAGAgent().answer("data minimization obligations")
    assert a["citations"] and any("GDPR" in c for c in a["citations"])

def test_rag_local_only():
    a = LegalRAGAgent().answer("suspicious transaction reporting")
    assert a["route"]["provider"] == "local"
