import os
import httpx
from typing import Optional

# Supports Groq (fast, free tier) or OpenAI-compatible APIs
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = "llama3-8b-8192"  # Fast, multilingual, free tier
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

async def call_llm(messages: list[dict], system_prompt: str, max_tokens: int = 300) -> str:
    """
    Call LLM with conversation history.
    Keeps responses short for low-bandwidth (max_tokens=300).
    """
    payload = {
        "model": GROQ_MODEL,
        "messages": [{"role": "system", "content": system_prompt}] + messages,
        "max_tokens": max_tokens,
        "temperature": 0.3,  # Low temp = more factual, less hallucination
    }
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    async with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.post(GROQ_URL, json=payload, headers=headers)
        resp.raise_for_status()
        data = resp.json()
        return data["choices"][0]["message"]["content"].strip()

async def detect_language(text: str) -> str:
    """Detect if user is writing in hi, ta, or en."""
    # Simple heuristic: check for Devanagari or Tamil Unicode ranges
    devanagari = sum(1 for c in text if '\u0900' <= c <= '\u097F')
    tamil = sum(1 for c in text if '\u0B80' <= c <= '\u0BFF')
    if devanagari > 2:
        return "hi"
    if tamil > 2:
        return "ta"
    return "en"