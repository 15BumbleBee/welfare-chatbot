import os
import json
import asyncio
from fastapi import FastAPI, Request, Response
from fastapi.responses import PlainTextResponse
from twilio.rest import Client as TwilioClient
from twilio.twiml.messaging_response import MessagingResponse

from rag_engine import rag
from session_store import get_session, save_session, clear_session
from llm_client import call_llm, detect_language
from eligibility import parse_user_answer
from prompts import SYSTEM_PROMPTS, QUESTIONS, GREETINGS

app = FastAPI()

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER", "whatsapp:+14155238886")


def format_scheme_summary(scheme: dict, lang: str) -> str:
    """Format a scheme as a short SMS-friendly message."""
    name_key = f"name_{lang}" if f"name_{lang}" in scheme else "name"
    name = scheme.get(name_key, scheme["name"])
    desc = scheme["description"]
    # Keep under 160 chars for SMS
    return f"✅ *{name}*\n{desc[:120]}...\nReply with scheme number for documents needed."


def format_document_checklist(scheme: dict, lang: str) -> str:
    """Format document checklist in user's language."""
    name_key = f"name_{lang}" if f"name_{lang}" in scheme else "name"
    docs_key = f"documents_{lang}" if f"documents_{lang}" in scheme else "documents"
    name = scheme.get(name_key, scheme["name"])
    docs = scheme.get(docs_key, scheme["documents"])
    checklist = "\n".join(f"  {i+1}. {d}" for i, d in enumerate(docs))

    labels = {
        "en": f"📋 *Documents for {name}:*\n{checklist}\n\nApply at: {scheme['apply_url']}",
        "hi": f"📋 *{name} के लिए दस्तावेज़:*\n{checklist}\n\nआवेदन: {scheme['apply_url']}",
        "ta": f"📋 *{name} ஆவணங்கள்:*\n{checklist}\n\nவிண்ணப்பிக்க: {scheme['apply_url']}"
    }
    return labels.get(lang, labels["en"])


