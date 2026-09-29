import os
import json
import numpy as np

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class ResearchGapService:

    def __init__(self):

        BASE_DIR = os.path.dirname(
            os.path.dirname(
                os.path.dirname(
                    os.path.abspath(__file__)
                )
            )
        )

        self.dataset_path = os.path.join(
            BASE_DIR,
            "data",
            "literature",
            "literature_dataset.json"
        )

        self.literature = self.load_literature()

    # ==========================================
    # LOAD LITERATURE DATASET
    # ==========================================

    def load_literature(self):
        try:
            # 1. Check for standard curated domain benchmark dataset
            if os.path.exists(self.dataset_path):
                with open(self.dataset_path, "r", encoding="utf-8") as file:
                    data = json.load(file)
                    if isinstance(data, list) and len(data) > 0:
                        print(f"Loaded curated domain benchmark dataset ({len(data)} foundational papers).")
                        return data

            # 2. Fallback to JSONL dataset only if standard dataset is missing
            literature_papers = []
            jsonl_path = os.path.join(os.path.dirname(self.dataset_path), "sample.jsonl")
            if os.path.exists(jsonl_path):
                with open(jsonl_path, "r", encoding="utf-8") as f:
                    for line in f:
                        if not line.strip():
                            continue
                        try:
                            item = json.loads(line)
                            title = item.get("title", "")
                            abstract = item.get("abstract") or ""
                            if title and (abstract or len(title) > 25):
                                literature_papers.append({
                                    "id": item.get("paper_id") or item.get("id"),
                                    "title": title,
                                    "abstract": abstract,
                                    "keywords": item.get("mag_field_of_study") or item.get("keywords") or ["General"],
                                    "year": item.get("year", 2000),
                                    "venue": item.get("journal") or item.get("venue")
                                })
                        except Exception:
                            continue

            with_abs = [p for p in literature_papers if p.get("abstract")]
            without_abs = [p for p in literature_papers if not p.get("abstract")]
            return (with_abs + without_abs)[:35]

        except Exception as error:
            print("Literature dataset loading error:", error)
            return []

    # suchdef load_literature(self):

    #     try:

    #         if not os.path.exists(
    #             self.dataset_path
    #         ):

    #             return []


    #         with open(
    #             self.dataset_path,
    #             "r",
    #             encoding="utf-8"
    #         ) as file:

    #             data = json.load(file)


    #         if not isinstance(data, list):

    #             return []


    #         return data


    #     except Exception as error:

    #         print(
    #             "Literature dataset loading error:",
    #             error
    #         )

    #         return []


    # ==========================================
    # NORMALIZE KEYWORDS
    # ==========================================

    def normalize_keywords(self, keywords):

        normalized = []


        if not keywords:

            return normalized


        for keyword in keywords:

            if isinstance(keyword, dict):

                value = keyword.get(
                    "keyword",
                    ""
                )

            else:

                value = str(keyword)


            value = value.strip().lower()


            if value:

                normalized.append(
                    value
                )


        return normalized


    # ==========================================
    # CREATE PAPER TEXT
    # ==========================================

    def create_paper_text(
        self,
        paper
    ):

        title = str(
            paper.get(
                "title",
                ""
            )
        )


        abstract = str(
            paper.get(
                "abstract",
                ""
            )
        )


        keywords = self.normalize_keywords(

            paper.get(
                "keywords",
                []
            )

        )


        keyword_text = " ".join(
            keywords
        )


        text = " ".join(

            [
                title,
                abstract,
                keyword_text
            ]

        )


        return text.lower().strip()


    def calculate_similarity(
        self,
        query_text,
        literature_texts
    ):
        try:
            from app.ml.embeddings import EmbeddingService
            emb_service = EmbeddingService()
            if not emb_service._use_fallback and emb_service._model is not None:
                query_vec = emb_service.encode(query_text)
                lit_vecs = emb_service.encode(literature_texts)
                scores = np.dot(lit_vecs, query_vec)
                return np.clip(scores, 0.0, 1.0)
        except Exception:
            pass

        # TF-IDF Cosine Similarity Fallback
        documents = [
            query_text
        ] + literature_texts

        vectorizer = TfidfVectorizer(
            stop_words="english",
            ngram_range=(1, 2)
        )

        matrix = vectorizer.fit_transform(
            documents
        )

        query_vector = matrix[0]
        literature_vectors = matrix[1:]

        similarity_scores = cosine_similarity(
            query_vector,
            literature_vectors
        ).flatten()

        return similarity_scores


    # ==========================================
    # ANALYZE KEYWORD FREQUENCY
    # ==========================================

    def analyze_keyword_frequency(self):

        frequency = {}


        for paper in self.literature:

            keywords = self.normalize_keywords(

                paper.get(
                    "keywords",
                    []
                )

            )


            for keyword in keywords:

                frequency[keyword] = (

                    frequency.get(
                        keyword,
                        0
                    )

                    + 1
                )


        return frequency


    # ==========================================
    # DETECT UNDEREXPLORED KEYWORDS
    # ==========================================

    def detect_underexplored_keywords(
        self,
        query_keywords
    ):

        frequency = self.analyze_keyword_frequency()


        query_keywords = self.normalize_keywords(
            query_keywords
        )


        underexplored = []


        for keyword in query_keywords:

            keyword_frequency = frequency.get(
                keyword,
                0
            )


            if keyword_frequency <= 1:

                underexplored.append({

                    "keyword": keyword,

                    "frequency": keyword_frequency

                })


        return underexplored


    # ==========================================
    # GENERATE GAP STATEMENT
    # ==========================================

    def generate_gap_statement(
        self,
        query_paper,
        average_similarity,
        underexplored_keywords,
        novelty_level: str = None
    ):

        title = query_paper.get(
            "title",
            "the proposed research"
        )


        if novelty_level == "High" or (novelty_level is None and average_similarity < 0.20):

            gap_level = (
                "The proposed research explores frontier territory with "
                "relatively low direct overlap against existing literature."
            )

        elif novelty_level == "Medium" or (novelty_level is None and average_similarity < 0.50):

            gap_level = (
                "The proposed research builds directly upon established literature "
                "while introducing distinct conceptual perspectives and novel combinations."
            )

        else:

            gap_level = (
                "The proposed research has substantial overlap with prior art "
                "and functions as a direct, incremental continuation."
            )


        if underexplored_keywords:

            keywords = [

                item["keyword"]

                for item in underexplored_keywords[:5]

            ]


            keyword_statement = (

                "Potentially underexplored concepts include: "

                + ", ".join(keywords)

                + "."
            )

        else:

            keyword_statement = (

                "No strongly underexplored keywords were identified "
                "from the current literature dataset."
            )


        return (

            f"{gap_level} "

            f"{keyword_statement} "

            f"This suggests that '{title}' may contribute by exploring "
            f"relationships or applications that are less represented "
            f"in the analyzed literature."
        )


    # ==========================================
    # NOVELTY CALCULATION & CLASSIFICATION
    # ==========================================

    def calculate_novelty(
        self,
        similar_papers: list,
        cluster_novelty_score: float = None
    ) -> dict:
        """
        Calculates literature novelty based on:
        1. Nearest prior art similarity (top-1)
        2. Local neighborhood overlap (top-3 average)
        3. Thematic cluster distance in dense embedding space
        """
        if not similar_papers:
            return {
                "novelty_score": 0.85,
                "novelty_percentage": 85.0,
                "novelty_level": "High",
                "nearest_similarity": 0.0,
                "top3_similarity": 0.0,
                "novelty_category": "High (Pioneering / Frontier)"
            }

        top_sims = [float(p.get("similarity", 0.0) or 0.0) for p in similar_papers[:3]]
        nearest_sim = top_sims[0] if top_sims else 0.0
        top3_sim = sum(top_sims) / len(top_sims) if top_sims else 0.0

        # Prior art overlap: 60% nearest benchmark paper, 40% top-3 neighborhood
        prior_art_overlap = 0.60 * nearest_sim + 0.40 * top3_sim

        # Factor in cluster novelty if available
        if cluster_novelty_score is not None:
            raw_novelty = 0.70 * (1.0 - prior_art_overlap) + 0.30 * cluster_novelty_score
        else:
            raw_novelty = 1.0 - prior_art_overlap

        novelty_score = round(max(0.08, min(0.96, raw_novelty)), 4)
        novelty_percentage = round(novelty_score * 100.0, 1)

        # Classification based on novelty score
        if novelty_score >= 0.72:
            novelty_level = "High"
            novelty_category = "High (Pioneering / Frontier)"
        elif novelty_score >= 0.42:
            novelty_level = "Medium"
            novelty_category = "Medium (Novel Synthesis / Extension)"
        else:
            novelty_level = "Low"
            novelty_category = "Low (Incremental Follow-up)"

        return {
            "novelty_score": novelty_score,
            "novelty_percentage": novelty_percentage,
            "novelty_level": novelty_level,
            "nearest_similarity": round(nearest_sim, 4),
            "top3_similarity": round(top3_sim, 4),
            "novelty_category": novelty_category
        }

    def classify_novelty(
        self,
        average_similarity
    ):
        if isinstance(average_similarity, str):
            return average_similarity
        if average_similarity < 0.25:
            return "High"
        elif average_similarity < 0.55:
            return "Medium"
        return "Low"


    # ==========================================
    # MAIN GAP DETECTION
    # ==========================================

    def detect_gap(
        self,
        query_paper
    ):

        # Reload dataset every request

        self.literature = self.load_literature()


        if not self.literature:

            return {

                "error":
                    "Literature dataset not found or empty.",

                "literature_count": 0,

                "average_similarity": 0,

                "novelty_level": "Unknown",

                "similar_papers": [],

                "underexplored_keywords": [],

                "potential_gap":
                    "Unable to perform research gap analysis."
            }


        # --------------------------------------
        # CREATE QUERY TEXT
        # --------------------------------------

        query_text = self.create_paper_text(
            query_paper
        )


        # --------------------------------------
        # CREATE LITERATURE TEXTS
        # --------------------------------------

        literature_texts = []


        for paper in self.literature:

            text = self.create_paper_text(
                paper
            )

            literature_texts.append(
                text
            )


        # --------------------------------------
        # CALCULATE SIMILARITY
        # --------------------------------------

        similarity_scores = (

            self.calculate_similarity(

                query_text,

                literature_texts

            )

        )


        # --------------------------------------
        # BUILD SIMILAR PAPER LIST
        # --------------------------------------

        similar_papers = []


        for index, score in enumerate(
            similarity_scores
        ):

            paper = self.literature[index]


            similar_papers.append({
                "id": paper.get("id"),
                "title": paper.get("title"),
                "year": paper.get("year"),
                "venue": paper.get("venue"),
                "doi": paper.get("doi"),
                "similarity": round(float(score), 4)
            })

        # Sort by similarity
        similar_papers = sorted(
            similar_papers,
            key=lambda x: x["similarity"],
            reverse=True
        )

        # Top 5
        similar_papers = similar_papers[:5]

        # --------------------------------------
        # AVERAGE SIMILARITY
        # --------------------------------------

        average_similarity = (
            sum(similarity_scores)
            / len(similarity_scores)
        )

        average_similarity = round(
            float(average_similarity),
            4
        )

        # --------------------------------------
        # UNDEREXPLORED KEYWORDS
        # --------------------------------------

        underexplored_keywords = (
            self.detect_underexplored_keywords(
                query_paper.get(
                    "keywords",
                    []
                )
            )
        )

        # --------------------------------------
        # THEMATIC CLUSTERING (K-Means + PCA)
        # --------------------------------------
        clustering_result = {}
        cluster_nov = None
        try:
            from app.ml.clustering import ResearchClusteringService
            clustering_service = ResearchClusteringService()
            clustering_result = clustering_service.cluster_literature(
                target_paper=query_paper,
                literature_papers=self.literature
            )
            target_pos = clustering_result.get("target_position", {})
            cluster_nov = target_pos.get("novelty_score")
        except Exception as e:
            print("Clustering error:", e)
            clustering_result = {}

        # --------------------------------------
        # NOVELTY METRICS
        # --------------------------------------
        novelty_data = self.calculate_novelty(
            similar_papers=similar_papers,
            cluster_novelty_score=cluster_nov
        )
        novelty_level = novelty_data["novelty_level"]
        novelty_score = novelty_data["novelty_score"]
        novelty_percentage = novelty_data["novelty_percentage"]

        # --------------------------------------
        # GAP STATEMENT
        # --------------------------------------
        potential_gap = self.generate_gap_statement(
            query_paper,
            average_similarity,
            underexplored_keywords,
            novelty_level=novelty_level
        )

        # --------------------------------------
        # FINAL RESULT
        # --------------------------------------
        return {
            "literature_count": len(self.literature),
            "average_similarity": average_similarity,
            "novelty_level": novelty_level,
            "novelty_score": novelty_score,
            "novelty_percentage": novelty_percentage,
            "novelty_category": novelty_data["novelty_category"],
            "nearest_similarity": novelty_data["nearest_similarity"],
            "top3_similarity": novelty_data["top3_similarity"],
            "similar_papers": similar_papers,
            "underexplored_keywords": underexplored_keywords,
            "potential_gap": potential_gap,
            "clustering": clustering_result
        }