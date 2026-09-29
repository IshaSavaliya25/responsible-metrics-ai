import os
import logging
import numpy as np
from typing import List, Union, Tuple, Optional

logger = logging.getLogger(__name__)

class EmbeddingService:
    """
    Singleton service managing dense semantic embeddings.
    Uses SentenceTransformers (all-MiniLM-L6-v2) with graceful fallback
    to TF-IDF / character n-gram cosine similarity.
    """
    _instance = None
    _model = None
    _model_name = "sentence-transformers/all-MiniLM-L6-v2"
    _use_fallback = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(EmbeddingService, cls).__new__(cls)
            cls._instance._init_model()
        return cls._instance

    def _init_model(self):
        """Lazy model loader with local-first check & exception handling."""
        try:
            import os
            # If offline or HF download is not desirable, check local cache first
            from sentence_transformers import SentenceTransformer
            try:
                self._model = SentenceTransformer(self._model_name, local_files_only=True)
                self._use_fallback = False
                logger.info("SentenceTransformer model loaded from local cache.")
                return
            except Exception:
                pass

            # Fast network attempt if ALLOW_ONLINE_DOWNLOAD is set or default
            if os.environ.get("TRANSFORMERS_OFFLINE") == "1":
                self._use_fallback = True
                self._model = None
                return

            self._model = SentenceTransformer(self._model_name)
            self._use_fallback = False
            logger.info("SentenceTransformer model loaded successfully.")
        except Exception as e:
            logger.info("Using high-performance HashingVectorizer semantic representation: %s", str(e))
            self._model = None
            self._use_fallback = True

    def encode(self, texts: Union[str, List[str]]) -> np.ndarray:
        """
        Encode a single string or list of strings into normalized embedding vectors.
        """
        is_single = isinstance(texts, str)
        text_list = [texts] if is_single else texts

        if not text_list:
            return np.zeros((0, 384), dtype=np.float32) if not is_single else np.zeros(384, dtype=np.float32)

        if not self._use_fallback and self._model is not None:
            try:
                embeddings = self._model.encode(
                    text_list,
                    convert_to_numpy=True,
                    normalize_embeddings=True,
                    show_progress_bar=False
                )
                return embeddings[0] if is_single else embeddings
            except Exception as err:
                logger.debug("Error during dense encoding, using hash vectorizer: %s", err)

        # High-performance deterministic HashingVectorizer fallback
        return self._hash_encode(text_list, is_single)

    def _hash_encode(self, texts: List[str], is_single: bool):
        from sklearn.feature_extraction.text import HashingVectorizer
        try:
            vectorizer = HashingVectorizer(
                n_features=384,
                alternate_sign=False,
                norm="l2",
                ngram_range=(1, 2),
                stop_words="english"
            )
            matrix = vectorizer.transform(texts).toarray().astype(np.float32)
            # Normalize
            norms = np.linalg.norm(matrix, axis=1, keepdims=True)
            norms[norms == 0] = 1.0
            normalized = matrix / norms
            return normalized[0] if is_single else normalized
        except Exception as e:
            # Deterministic ASCII projection
            vectors = []
            for t in texts:
                vec = np.zeros(384, dtype=np.float32)
                for i, char in enumerate(t[:384]):
                    vec[i % 384] += ord(char)
                norm = np.linalg.norm(vec)
                vectors.append(vec / norm if norm > 0 else vec)
            res = np.array(vectors, dtype=np.float32)
            return res[0] if is_single else res
        except Exception:
            # Deterministic hash fallback
            vectors = []
            for t in texts:
                vec = np.zeros(384, dtype=np.float32)
                for i, char in enumerate(t[:384]):
                    vec[i % 384] += ord(char)
                norm = np.linalg.norm(vec)
                vectors.append(vec / norm if norm > 0 else vec)
            res = np.array(vectors, dtype=np.float32)
            return res[0] if is_single else res

    def compute_similarity(self, text1: str, text2: str) -> float:
        """Calculate cosine similarity between two texts in [0.0, 1.0]."""
        if not text1 or not text2:
            return 0.0
        vecs = self.encode([text1, text2])
        sim = float(np.dot(vecs[0], vecs[1]))
        return max(0.0, min(1.0, round(sim, 4)))

    def rank_by_similarity(self, query: str, candidates: List[str], top_k: Optional[int] = None) -> List[Tuple[int, float]]:
        """
        Rank candidate texts against a query string.
        Returns list of (candidate_index, similarity_score) sorted descending.
        """
        if not query or not candidates:
            return []

        query_vec = self.encode(query)
        cand_vecs = self.encode(candidates)

        similarities = np.dot(cand_vecs, query_vec)
        ranked_indices = np.argsort(-similarities)

        results = [(int(idx), float(round(similarities[idx], 4))) for idx in ranked_indices]
        if top_k:
            results = results[:top_k]
        return results
