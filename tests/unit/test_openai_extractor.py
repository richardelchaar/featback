from featback.llm.openai_extractor import extract_features

def test_llm_fail_soft(monkeypatch):
    from featback.llm import openai_extractor as oe
    def blow(*a, **k): 
        raise RuntimeError("boom")
    monkeypatch.setattr(oe.client.chat.completions, "create", blow, raising=True)
    assert extract_features("t","text","prod") == []
