from featback.llm.openai_extractor import extract_features


def test_llm_fail_soft(monkeypatch):
    from featback.llm import openai_extractor as oe
    
    class DummyCompletions:
        def create(self, *args, **kwargs):
            raise RuntimeError("boom")
    
    class DummyChat:
        def __init__(self):
            self.completions = DummyCompletions()
    
    class DummyClient:
        def __init__(self):
            self.chat = DummyChat()
    
    monkeypatch.setattr(oe, "client", DummyClient())
    assert extract_features("title", "text", "product") == []
