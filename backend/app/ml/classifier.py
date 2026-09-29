import re
import logging
from typing import Dict, Any, List, Optional
from app.ml.embeddings import EmbeddingService

logger = logging.getLogger(__name__)

class MetricStanceClassifier:
    """
    Classifies the stance/usage pattern of bibliometric indicator references
    into:
      - CRITICAL_AWARE: Highlights limitations, cautions against misuse, advocates responsible metrics.
      - NEUTRAL_DESCRIPTIVE: Factual citation counts, standard descriptive metadata.
      - UNCRITICAL_RELIANCE: Uncritical reliance or inappropriate evaluation use (e.g., using JIF to evaluate an individual).
    """

    EXEMPLARS = {
        "CRITICAL_AWARE": [
            "Bibliometric indicators have severe limitations and should not be used in isolation.",
            "Journal impact factor is an inappropriate proxy for the scientific quality of an individual paper.",
            "Citation practices vary drastically between disciplines and require field-normalized evaluation.",
            "Quantitative metrics must always be complemented by qualitative expert peer review.",
            "Using h-index disadvantages early career researchers and ignores non-citation contributions."
        ],
        "UNCRITICAL_RELIANCE": [
            "We evaluated the researchers based purely on their journal impact factors and total citations.",
            "Candidates with an h-index lower than the threshold were filtered out of the tenure review.",
            "The journal impact factor proves the exceptional merit of this individual research article.",
            "Higher citation counts unequivocally denote superior scientific quality regardless of discipline.",
            "Funding decisions should strictly follow the journal ranking metrics."
        ],
        "NEUTRAL_DESCRIPTIVE": [
            "The paper was cited thirty times according to the OpenAlex academic database.",
            "Bibliometric statistics were collected from the Web of Science and Scopus platforms.",
            "Figure 2 illustrates the distribution of publication years and citation numbers in our dataset.",
            "We retrieved metadata including title, author names, publication year, and source venue.",
            "The average number of citations per article in this sample was four point two."
        ]
    }

    def __init__(self):
        self.embedding_service = EmbeddingService()
        self._exemplar_embeddings = {}
        self._precompute_exemplars()

    def _precompute_exemplars(self):
        for stance, texts in self.EXEMPLARS.items():
            self._exemplar_embeddings[stance] = self.embedding_service.encode(texts)

    def classify_sentence(self, sentence: str) -> Dict[str, Any]:
        """
        Classify a single sentence mentioning bibliometric indicators.
        Returns predicted stance, confidence score, and explanation.
        """
        if not sentence or len(sentence.strip()) < 10:
            return {
                "stance": "NEUTRAL_DESCRIPTIVE",
                "confidence": 0.5,
                "label": "Neutral / Descriptive",
                "risk_level": "LOW"
            }

        sent_vec = self.embedding_service.encode(sentence)
        scores = {}

        for stance, exemplar_matrix in self._exemplar_embeddings.items():
            sims = exemplar_matrix.dot(sent_vec)
            # Top-2 average similarity
            top_sims = sorted(sims, reverse=True)[:2]
            scores[stance] = float(sum(top_sims) / len(top_sims))

        # Check explicit keywords that tilt stance
        lower = sentence.lower()
        if any(w in lower for w in ["limitation", "bias", "misuse", "flawed", "responsible", "dora", "leiden", "caution", "context"]):
            scores["CRITICAL_AWARE"] += 0.15

        if any(w in lower for w in ["solely based on", "strictly ranked by", "filtered by impact factor", "proves quality", "h-index cutoff"]):
            scores["UNCRITICAL_RELIANCE"] += 0.20

        predicted_stance = max(scores, key=scores.get)
        confidence = round(scores[predicted_stance], 3)

        label_map = {
            "CRITICAL_AWARE": "Responsible & Context-Aware",
            "NEUTRAL_DESCRIPTIVE": "Neutral / Descriptive",
            "UNCRITICAL_RELIANCE": "Potential Indicator Misuse / Uncritical Reliance"
        }

        risk_map = {
            "CRITICAL_AWARE": "MINIMAL (Good Practice)",
            "NEUTRAL_DESCRIPTIVE": "LOW (Standard Usage)",
            "UNCRITICAL_RELIANCE": "HIGH (Violation of DORA/Leiden Guidelines)"
        }

        return {
            "stance": predicted_stance,
            "confidence": confidence,
            "label": label_map.get(predicted_stance, predicted_stance),
            "risk_level": risk_map.get(predicted_stance, "LOW"),
            "scores": {k: round(v, 3) for k, v in scores.items()}
        }

    def analyze_passages(self, sentences: List[str]) -> List[Dict[str, Any]]:
        """Classify multiple candidate indicator sentences."""
        results = []
        for s in sentences:
            res = self.classify_sentence(s)
            res["sentence"] = s
            results.append(res)
        return results
