import pandas as pd

from coar.cluster import agglomerative_clustering
from tests.conftest import SUPP, CONF, ANTECEDENT_TYPE, SUCCEDENT_TYPE, MAX_SUPP

ABS_ATTR_DIFF_THRESHOLD = 1
REL_ATTR_DIFF_THRESHOLD = 0.2
SUPP_DIFF_THRESHOLD = 0.2
CONF_DIFF_THRESHOLD = 0.2


def test_identical_rules_abs_threshold_pass(rule_factory, cedent_factory):
    ante_1, succ_1 = cedent_factory(1, ANTECEDENT_TYPE), cedent_factory(1, SUCCEDENT_TYPE)
    df = pd.DataFrame.from_records([rule_factory(ante_1, succ_1, SUPP, CONF)] * 2)
    clustering = agglomerative_clustering(
        df, abs_ante_attr_diff_threshold=0, abs_succ_attr_diff_threshold=0,
        abs_supp_diff_threshold=0,
        abs_conf_diff_threshold=0,
    )
    assert len(set(clustering['cluster'])) == 1


def test_identical_rules_rel_threshold_pass(rule_factory, cedent_factory, attr_factory):
    ante_1, succ_1 = cedent_factory(1, ANTECEDENT_TYPE), cedent_factory(1, SUCCEDENT_TYPE)
    df = pd.DataFrame.from_records([rule_factory(ante_1, succ_1, SUPP, CONF)] * 2)
    clustering = agglomerative_clustering(
        df, rel_ante_attr_diff_threshold=REL_ATTR_DIFF_THRESHOLD, rel_succ_attr_diff_threshold=REL_ATTR_DIFF_THRESHOLD,
        abs_supp_diff_threshold=SUPP_DIFF_THRESHOLD,
        abs_conf_diff_threshold=CONF_DIFF_THRESHOLD,
    )
    assert len(set(clustering['cluster'])) == 1


def test_ante_diff_abs_threshold_fail(rule_factory, cedent_factory, attr_factory):
    ante_1, succ_1 = cedent_factory(1, ANTECEDENT_TYPE), cedent_factory(1, SUCCEDENT_TYPE)
    ante_2, succ_2 = cedent_factory(1, ANTECEDENT_TYPE), cedent_factory(1, SUCCEDENT_TYPE)
    ante_2.add(attr_factory(2, ANTECEDENT_TYPE))
    ante_2.add(attr_factory(3, ANTECEDENT_TYPE))
    df = pd.DataFrame.from_records([rule_factory(ante_1, succ_1, SUPP, CONF), rule_factory(ante_2, succ_2, SUPP, CONF)])
    clustering = agglomerative_clustering(
        df, abs_ante_attr_diff_threshold=ABS_ATTR_DIFF_THRESHOLD, abs_succ_attr_diff_threshold=ABS_ATTR_DIFF_THRESHOLD,
        abs_supp_diff_threshold=SUPP_DIFF_THRESHOLD,
        abs_conf_diff_threshold=CONF_DIFF_THRESHOLD,
    )
    assert len(set(clustering['cluster'])) == 2


def test_succ_diff_rel_threshold_fail(rule_factory, cedent_factory, attr_factory):
    ante_1, succ_1 = cedent_factory(1, ANTECEDENT_TYPE), cedent_factory(1, SUCCEDENT_TYPE)
    ante_2, succ_2 = cedent_factory(1, ANTECEDENT_TYPE), cedent_factory(1, SUCCEDENT_TYPE)
    succ_2.add(attr_factory(2, SUCCEDENT_TYPE))
    df = pd.DataFrame.from_records([rule_factory(ante_1, succ_1, SUPP, CONF), rule_factory(ante_2, succ_2, SUPP, CONF)])
    clustering = agglomerative_clustering(
        df, rel_ante_attr_diff_threshold=REL_ATTR_DIFF_THRESHOLD, rel_succ_attr_diff_threshold=REL_ATTR_DIFF_THRESHOLD,
        abs_supp_diff_threshold=SUPP_DIFF_THRESHOLD,
        abs_conf_diff_threshold=CONF_DIFF_THRESHOLD,
    )
    assert len(set(clustering['cluster'])) == 2


def test_supp_diff_threshold_fail(rule_factory, cedent_factory, attr_factory):
    ante_1, succ_1 = ante_2, succ_2 = cedent_factory(1, ANTECEDENT_TYPE), cedent_factory(1, SUCCEDENT_TYPE)
    df = pd.DataFrame.from_records(
        [rule_factory(ante_1, succ_1, SUPP, CONF), rule_factory(ante_2, succ_2, MAX_SUPP, CONF)])
    clustering = agglomerative_clustering(
        df, abs_ante_attr_diff_threshold=ABS_ATTR_DIFF_THRESHOLD, abs_succ_attr_diff_threshold=ABS_ATTR_DIFF_THRESHOLD,
        abs_supp_diff_threshold=SUPP_DIFF_THRESHOLD,
        abs_conf_diff_threshold=CONF_DIFF_THRESHOLD,
    )
    assert len(set(clustering['cluster'])) == 2


def test_cluster_n_clusters_natural_clusters(rule_factory, cedent_factory):
    all_attrs_ante = sorted(list(cedent_factory(5, ANTECEDENT_TYPE)))
    succ = cedent_factory(1, SUCCEDENT_TYPE)
    df = pd.DataFrame.from_records([
        rule_factory(set(all_attrs_ante[1:3]), succ, SUPP, CONF),
        rule_factory(set(all_attrs_ante[:3]), succ, SUPP, CONF),
        rule_factory(set(all_attrs_ante[2:]), succ, SUPP, CONF),
        rule_factory(set(all_attrs_ante[2:4]), succ, SUPP, CONF),
                                    ])
    clustering = agglomerative_clustering(
        df, n_clusters=2
    )
    assert len(set(clustering['cluster'])) == 2
    assert clustering.iloc[0, df.columns.get_loc('cluster')] == clustering.iloc[1, df.columns.get_loc('cluster')]
    assert clustering.iloc[2, df.columns.get_loc('cluster')] == clustering.iloc[3, df.columns.get_loc('cluster')]
    assert clustering.iloc[0, df.columns.get_loc('cluster')] != clustering.iloc[2, df.columns.get_loc('cluster')]
