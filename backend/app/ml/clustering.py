import logging
import numpy as np
from typing import List, Dict, Any, Optional
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from app.ml.embeddings import EmbeddingService

logger = logging.getLogger(__name__)

class ResearchClusteringService:
    """
    Performs semantic clustering and 2D dimensional reduction (PCA)
    on research papers to discover thematic clusters and identify
    research gap positioning.
    """

    def __init__(self):
        self.embedding_service = EmbeddingService()

    def cluster_literature(
        self,
        target_paper: Dict[str, Any],
        literature_papers: List[Dict[str, Any]],
        n_clusters: int = 3
    ) -> Dict[str, Any]:
        """
        Clusters literature papers and computes target paper position relative
        to literature clusters.
        """
        if not literature_papers:
            return {
                "clusters": [],
                "target_position": {"x": 0.0, "y": 0.0, "cluster": 0, "nearest_cluster": "N/A"},
                "scatter_points": []
            }

        all_papers = list(literature_papers)
        # Create corpus representations
        corpus_texts = [
            f"{p.get('title', '')}. {p.get('abstract', '')}"
            for p in all_papers
        ]

        target_text = f"{target_paper.get('title', '')}. {target_paper.get('abstract', '')}"
        all_texts = corpus_texts + [target_text]

        # Embed all texts
        vectors = self.embedding_service.encode(all_texts)

        # 2D projection via PCA
        n_samples = len(all_texts)
        n_components = 2 if n_samples >= 2 else 1

        pca = PCA(n_components=n_components, random_state=42)
        coords_2d = pca.fit_transform(vectors)

        if n_components == 1:
            coords_2d = np.hstack([coords_2d, np.zeros((n_samples, 1))])

        # Cluster literature papers
        k = min(n_clusters, max(1, len(literature_papers)))
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        lit_labels = kmeans.fit_predict(vectors[:len(literature_papers)])

        # Predict cluster for target paper
        target_vector = vectors[-1:]
        target_cluster = int(kmeans.predict(target_vector)[0])
        target_dist_to_center = float(np.linalg.norm(target_vector[0] - kmeans.cluster_centers_[target_cluster]))

        # Format cluster themes based on common keywords
        clusters_summary = []
        for c_id in range(k):
            members = [all_papers[i] for i, lbl in enumerate(lit_labels) if lbl == c_id]
            kw_pool = []
            for m in members:
                kw_pool.extend(m.get("keywords", []))
            top_kws = list(dict.fromkeys(kw_pool))[:4]
            theme_name = ", ".join(top_kws) if top_kws else f"Cluster {c_id + 1}"

            clusters_summary.append({
                "cluster_id": c_id,
                "theme": theme_name,
                "paper_count": len(members)
            })

        # Format scatter points for visualization
        scatter_points = []
        for i, p in enumerate(all_papers):
            scatter_points.append({
                "title": p.get("title", f"Paper {i+1}"),
                "x": round(float(coords_2d[i][0]), 4),
                "y": round(float(coords_2d[i][1]), 4),
                "cluster": int(lit_labels[i]),
                "type": "Literature Reference",
                "year": p.get("year", "N/A")
            })

        # Add target paper point
        target_x = round(float(coords_2d[-1][0]), 4)
        target_y = round(float(coords_2d[-1][1]), 4)
        scatter_points.append({
            "title": target_paper.get("title", "Analyzed Paper"),
            "x": target_x,
            "y": target_y,
            "cluster": target_cluster,
            "type": "Analyzed Paper (You)",
            "year": target_paper.get("year", "Current")
        })

        # Compute cluster cosine similarity and novelty score
        center_vec = kmeans.cluster_centers_[target_cluster]
        center_norm = float(np.linalg.norm(center_vec))
        if center_norm > 0:
            cluster_sim = float(np.dot(target_vector[0], center_vec / center_norm))
        else:
            cluster_sim = 0.0
        cluster_sim = max(0.0, min(1.0, cluster_sim))
        novelty_score = round(max(0.05, min(0.98, 1.0 - cluster_sim)), 3)

        return {
            "clusters": clusters_summary,
            "target_position": {
                "x": target_x,
                "y": target_y,
                "cluster": target_cluster,
                "distance_to_center": round(target_dist_to_center, 4),
                "cluster_similarity": round(cluster_sim, 4),
                "novelty_score": novelty_score
            },
            "scatter_points": scatter_points
        }
