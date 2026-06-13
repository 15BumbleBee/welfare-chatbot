import json
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from schemes_data import SCHEMES

# Use a multilingual model that supports Indic languages
MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

class RAGEngine:
    def __init__(self):
        self.model = SentenceTransformer(MODEL_NAME)
        self.schemes = SCHEMES
        self.embeddings = None
        self._build_index()

    def _build_index(self):
        """Embed all scheme descriptions + tags for retrieval."""
        texts = []
        for s in self.schemes:
            # Combine multiple fields for richer embedding
            text = f"{s['name']}. {s['description']} Tags: {', '.join(s['tags'])}"
            texts.append(text)
        self.embeddings = self.model.encode(texts, convert_to_numpy=True)
        print(f"[RAG] Indexed {len(self.schemes)} schemes.")

    def retrieve(self, query: str, top_k: int = 3) -> list[dict]:
        """Return top_k most relevant schemes for a query."""
        query_vec = self.model.encode([query], convert_to_numpy=True)
        scores = cosine_similarity(query_vec, self.embeddings)[0]
        top_indices = np.argsort(scores)[::-1][:top_k]
        results = []
        for idx in top_indices:
            scheme = self.schemes[idx].copy()
            scheme["_score"] = float(scores[idx])
            results.append(scheme)
        return results

    def get_by_id(self, scheme_id: str) -> dict | None:
        return next((s for s in self.schemes if s["id"] == scheme_id), None)

    def filter_by_eligibility(self, user_profile: dict) -> list[dict]:
        """
        Rule-based eligibility filter.
        user_profile keys: occupation, gender, age, residence, income, land_hectares, has_lpg
        """
        matched = []
        occ = user_profile.get("occupation", "").lower()
        gender = user_profile.get("gender", "").lower()
        age = user_profile.get("age", 30)
        residence = user_profile.get("residence", "rural").lower()
        income = user_profile.get("income", 0)
        land = user_profile.get("land_hectares", 0)
        has_lpg = user_profile.get("has_lpg", False)
        is_bpl = user_profile.get("is_bpl", False)

        for s in self.schemes:
            elig = s.get("eligibility", {})
            score = 0

            # PM-KISAN: farmer with land ≤2ha
            if s["id"] == "pm_kisan":
                if "farmer" in occ and land > 0 and land <= 2.0 and residence == "rural":
                    score = 3

            # Ayushman Bharat: low income
            elif s["id"] == "ayushman_bharat":
                if income < 300000 or is_bpl:
                    score = 3

            # PMAY Gramin: rural + no pucca house
            elif s["id"] == "pmay_gramin":
                if residence == "rural" and user_profile.get("house_type", "") in ["kutcha", "houseless"]:
                    score = 3

            # Ujjwala: female + BPL + no LPG
            elif s["id"] == "ujjwala":
                if gender == "female" and is_bpl and not has_lpg:
                    score = 3

            # MGNREGA: any rural adult
            elif s["id"] == "nrega":
                if residence == "rural" and age >= 18:
                    score = 2

            # Sukanya Samriddhi: has girl child under 10
            elif s["id"] == "sukanya_samriddhi":
                if user_profile.get("has_girl_child_under_10", False):
                    score = 3

            # PM Vishwakarma: artisans
            elif s["id"] == "pm_vishwakarma":
                artisan_occupations = ["carpenter", "blacksmith", "potter", "weaver", "goldsmith",
                                       "cobbler", "tailor", "barber", "mason", "washerman", "artisan", "craft"]
                if any(a in occ for a in artisan_occupations):
                    score = 3

            # e-Shram: gig/unorganized workers
            elif s["id"] == "e_shram":
                unorganized = ["gig", "daily wage", "construction", "domestic", "vendor", "labor", "labourer"]
                if any(u in occ for u in unorganized) and 16 <= age <= 59:
                    score = 3

            # SVAMITVA: rural property owner
            elif s["id"] == "pm_svamitva":
                if residence == "rural":
                    score = 1

            if score > 0:
                result = s.copy()
                result["_eligibility_score"] = score
                matched.append(result)

        # Sort by score descending
        matched.sort(key=lambda x: x["_eligibility_score"], reverse=True)
        return matched

# Singleton
rag = RAGEngine()