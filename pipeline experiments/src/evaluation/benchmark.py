from pathlib import Path
import pandas as pd

# ---------------------------------------------------
# Project Paths
# ---------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DEFAULT_BENCHMARK = PROJECT_ROOT / "data" / "benchmark" / "benchmark_queries.csv"


class BenchmarkDataset:
    """
    Loads benchmark queries.
    """

    def __init__(
        self,
        csv_path: str | Path | None = None,
    ):

        if csv_path is None:
            csv_path = DEFAULT_BENCHMARK

        self.csv_path = Path(csv_path)

        self.data = pd.read_csv(self.csv_path)

    def queries(self):

        return self.data

    def __len__(self):

        return len(self.data)

    def summary(self):

        print("\n")
        print("=" * 70)
        print("BENCHMARK SUMMARY")
        print("=" * 70)

        print(f"File      : {self.csv_path}")
        print(f"Queries   : {len(self.data)}")

        print("\nCategories")

        print(self.data["category"].value_counts())

        print("=" * 70)
