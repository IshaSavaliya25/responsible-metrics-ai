import re
import logging
from typing import List, Dict, Any

from app.rules.responsible_metrics_rules import (
    LEIDEN_PRINCIPLES,
    DORA_PRINCIPLES,
    MISUSE_RULES,
    get_remediation_recommendations
)
from app.ml.embeddings import EmbeddingService
from app.ml.classifier import MetricStanceClassifier

logger = logging.getLogger(__name__)


class PrincipleDetectionService:
    """
    Detects adherence to responsible research assessment principles
    (Leiden Manifesto, DORA) and identifies metric misuse violations.
    Combines rule-based pattern matching with dense semantic embeddings
    and stance classification.
    """

    def __init__(self):
        try:
            self.embedding_service = EmbeddingService()
            self.stance_classifier = MetricStanceClassifier()
        except Exception as e:
            logger.warning("Could not initialize embedding/classifier services in PrincipleDetectionService: %s", e)
            self.embedding_service = None
            self.stance_classifier = None

    def split_sentences(self, text: str) -> list:
        if not text:
            return []
        sentences = re.split(r'(?<=[.!?])\s+', text)
        return [
            sentence.strip()
            for sentence in sentences
            if len(sentence.strip()) > 20
        ]

    def find_matching_sentences(self, sentences: list, patterns: list, max_results: int = 5) -> list:
        matches = []
        for sentence in sentences:
            sentence_lower = sentence.lower()
            for pattern in patterns:
                if pattern in sentence_lower:
                    matches.append(sentence)
                    break
            if len(matches) >= max_results:
                break
        return matches

    def detect_responsible_practices(self, text: str) -> list:
        sentences = self.split_sentences(text)
        practices = []

        # 1. MULTIPLE INDICATORS
        patterns = [
            "multiple indicators", "multiple metrics", "combination of indicators",
            "variety of indicators", "different indicators", "several indicators",
            "multidimensional evaluation", "diverse metrics"
        ]
        matches = self.find_matching_sentences(sentences, patterns)
        if matches:
            practices.append({
                "category": "multiple_indicators",
                "principle": "Use multiple indicators instead of relying on a single metric.",
                "severity": "positive",
                "evidence": matches
            })

        # 2. QUALITATIVE EVIDENCE
        patterns = [
            "peer review", "qualitative evidence", "qualitative assessment",
            "expert judgment", "narrative assessment", "human evaluation",
            "portfolio evaluation"
        ]
        matches = self.find_matching_sentences(sentences, patterns)
        if matches:
            practices.append({
                "category": "qualitative_evidence",
                "principle": "Combine quantitative metrics with qualitative evidence.",
                "severity": "positive",
                "evidence": matches
            })

        # 3. CONTEXT AWARENESS & FIELD NORMALIZATION
        patterns = [
            "disciplinary differences", "discipline-specific", "field-specific",
            "research context", "publication age", "career stage",
            "contextual differences", "field normalization", "field-weighted"
        ]
        matches = self.find_matching_sentences(sentences, patterns)
        if matches:
            practices.append({
                "category": "context_awareness",
                "principle": "Account for disciplinary variation and career stage context.",
                "severity": "positive",
                "evidence": matches
            })

        # 4. METRIC LIMITATIONS
        patterns = [
            "limitation of citations", "citation bias", "limitations of h-index",
            "metric limitations", "caveat", "skewed citation distribution",
            "should not be used blindly", "goodhart"
        ]
        matches = self.find_matching_sentences(sentences, patterns)
        if matches:
            practices.append({
                "category": "metric_limitations",
                "principle": "Acknowledge limitations of bibliometric indicators.",
                "severity": "positive",
                "evidence": matches
            })

        # 5. TRANSPARENCY & OPEN DATA
        patterns = [
            "transparent methodology", "transparency", "clearly defined",
            "open methodology", "reproducible evaluation", "open data",
            "open access", "openalex", "data availability"
        ]
        matches = self.find_matching_sentences(sentences, patterns)
        if matches:
            practices.append({
                "category": "transparency",
                "principle": "Use transparent and reproducible evaluation methods.",
                "severity": "positive",
                "evidence": matches
            })

        # 6. SEMANTIC PRINCIPLE ALIGNMENT (LEIDEN & DORA)
        if self.embedding_service and len(sentences) > 0:
            try:
                # Sample up to 30 sentences for efficiency
                sampled_sentences = sentences[:35]
                for code, p_data in LEIDEN_PRINCIPLES.items():
                    # check if this principle is already represented
                    p_query = f"{p_data['title']}. {p_data['description']}"
                    ranked = self.embedding_service.rank_by_similarity(p_query, sampled_sentences, top_k=1)
                    if ranked and ranked[0][1] >= 0.65:
                        matched_sent = sampled_sentences[ranked[0][0]]
                        if not any(matched_sent in p["evidence"] for p in practices):
                            practices.append({
                                "category": f"leiden_{code.lower()}",
                                "principle": f"{code}: {p_data['title']}",
                                "severity": "positive",
                                "evidence": [matched_sent]
                            })
            except Exception as e:
                logger.debug("Semantic principle check skipped: %s", e)

        return practices

    def detect_metric_misuse(self, text: str) -> list:
        sentences = self.split_sentences(text)
        misuse_cases = []

        # 1. SINGLE METRIC DEPENDENCY
        patterns = [
            "only citation count", "solely based on citations", "based only on citations",
            "only based on h-index", "solely on the h-index", "single metric cutoff",
            "solely evaluated by citation"
        ]
        matches = self.find_matching_sentences(sentences, patterns)
        if matches:
            misuse_cases.append({
                "category": "single_metric_dependency",
                "severity": "high",
                "message": "Potential over-reliance on a single bibliometric indicator.",
                "evidence": matches
            })

        # 2. JOURNAL IMPACT FACTOR MISUSE (DORA VIOLATION)
        patterns = [
            "impact factor determines", "journal impact factor determines",
            "quality based on impact factor", "research quality based on journal",
            "high impact factor means high quality", "selected based on impact factor"
        ]
        matches = self.find_matching_sentences(sentences, patterns)
        if matches:
            misuse_cases.append({
                "category": "journal_metric_misuse",
                "severity": "high",
                "message": "Potential misuse of journal-level metrics for evaluating individual research (DORA violation).",
                "evidence": matches
            })

        # 3. RESEARCHER RANKING BY RAW METRICS
        patterns = [
            "rank researchers by citation", "ranking researchers by citations",
            "ranked according to h-index", "rank researchers based on",
            "researcher ranking based on citation"
        ]
        matches = self.find_matching_sentences(sentences, patterns)
        if matches:
            misuse_cases.append({
                "category": "researcher_ranking",
                "severity": "medium",
                "message": "Inappropriate ranking of individual researchers based purely on citation metrics.",
                "evidence": matches
            })

        # 4. CROSS-FIELD UNNORMALIZED COMPARISONS
        patterns = [
            "compare citations across disciplines", "compared citations between fields",
            "citations across different disciplines without", "cross-field citation comparison"
        ]
        matches = self.find_matching_sentences(sentences, patterns)
        if matches:
            misuse_cases.append({
                "category": "cross_field_comparison",
                "severity": "high",
                "message": "Comparison of citation metrics across distinct disciplines without normalization.",
                "evidence": matches
            })

        # 5. FORMAL RULE-BASED REGEX MISUSE RULES
        for rule in MISUSE_RULES:
            rule_matches = []
            for sent in sentences:
                for pat in rule["regex_patterns"]:
                    if re.search(pat, sent, re.IGNORECASE):
                        rule_matches.append(sent)
                        break
            if rule_matches and not any(m.get("id") == rule["id"] for m in misuse_cases):
                misuse_cases.append({
                    "id": rule["id"],
                    "category": rule["id"].lower(),
                    "severity": rule["severity"].lower(),
                    "message": f"{rule['name']} ({rule['framework']})",
                    "explanation": rule["explanation"],
                    "remediation": rule["remediation"],
                    "evidence": rule_matches[:3]
                })

        # 6. STANCE CLASSIFIER DETECTION
        if self.stance_classifier and sentences:
            try:
                candidate_sents = [s for s in sentences if any(w in s.lower() for w in ["impact factor", "h-index", "citation count", "ranking"])]
                for cand in candidate_sents[:10]:
                    classification = self.stance_classifier.classify_sentence(cand)
                    if classification["stance"] == "UNCRITICAL_RELIANCE" and classification["confidence"] >= 0.65:
                        if not any(cand in m.get("evidence", []) for m in misuse_cases):
                            misuse_cases.append({
                                "category": "uncritical_reliance",
                                "severity": "high",
                                "message": f"Sentence exhibits uncritical reliance on metric: {classification['label']}",
                                "evidence": [cand]
                            })
            except Exception as e:
                logger.debug("Stance classifier check skipped: %s", e)

        return misuse_cases

    def generate_recommendations(self, practices: list, misuse_cases: list) -> list:
        recommendations = []
        detected_practices = [item.get("category", "") for item in practices]
        detected_misuse = [item.get("category", "") for item in misuse_cases]

        if "multiple_indicators" not in detected_practices:
            recommendations.append("Use multiple bibliometric indicators instead of relying on a single metric.")

        if "qualitative_evidence" not in detected_practices:
            recommendations.append("Include qualitative evidence such as peer review, research narratives, or expert assessment.")

        if "context_awareness" not in detected_practices:
            recommendations.append("Consider discipline, publication year, career stage, and research context.")

        if "metric_limitations" not in detected_practices:
            recommendations.append("Explicitly discuss the limitations and potential biases of bibliometric indicators.")

        if "single_metric_dependency" in detected_misuse:
            recommendations.append("Avoid making evaluation decisions based on only one bibliometric metric.")

        if "journal_metric_misuse" in detected_misuse:
            recommendations.append("Do not use journal-level metrics such as impact factor to directly evaluate individual researchers (DORA Principle 1).")

        if "cross_field_comparison" in detected_misuse:
            recommendations.append("Normalize bibliometric indicators (e.g. FWCI) before comparing different research disciplines.")

        # Enrich with remediation recommendations from formal rules
        formal_recs = get_remediation_recommendations(misuse_cases, 70.0)
        for rec in formal_recs:
            rec_text = f"[{rec['priority']}] {rec['target']}: {rec['action']}"
            if rec_text not in recommendations:
                recommendations.append(rec_text)

        return recommendations

    def calculate_compliance_score(self, practices: list, misuse_cases: list) -> int:
        score = 50
        score += len(practices) * 7

        for misuse in misuse_cases:
            severity = str(misuse.get("severity", "medium")).lower()
            if severity == "high":
                score -= 15
            elif severity == "medium":
                score -= 10
            else:
                score -= 5

        return max(0, min(score, 100))

    def analyze(self, text: str) -> dict:
        practices = self.detect_responsible_practices(text)
        misuse_cases = self.detect_metric_misuse(text)
        recommendations = self.generate_recommendations(practices, misuse_cases)
        compliance_score = self.calculate_compliance_score(practices, misuse_cases)

        return {
            "responsible_practices": practices,
            "potential_misuse": misuse_cases,
            "recommendations": recommendations,
            "compliance_score": compliance_score
        }