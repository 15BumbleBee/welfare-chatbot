SYSTEM_PROMPTS = {
    "en": """You are a friendly welfare scheme assistant for rural India. 
You help people discover government schemes they qualify for.
RULES:
- Keep responses under 160 characters when possible (SMS-friendly)
- Never invent or hallucinate scheme details. Only use information provided to you.
- If you don't know, say "I'm not sure — please visit your nearest CSC center."
- Be warm, simple, and avoid jargon.
- Always end with a clear next action for the user.""",

    "hi": """आप ग्रामीण भारत के लिए एक सरकारी योजना सहायक हैं।
नियम:
- जवाब 160 अक्षरों से कम रखें (SMS के लिए)
- कभी भी योजना की जानकारी न बनाएं। केवल दी गई जानकारी का उपयोग करें।
- अगर पता न हो: "मुझे पक्का नहीं है — नजदीकी CSC केंद्र जाएं।"
- सरल और मित्रवत भाषा का उपयोग करें।""",

    "ta": """நீங்கள் கிராமப்புற இந்தியாவுக்கான அரசு திட்ட உதவியாளர்.
விதிகள்:
- பதில்கள் 160 எழுத்துகளுக்கும் குறைவாக இருக்கட்டும்
- திட்ட தகவல்களை புனைந்து சொல்லாதீர்கள்.
- தெரியாவிட்டால்: "உறுதியாக தெரியவில்லை — அருகில் உள்ள CSC மையம் செல்லுங்கள்."
- எளிமையான மொழி பயன்படுத்துங்கள்."""
}

# Eligibility questions in all 3 languages
QUESTIONS = {
    "en": [
        ("occupation", "What is your main work? (farmer / daily wage / artisan / gig worker / other)"),
        ("residence", "Do you live in a village (rural) or town/city (urban)?"),
        ("gender", "Are you male or female?"),
        ("income", "What is your yearly family income in rupees? (rough estimate)"),
        ("land_hectares", "If farmer: how many hectares of land do you own? (enter 0 if not farmer)"),
        ("is_bpl", "Do you have a BPL (Below Poverty Line) ration card? (yes / no)"),
    ],
    "hi": [
        ("occupation", "आपका मुख्य काम क्या है? (किसान / दिहाड़ी मजदूर / कारीगर / गिग वर्कर / अन्य)"),
        ("residence", "आप गांव में रहते हैं या शहर में? (गांव / शहर)"),
        ("gender", "आप पुरुष हैं या महिला? (पुरुष / महिला)"),
        ("income", "आपकी वार्षिक पारिवारिक आय कितनी है? (अनुमानित रुपयों में)"),
        ("land_hectares", "अगर किसान हैं: आपके पास कितनी हेक्टेयर जमीन है? (0 अगर किसान नहीं)"),
        ("is_bpl", "क्या आपके पास बीपीएल राशन कार्ड है? (हां / नहीं)"),
    ],
    "ta": [
        ("occupation", "உங்கள் தொழில் என்ன? (விவசாயி / கூலி தொழிலாளி / கைவினைஞர் / கிக் ஒர்க்கர் / மற்றவை)"),
        ("residence", "நீங்கள் கிராமத்தில் வசிக்கிறீர்களா நகரத்திலா? (கிராமம் / நகரம்)"),
        ("gender", "நீங்கள் ஆண் அல்லது பெண்? (ஆண் / பெண்)"),
        ("income", "உங்கள் குடும்பத்தின் ஆண்டு வருமானம் எவ்வளவு? (தோராயமாக ரூபாயில்)"),
        ("land_hectares", "விவசாயி எனில்: நீங்கள் எத்தனை ஹெக்டேர் நிலம் வைத்திருக்கிறீர்கள்? (விவசாயி இல்லை எனில் 0)"),
        ("is_bpl", "உங்களிடம் BPL ரேஷன் கார்டு இருக்கிறதா? (ஆம் / இல்லை)"),
    ]
}

GREETINGS = {
    "en": "🙏 Hello! I help you find government schemes you qualify for.\nReply with your language:\n1. हिंदी (Hindi)\n2. தமிழ் (Tamil)\n3. English",
    "hi": "🙏 नमस्ते! मैं आपकी सरकारी योजनाओं को खोजने में मदद करता हूं।\nआइए शुरू करें। आप कुछ सवालों के जवाब दीजिए।",
    "ta": "🙏 வணக்கம்! அரசு திட்டங்கள் கண்டறிய உதவுகிறேன்.\nசில கேள்விகளுக்கு பதில் கூறுங்கள்."
}