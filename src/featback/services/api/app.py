from fastapi import FastAPI
from pydantic import BaseModel

from featback.llm.openai_extractor import extract_features

app = FastAPI(title="Featback API")

class ExtractRequest(BaseModel):
    text: str
    product: str | None = None
    title: str | None = ""

class ExtractItem(BaseModel):
    type: str
    category: str
    feature: str
    emotion: str | None = None
    reason: str

class ExtractResponse(BaseModel):
    items: list[ExtractItem]
    source: str

@app.get("/health")
def health(): 
    return {"ok": True}

@app.post("/extract", response_model=ExtractResponse)
def extract(req: ExtractRequest):
    items = extract_features(req.title or "", req.text or "", req.product or "")
    return {"items": items, "source": "llm"}