async def process_message(session_id: str, user_msg: str) -> str:
    """Core state machine for conversation flow."""
    session = get_session(session_id)
    lang = session["language"]

    # Detect language switch
    detected_lang = await detect_language(user_msg)
    if detected_lang != "en" and session["state"] == "greeting":
        lang = detected_lang
        session["language"] = lang

    # Handle language selection in greeting
    if session["state"] == "greeting":
        if user_msg.strip() in ["1", "hindi", "हिंदी"]:
            session["language"] = "hi"
            lang = "hi"
        elif user_msg.strip() in ["2", "tamil", "தமிழ்"]:
            session["language"] = "ta"
            lang = "ta"
        elif user_msg.strip() in ["3", "english"]:
            session["language"] = "en"
            lang = "en"

        session["state"] = "collecting"
        session["step"] = 0
        save_session(session)
        # Ask first question
        _, question = QUESTIONS[lang][0]
        return question

    # Eligibility collection flow
    if session["state"] == "collecting":
        step = session["step"]
        questions = QUESTIONS[lang]

        if step > 0:
            # Parse and store previous answer
            field, _ = questions[step - 1]
            parsed = parse_user_answer(field, user_msg, lang)
            session["user_profile"][field] = parsed

        if step < len(questions):
            _, next_question = questions[step]
            session["step"] += 1
            save_session(session)
            return next_question
        else:
            # All questions answered — compute eligibility
            session["state"] = "results"
            matched = rag.filter_by_eligibility(session["user_profile"])
            session["matched_schemes"] = [s["id"] for s in matched]
            save_session(session)

            if not matched:
                no_match = {
                    "en": "😔 Based on your answers, no exact matches found. Visit myscheme.gov.in or your nearest CSC center for more help.",
                    "hi": "😔 आपके जवाबों के आधार पर कोई योजना नहीं मिली। myscheme.gov.in या नजदीकी CSC केंद्र जाएं।",
                    "ta": "😔 உங்கள் பதில்களை வைத்து எந்த திட்டமும் கிடைக்கவில்லை. myscheme.gov.in அல்லது அருகில் உள்ள CSC மையத்தை தொடர்பு கொள்ளுங்கள்."
                }
                return no_match[lang]

            # Build results message
            header = {"en": "🎯 You may qualify for these schemes:", "hi": "🎯 आप इन योजनाओं के लिए पात्र हो सकते हैं:", "ta": "🎯 நீங்கள் இந்த திட்டங்களுக்கு தகுதியானவராக இருக்கலாம்:"}
            lines = [header[lang]]
            for i, s in enumerate(matched[:5], 1):
                name_key = f"name_{lang}" if f"name_{lang}" in s else "name"
                lines.append(f"{i}. {s.get(name_key, s['name'])}")
            footer = {"en": "\nReply with a number (1-5) to get required documents.", "hi": "\nदस्तावेज़ जानने के लिए नंबर भेजें (1-5).", "ta": "\nஆவணங்கள் தெரிய எண் அனுப்புங்கள் (1-5)."}
            lines.append(footer[lang])
            return "\n".join(lines)

    # Document detail state
    if session["state"] == "results":
        try:
            choice = int(user_msg.strip()) - 1
            scheme_ids = session["matched_schemes"]
            if 0 <= choice < len(scheme_ids):
                scheme = rag.get_by_id(scheme_ids[choice])
                if scheme:
                    session["state"] = "doc_detail"
                    save_session(session)
                    checklist = format_document_checklist(scheme, lang)
                    steps_label = {"en": f"\n\n📝 How to apply:\n{scheme['apply_steps']}", "hi": f"\n\n📝 आवेदन कैसे करें:\n{scheme['apply_steps']}", "ta": f"\n\n📝 விண்ணப்பிப்பது எப்படி:\n{scheme['apply_steps']}"}
                    more = {"en": "\n\nType 'menu' to check other schemes or 'restart' to start over.", "hi": "\n\n'menu' टाइप करें अन्य योजनाओं के लिए, 'restart' से फिर शुरू करें।", "ta": "\n\n'menu' என்று தட்டச்சு செய்யுங்கள் மேலும் திட்டங்களுக்கு."}
                    return checklist + steps_label[lang] + more[lang]
        except (ValueError, IndexError):
            pass

        # Use RAG+LLM for free-form questions about schemes
        context_schemes = [rag.get_by_id(sid) for sid in session["matched_schemes"][:3]]
        context_text = json.dumps([{
            "name": s["name"], "description": s["description"],
            "documents": s["documents"], "apply_url": s["apply_url"]
        } for s in context_schemes if s], ensure_ascii=False)

        messages = session["history"][-6:] + [{"role": "user", "content": user_msg}]
        system = SYSTEM_PROMPTS[lang] + f"\n\nAvailable scheme data (ONLY use this):\n{context_text}"

        response = await call_llm(messages, system_prompt=system, max_tokens=250)
        session["history"].append({"role": "user", "content": user_msg})
        session["history"].append({"role": "assistant", "content": response})
        save_session(session)
        return response

    # Handle restart
    if "restart" in user_msg.lower() or "फिर" in user_msg or "மறுதொடக்கம்" in user_msg:
        clear_session(session_id)
        return GREETINGS["en"]

    # Default: LLM fallback
    messages = [{"role": "user", "content": user_msg}]
    return await call_llm(messages, system_prompt=SYSTEM_PROMPTS[lang], max_tokens=200)


# ── WhatsApp Webhook (Twilio) ─────────────────────────────────────────────────

@app.post("/webhook/whatsapp")
async def whatsapp_webhook(request: Request):
    form = await request.form()
    user_msg = form.get("Body", "").strip()
    from_number = form.get("From", "")  # e.g. whatsapp:+919876543210
    session_id = from_number.replace("whatsapp:", "").replace("+", "")

    # First-time greeting
    session = get_session(session_id)
    if session["state"] == "greeting" and not user_msg:
        reply = GREETINGS["en"]
    else:
        reply = await process_message(session_id, user_msg)

    twiml = MessagingResponse()
    twiml.message(reply)
    return Response(content=str(twiml), media_type="application/xml")


# ── REST API for testing without WhatsApp ─────────────────────────────────────

@app.post("/chat")
async def chat_endpoint(request: Request):
    """Test endpoint — send JSON: {"session_id": "test123", "message": "hello"}"""
    body = await request.json()
    session_id = body.get("session_id", "test")
    user_msg = body.get("message", "")

    session = get_session(session_id)
    if not user_msg:
        return {"reply": GREETINGS["en"], "session": session["state"]}

    reply = await process_message(session_id, user_msg)
    return {"reply": reply, "session": get_session(session_id)["state"]}


@app.get("/health")
async def health():
    return {"status": "ok", "schemes_indexed": len(rag.schemes)}