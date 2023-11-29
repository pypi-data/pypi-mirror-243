import pytest
from src.utagmsengine.utils.dataclasses_utils import DataclassesUtils
from src.utagmsengine.dataclasses import Comparison, Criterion


@pytest.fixture()
def refined_performance_table_dict_dummy():
    return [[26.0, 40.0, 44.0],  # 0 - A
            [2.0, 2.0, 68.0],  # 1 - B
            [18.0, 17.0, 14.0],  # 2 - C
            [35.0, 62.0, 25.0],  # 3 - D
            [7.0, 55.0, 12.0],  # 4 - E
            [25.0, 30.0, 12.0],  # 5 - F
            [9.0, 62.0, 88.0],  # 6 - G
            [0.0, 24.0, 73.0],  # 7 - H
            [6.0, 15.0, 100.0],  # 8 - I
            [16.0, 9.0, 0.0],  # 9 - J
            [26.0, 17.0, 17.0],  # 10 - K
            [62.0, 43.0, 0.0]]  # 11 - L


@pytest.fixture()
def performance_table_dict_dummy():
    return {
        'A': {'g1': 26.0, 'g2': 40.0, 'g3': 44.0},
        'B': {'g1': 2.0, 'g2': 2.0, 'g3': 68.0},
        'C': {'g1': 18.0, 'g2': 17.0, 'g3': 14.0},
        'D': {'g1': 35.0, 'g2': 62.0, 'g3': 25.0},
        'E': {'g1': 7.0, 'g2': 55.0, 'g3': 12.0},
        'F': {'g1': 25.0, 'g2': 30.0, 'g3': 12.0},
        'G': {'g1': 9.0, 'g2': 62.0, 'g3': 88.0},
        'H': {'g1': 0.0, 'g2': 24.0, 'g3': 73.0},
        'I': {'g1': 6.0, 'g2': 15.0, 'g3': 100.0},
        'J': {'g1': 16.0, 'g2': 9.0, 'g3': 0.0},
        'K': {'g1': 26.0, 'g2': 17.0, 'g3': 17.0},
        'L': {'g1': 62.0, 'g2': 43.0, 'g3': 0.0}
    }


@pytest.fixture()
def refined_comparisons_dummy():
    return [
        [6, 5, [], '>'],
        [5, 4, [], '>'],
        [3, 6, [], '=']
    ]


@pytest.fixture()
def comparisons_dummy():
    return [
        Comparison(alternative_1='G', alternative_2='F'),
        Comparison(alternative_1='F', alternative_2='E'),
        Comparison(alternative_1='D', alternative_2='G', sign='=')
    ]


@pytest.fixture()
def criterions_dummy():
    return [Criterion(criterion_id='1', gain=True), Criterion(criterion_id='1', gain=True), Criterion(criterion_id='1', gain=True)]


def test_refine_performance_table_dict(
        performance_table_dict_dummy,
        refined_performance_table_dict_dummy
):
    refined_performance_table_dict = DataclassesUtils.refine_performance_table_dict(
        performance_table_dict=performance_table_dict_dummy
    )

    assert refined_performance_table_dict == refined_performance_table_dict_dummy


def test_refine_comparisons(
        performance_table_dict_dummy,
        comparisons_dummy,
        refined_comparisons_dummy
):
    refined_comparisons = DataclassesUtils.refine_comparisons(
        performance_table_dict=performance_table_dict_dummy,
        comparisons=comparisons_dummy
    )

    assert refined_comparisons == refined_comparisons_dummy



