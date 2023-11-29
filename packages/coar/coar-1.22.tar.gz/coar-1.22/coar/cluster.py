import typing

import numpy as np
import pandas as pd

from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import pairwise_distances

from coar.utils import rule_distance


def _check_input(df: pd.DataFrame, columns: typing.List[str]) -> None:
    # check df is DataFrame
    if not isinstance(df, pd.DataFrame):
        raise ValueError(
            "The input `df` must be a pandas.DataFrame."
        )

    # check df is not empty
    if not df.shape[0]:
        raise ValueError(
            "The input DataFrame `df` is empty."
        )

    # check for mandatory columns
    if not all(col in df.columns for col in columns):
        raise ValueError(
            f"The input DataFrame `df` must have columns {columns}."
        )

    # check column types

    if "antecedent" in columns and not all(
            type(val) == set and all(type(v) == str for v in val) for val in df["antecedent"]):
        raise ValueError("Column `antecedent` must contain set of strings.")

    if "succedent" in columns and not all(
            type(val) == set and all(type(v) == str for v in val) for val in df["succedent"]):
        raise ValueError("Column `succedent` must contain set of strings.")

    if "support" in columns and not all(type(val) == float for val in df["support"]):
        raise ValueError("Column `support` must be float.")

    if "confidence" in columns and not all(type(val) == float for val in df["confidence"]):
        raise ValueError("Column `confidence` must be float.")

    if "cluster" in columns and not all(type(val) == int for val in df["cluster"]):
        raise ValueError("Column `cluster` must be float.")


def agglomerative_clustering(
        df: pd.DataFrame,
        n_clusters: int = None,
        abs_ante_attr_diff_threshold: float | int = None,
        abs_succ_attr_diff_threshold: float | int = None,
        rel_ante_attr_diff_threshold: float | int = None,
        rel_succ_attr_diff_threshold: float | int = None,
        abs_supp_diff_threshold: float | int = None,
        abs_conf_diff_threshold: float | int = None,
        linkage: str = 'complete',
) -> pd.DataFrame:

    exclusive_param_pairs = [
        (abs_ante_attr_diff_threshold, rel_ante_attr_diff_threshold),
        (abs_succ_attr_diff_threshold, rel_succ_attr_diff_threshold),
    ]

    if linkage not in ['complete', 'single']:
        raise ValueError(
            "Linkage must be either `complete` or `single`."
        )

    # validate params
    if n_clusters is not None:
        if not all(
                [param is None for param_pairs in exclusive_param_pairs for param in param_pairs] + [
                    abs_supp_diff_threshold is None, abs_conf_diff_threshold is None
                ]
        ):
            raise ValueError(
                "Threshold params "
                "abs_ante_attr_diff_threshold, rel_ante_attr_diff_threshold, "
                "abs_succ_attr_diff_threshold, rel_succ_attr_diff_threshold, "
                "abs_supp_diff_threshold, "
                "abs_conf_diff_threshold "
                " must be None if n_clusters is specified. "
                "Specify either n_clusters or threshold params."
            )
        distance_threshold = None
    else:
        for i, j in exclusive_param_pairs:
            if not ((i is None) ^ (j is None)):
                raise ValueError(
                    "Exactly one of absolute and relative thresholds has to be set per characteristic, "
                    "and the other needs to be None. Set one param per each of the following pairs:"
                    "abs_ante_attr_diff_threshold, rel_ante_attr_diff_threshold, "
                    "abs_succ_attr_diff_threshold, rel_succ_attr_diff_threshold, "
                )

        selected_thresholds = [abs_threshold if abs_threshold is not None else rel_threshold for abs_threshold, rel_threshold in
                               exclusive_param_pairs] + [abs_supp_diff_threshold, abs_conf_diff_threshold]

        if not all((isinstance(threshold, float) or isinstance(threshold, int)) and threshold >= 0 for threshold in
                   selected_thresholds):
            raise ValueError(
                "Threshold params"
                "abs_ante_attr_diff_threshold, rel_ante_attr_diff_threshold, "
                "abs_succ_attr_diff_threshold, rel_succ_attr_diff_threshold, "
                "abs_supp_diff_threshold, "
                "abs_conf_diff_threshold "
                "must be positive and must be float or int. "
            )
        # Distance threshold in AgglomerativeClustering means threshold at or above which clusters will not be merged.
        # We want the clusters to be merged at distance threshold therefore we pass double sum selected thresholds.
        # If any threshold is surpassed, the rule distance is infinity. That means, it really doesn't matter
        # what threshold we pass, as long as it is less than infinity.
        distance_threshold = sum(selected_thresholds) * 2 + 1

    _check_input(df, ["antecedent", "succedent", "support", "confidence"])

    metric_params = {
        'df': df,
        'abs_ante_attr_diff_threshold': abs_ante_attr_diff_threshold,
        'abs_succ_attr_diff_threshold': abs_succ_attr_diff_threshold,
        'rel_ante_attr_diff_threshold': rel_ante_attr_diff_threshold,
        'rel_succ_attr_diff_threshold': rel_succ_attr_diff_threshold,
        'abs_supp_diff_threshold': abs_supp_diff_threshold,
        'abs_conf_diff_threshold': abs_conf_diff_threshold,
    }

    # surpass validation
    x = np.array([i for i in df.index]).reshape(-1, 1)
    distance_matrix = pairwise_distances(
        x, metric=rule_distance, **metric_params
    )
    clustering = AgglomerativeClustering(
        n_clusters=n_clusters, linkage=linkage, metric='precomputed',
        compute_full_tree='auto' if n_clusters is None else True,
        distance_threshold=distance_threshold
    )

    clusters = clustering.fit_predict(distance_matrix)
    df['cluster'] = clusters
    return df


def cluster_representative(df: pd.DataFrame) -> pd.DataFrame:
    columns_in_sort_order = ["support", "confidence", "antecedent", "succedent"]
    _check_input(df, columns_in_sort_order + ["cluster"])
    df = df.sort_values('cluster')
    repr_indexes = [df.loc[df['cluster'] == cluster].sort_values(
        columns_in_sort_order, ascending=[False, False, True, True],
        key=lambda x: pd.Series(len(i) if type(i) is set else i for i in x)).index[0] for cluster in
                    set(df['cluster'].tolist())]
    df['representative'] = [1 if i in repr_indexes else 0 for i in df.index]
    return df
