import sys
import typing

import pandas as pd


def get_support_from_fourfold(fourfold):
    return fourfold[0] / sum(fourfold)


def get_confidence_from_fourfold(fourfold):
    return fourfold[0] / (fourfold[0] + fourfold[1])


def jacquard_distance(set_1: typing.Set[str], set_2: typing.Set[str]) -> float:
    intersection = set_1.intersection(set_2)
    union = set_1.union(set_2)
    return (len(union) - len(intersection)) / len(union)


def dist_abs(val_1: float, val_2: float) -> float:
    return abs(val_1 - val_2)


def confidence_dist_rel(conf1, conf2):
    try:
        return abs(conf1 - conf2) / max(1 - conf1, 1 - conf2)
    except ZeroDivisionError:
        return 0


def support_dist_rel(supp1, supp2):
    try:
        return abs(supp1 - supp2) / max(supp1, supp2)
    except ZeroDivisionError:
        return 0


def cedent_dist_abs(cedent_1: typing.Set[str], cedent_2: typing.Set[str]) -> int | float:
    intersection = cedent_1.intersection(cedent_2)
    if not intersection:
        return float('inf')
    return len(cedent_1.union(cedent_2)) - len(intersection)


def cedent_dist_rel(cedent_1: typing.Set[str], cedent_2: typing.Set[str]) -> float:
    dist = jacquard_distance(cedent_1, cedent_2)
    if dist == 1:
        return float('inf')
    return dist


def rule_distance(
        x: typing.List[int], y: typing.List[int],
        df: pd.DataFrame = None,
        abs_ante_attr_diff_threshold: float | int = None,
        abs_succ_attr_diff_threshold: float | int = None,
        rel_ante_attr_diff_threshold: float | int = None,
        rel_succ_attr_diff_threshold: float | int = None,
        abs_supp_diff_threshold: float | int = None,
        abs_conf_diff_threshold: float | int = None,
) -> float:
    x = df.iloc[int(x[0])]
    y = df.iloc[int(y[0])]

    ante_x, succ_x, supp_x, conf_x = x.antecedent, x.succedent, float(x.support), float(x.confidence)
    ante_y, succ_y, supp_y, conf_y = y.antecedent, y.succedent, float(y.support), float(y.confidence)

    ante_metric, ante_threshold = (
        cedent_dist_abs, abs_ante_attr_diff_threshold
    ) if abs_ante_attr_diff_threshold is not None else (
        cedent_dist_rel, rel_ante_attr_diff_threshold
    )
    succ_metric, succ_threshold = (
        cedent_dist_abs, abs_succ_attr_diff_threshold
    ) if abs_succ_attr_diff_threshold is not None else (
        cedent_dist_rel, rel_succ_attr_diff_threshold
    )
    supp_metric, supp_threshold = (dist_abs, abs_supp_diff_threshold)
    conf_metric, conf_threshold = (dist_abs, abs_conf_diff_threshold)

    ante_dist = ante_metric(ante_x, ante_y)
    succ_dist = succ_metric(succ_x, succ_y)
    supp_dist = supp_metric(supp_x, supp_y)
    conf_dist = conf_metric(conf_x, conf_y)
    thresholds = [ante_threshold, succ_threshold, supp_threshold, conf_threshold]
    distances = [ante_dist, succ_dist, supp_dist, conf_dist]

    dist = float('inf') if any(threshold is not None and distance > threshold for threshold, distance in zip(thresholds, distances)) else sum(distances)

    # clustering requires float64, can't return inf
    return sys.float_info.max if dist == float('inf') else dist
