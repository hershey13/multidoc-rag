from pathlib import Path

import pandas as pd


class RetrievalEvaluator:
    """
    Evaluate any retriever that implements:

        search_with_scores(query)

    and returns a RetrievalResponse.
    """

    def __init__(self, benchmark):

        self.benchmark = benchmark

    def evaluate(self, retriever):

        rows = []

        queries = self.benchmark.queries()

        for _, query_row in queries.iterrows():

            response = retriever.search_with_scores(query=query_row["query"])

            for result in response.results:

                doc = result.document

                rows.append(
                    {
                        "query_id": query_row["query_id"],
                        "query": query_row["query"],
                        "query_category": query_row["category"],
                        "retriever": response.retriever,
                        "latency": response.latency,
                        "rank": result.rank,
                        "retrieval_score": result.retrieval_score,
                        "score_type": result.score_type,
                        "filename": doc.metadata.get("filename"),
                        "page": doc.metadata.get("page"),
                        "chunk_id": doc.metadata.get("chunk_id"),
                        "document_category": doc.metadata.get("category"),
                        "chunk_length": len(doc.page_content),
                        "chunk_text": doc.page_content,
                    }
                )

        return pd.DataFrame(rows)

    def save_results(
        self,
        dataframe,
        output_file,
    ):

        output_file = Path(output_file)

        output_file.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        dataframe.to_csv(
            output_file,
            index=False,
        )

        print(f"Saved results to {output_file}")
