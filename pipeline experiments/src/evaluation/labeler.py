from pathlib import Path

import pandas as pd
from pandas.errors import EmptyDataError

import textwrap


class GroundTruthLabeler:
    """
    Interactive tool for creating ground-truth labels.
    """

    def __init__(self, retrieval_results_path, output_path):
        # Load retrieval results
        self.results = pd.read_csv(retrieval_results_path)

        # Output file
        self.output_path = Path(output_path)
        self.output_path.parent.mkdir(parents=True, exist_ok=True)

        # Load existing labels if available
        if self.output_path.exists():
            try:
                self.labels = pd.read_csv(self.output_path)
            except EmptyDataError:
                self.labels = self.results.copy()
        else:
            self.labels = self.results.copy()

        # Ensure relevance column exists
        if "relevance" not in self.labels.columns:
            self.labels["relevance"] = pd.NA

    def get_query(self, query_id):
        query_df = (
            self.labels[self.labels["query_id"] == query_id].sort_values("rank").copy()
        )

        if query_df.empty:
            raise ValueError(f"No retrieval results found for query_id={query_id}")

        return query_df

    def show_query(self, query_id):
        query_df = self.get_query(query_id)

        query_df = query_df[query_df["relevance"].isna()].copy()

        if query_df.empty:
            print(f"Query {query_id} is already fully labelled.")
            return

        print("=" * 100)
        print(f"Query {query_id}")
        print(query_df.iloc[0]["query"])
        print("=" * 100)

        for _, row in query_df.iterrows():
            print(f"\nRank      : {row['rank']}")
            print(f"Document  : {row['filename']}")
            print(f"Score     : {row['retrieval_score']:.4f}")
            print("-" * 100)
            print(row["text_preview"])

    def label_query(self, query_id):
        query_df = self.get_query(query_id)
        query_df = query_df[query_df["relevance"].isna()].copy()
        if query_df.empty:
            print(f"Query {query_id} is already fully labelled.")
            return

        total_queries = self.labels["query_id"].nunique()
        total_chunks = len(query_df)

        print("\n" + "=" * 100)
        print(f"QUERY {query_id}/{total_queries}")
        print("=" * 100)
        print(query_df.iloc[0]["query"])
        print("=" * 100)

        for idx, (_, row) in enumerate(query_df.iterrows(), start=1):
            print("\n" + "-" * 100)
            print(f"Chunk {idx}/{total_chunks}")
            print("-" * 100)

            print(f"Rank         : {row['rank']}")
            print(f"Document     : {row['filename']}")
            print(f"Page         : {row['page']}")
            print(f"Category     : {row['document_category']}")
            print(f"Chunk ID     : {row['chunk_id']}")
            print(f"Chunk Length : {row['chunk_length']}")
            print(f"Score        : {row['retrieval_score']:.4f}")

            print("-" * 100)
            print("FULL CHUNK")
            print("-" * 100)

            # Show the COMPLETE chunk with line wrapping
            chunk = str(row["chunk_text"])
            print(textwrap.fill(chunk, width=120))

            print("-" * 100)

            print("Label Guide")
            print("2 → Directly answers the query")
            print("1 → Relevant / supporting information")
            print("0 → Irrelevant")

            while True:
                label = input("\nYour Label (0/1/2): ").strip()

                if label in ("0", "1", "2"):
                    label = int(label)
                    break

                print("❌ Please enter only 0, 1 or 2.")

            mask = (self.labels["query_id"] == row["query_id"]) & (
                self.labels["chunk_id"] == row["chunk_id"]
            )

            self.labels.loc[mask, "relevance"] = label

        self.labels.to_csv(self.output_path, index=False)
        completed = len(self.completed_queries())

        print("\n" + "=" * 100)
        print(f"Query {query_id} completed.")
        print(f"Overall Progress: {completed}/{total_queries} queries labelled")
        print("=" * 100)

    def completed_queries(self):
        completed = []

        for query_id in sorted(self.labels["query_id"].unique()):

            query_rows = self.labels[self.labels["query_id"] == query_id]

            if (
                not query_rows.empty
                and "relevance" in query_rows.columns
                and query_rows["relevance"].notna().all()
            ):
                completed.append(query_id)

        return completed
