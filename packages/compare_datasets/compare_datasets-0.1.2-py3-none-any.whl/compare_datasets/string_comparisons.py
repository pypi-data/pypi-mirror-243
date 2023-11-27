from Levenshtein import distance
import polars as pl
from tabulate import tabulate
from tqdm import tqdm

from compare_datasets.prepare import PrepareForComparison
from compare_datasets.structure import Comparison, stringify_result, timeit

import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class StringComparisons(Comparison):
    def __init__(self, prepared_data: PrepareForComparison, verbose=False, progress_bar=None):
        self.column_list = prepared_data.column_list
        progress_bar.set_description("Preparing String Comparison")
        self.tested = prepared_data.tested.select(self.column_list["String Columns"])
        self.expected = prepared_data.expected.select(
            self.column_list["String Columns"]
        )
        progress_bar.set_description("Counting Nulls for string columns")
        null_counts = {
            "tested": self.tested.null_count(),
            "expected": self.expected.null_count(),
        }
        progress_bar.set_description("Filing Nulls with blanks for comparison")
        self.tested = self.tested.with_columns(pl.all().fill_null(""))
        self.expected = self.expected.with_columns(pl.all().fill_null(""))
        super().validate(self.tested, self.expected, "Utf8")
        self.data_type = "STRING"
        self.columns_names = list(self.expected.columns)
        self.report = {}
        self.report["name"] = "String Column Comparison"
        # super().calculate_jaccard_similarity(self.columns_names)
        progress_bar.set_description("Calculating Levenshtein Distance for string columns")
        self.compare()
        self.report["overall_result"] = (       
            self.report["value_by_value"]["result"]
        )
        if verbose:
            logger.info(f"Columns in the expected dataframe: {self.expected.columns}")
            logger.info(f"Columns in the tested dataframe: {self.tested.columns}")
            logger.info(f"Shape of the expected dataframe: {self.expected.shape}")
            logger.info(f"Shape of the tested dataframe: {self.tested.shape}")
            logger.info(
                f"Null counts in the expected dataframe: {null_counts['expected']}"
            )
            logger.info(f"Null counts in the tested dataframe: {null_counts['tested']}")
            logger.info("Nulls filled with blank string for comparison")
            # logger.info(self.report)
        self.result = self.report["overall_result"]

    # @timeit(name="Levenshtein Distance")
    def generate_differenced_dataframe(self):
        """
        Generates a dataframe containing the difference between the expected and tested dataframes.
        """
        return pl.DataFrame(
            [
                pl.Series(
                    distance(s1, s2) for s1, s2 in zip(self.expected[c], self.tested[c])
                ).alias(c)
                for c in self.columns_names
            ]
        )

    def compare(self):
        self.differenced = self.generate_differenced_dataframe()
        levenshtein_distances = pl.Series(
            self.differenced.select(pl.all().sum()).melt()["value"]
        )
        failed_columns = [
            column
            for column, distance in zip(self.columns_names, levenshtein_distances)
            if distance != 0
        ]
        self.differenced = self.differenced.select(failed_columns)
        self.report["value_by_value"] = {}
        self.report["value_by_value"]["result"] = levenshtein_distances.sum() == 0
        self.report["value_by_value"]["report"] = tabulate(
            [
                (column, distance, stringify_result(result))
                for column, distance, result in zip(
                    self.columns_names,
                    levenshtein_distances,
                    levenshtein_distances == 0,
                )
            ],
            headers=["Column Name", "Total Levenshtein Distance", "Result"],
            tablefmt="psql",
        )
        self.report["differenced"] = self.differenced

        self.report["value_by_value"][
            "explanation"
        ] = "The string comparisons are done using the Levenshtein distance. The Levenshtein distance is the minimum number of single-character edits (insertions, deletions or substitutions) required to change one word into the other."

        if not self.report["value_by_value"]["result"]:
            self.report["value_by_value"][
                "explanation"
            ] += f"\nThe Levenshtein distance between the expected and tested dataframes is not 0 for all columns.\nThis means that the expected and tested dataframes have different string values in the same column(s)."
        else:
            self.report["value_by_value"][
                "explanation"
            ] += f"\nThe Levenshtein distance between the expected and tested dataframes is 0 for all columns.\nThis means that the expected and tested dataframes have the same values for the same column(s)."

    def generate_report(self):
        report = f"""COMPARISON FOR {self.data_type} COLUMNS

Value by Value Comparison: {stringify_result(self.report['value_by_value']['result'])}
{self.report['value_by_value']['report']}
{self.report['value_by_value']['explanation']}
"""
        return report

    def validate(self):
        return super().validate(self.tested, self.expected, "Utf8")
