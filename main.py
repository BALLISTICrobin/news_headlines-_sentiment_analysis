from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline

# Initialize FastAPI app
app = FastAPI(title="Travel News Sentiment API", version="1.0")

# Load Hugging Face zero-shot classification pipeline
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

# Define candidate labels for sentiment
labels = ["POSITIVE", "NEGATIVE", "NEUTRAL"]

# Define request body schema
class TextInput(BaseModel):
    text: str

@app.post("/analyze_travel_news")
async def analyze_travel_news(input: TextInput):
    """
    Analyze whether the input news text is POSITIVE, NEGATIVE, or NEUTRAL.
    """
    result = classifier(input.text, candidate_labels=labels)
    return {
        "news_text": input.text,
        "label": result["labels"][0],
        "score": float(result["scores"][0])
    }

@app.get("/")
async def root():
    return {"message": "Welcome to the Travel News Sentiment API! Use /analyze_travel_news with POST."}
