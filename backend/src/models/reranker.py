from sentence_transformers import CrossEncoder

from src.config import (
    RERANKER_MODEL,
    RERANK_TOP_K,
)


class CrossEncoderReranker:
    """
    Cross-Encoder reranker using BGE Reranker.
    """

    def __init__(self, model_name: str = RERANKER_MODEL):

        print(f"Loading Cross Encoder: {model_name}")

        self.model = CrossEncoder(model_name)

    def rerank(
        self,
        query: str,
        retrieval_results,
        top_k: int = RERANK_TOP_K,
    ):

        if not retrieval_results:
            return []

        pairs = [(query, result.document.page_content) for result in retrieval_results]

        scores = self.model.predict(
            pairs,
            batch_size=16,
            show_progress_bar=False,
        )

        ranked = sorted(
            zip(retrieval_results, scores),
            key=lambda x: x[1],
            reverse=True,
        )

        reranked_results = []

        for rank, (result, score) in enumerate(
            ranked[:top_k],
            start=1,
        ):
            result.rank = rank
            result.retrieval_score = float(score)
            reranked_results.append(result)

        return reranked_results

    def score_sentences(
        self,
        query: str,
        sentences: list[str],
    ):
        """
        Score candidate sentences against a query.
        """

        if not sentences:
            return []

        pairs = [(query, sentence) for sentence in sentences]
        scores = self.model.predict(
            pairs,
            batch_size=16,
            show_progress_bar=False,
        )
        return list(zip(sentences, scores))
