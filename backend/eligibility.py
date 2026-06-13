import re

def parse_user_answer(field: str, raw_answer: str, lang: str) -> any:
    """Parse natural language answers into structured data."""
    text = raw_answer.lower().strip()

    if field == "occupation":
        if any(w in text for w in ["farmer", "kisan", "किसान", "விவசாய"]):
            return "farmer"
        if any(w in text for w in ["artisan", "craft", "carpenter", "potter", "weaver",
                                    "कारीगर", "carpenter", "கைவினை"]):
            return "artisan"
        if any(w in text for w in ["gig", "delivery", "ola", "swiggy", "uber", "gig"]):
            return "gig worker"
        if any(w in text for w in ["daily", "labour", "labourer", "mazdoor", "मजदूर", "கூலி"]):
            return "daily wage"
        return "other"

    elif field == "residence":
        if any(w in text for w in ["rural", "village", "gram", "gaon", "गांव", "கிராம"]):
            return "rural"
        return "urban"

    elif field == "gender":
        if any(w in text for w in ["female", "woman", "mahila", "महिला", "பெண்", "f", "2"]):
            return "female"
        return "male"

    elif field == "income":
        # Extract number from text like "50000", "50k", "1.5 lakh"
        text_clean = text.replace(",", "").replace(" ", "")
        lakh_match = re.search(r"(\d+\.?\d*)\s*lakh", text)
        if lakh_match:
            return float(lakh_match.group(1)) * 100000
        k_match = re.search(r"(\d+)\s*k", text)
        if k_match:
            return float(k_match.group(1)) * 1000
        num_match = re.search(r"\d+", text_clean)
        if num_match:
            val = int(num_match.group())
            # Handle short forms like "50" meaning 50,000
            if val < 1000:
                val *= 1000
            return float(val)
        return 0

    elif field == "land_hectares":
        num_match = re.search(r"(\d+\.?\d*)", text.replace(",", ""))
        if num_match:
            return float(num_match.group(1))
        return 0.0

    elif field == "is_bpl":
        if any(w in text for w in ["yes", "haan", "ha", "हां", "ஆம்", "y", "1"]):
            return True
        return False

    return raw_answer