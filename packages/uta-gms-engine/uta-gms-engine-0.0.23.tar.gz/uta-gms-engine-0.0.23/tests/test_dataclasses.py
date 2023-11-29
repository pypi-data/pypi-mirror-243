import pytest
from src.utagmsengine.dataclasses import Comparison, Criterion, DataValidator, Position


@pytest.fixture()
def performance_table_list_dummy():
    return {
        'A': {'g1': 26.0, 'g2': 40.0, 'g4': 44.0},
        'B': {'a1': 2.0, 'g2': 2.0, 'g4': 68.0},
        'C': {'g1': 18.0, 'g2': 17.0, 'g4': 14.0},
        'D': {'g1': 35.0, 'g2': 62.0, 'g4': 25.0},
        'E': {'g1': 7.0, 'g2': 55.0, 'g4': 12.0},
        'F': {'g1': 25.0, 'g2': 30.0, 'g4': 12.0},
        'G': {'g1': 9.0, 'g2': 62.0, 'g4': 88.0},
        'H': {'g1': 0.0, 'g2': 24.0, 'g4': 73.0},
        'I': {'g1': 6.0, 'g2': 15.0, 'g4': 100.0},
        'J': {'g1': 16.0, 'g2': 9.0, 'g4': 0.0},
        'K': {'g1': 26.0, 'g2': 17.0, 'g4': 17.0},
        'L': {'g1': 62.0, 'g2': 43.0, 'g4': 0.0}
    }


@pytest.fixture()
def comparisons_list_dummy():
    return [
        {'alternative_1': 'G', 'alternative_2': 'F'},
        {'alternative_1': 'F', 'alternative_2': 'E'},
        {'alternative_1': 'D', 'alternative_2': 'G', 'sign': '='}
    ]


@pytest.fixture()
def criterion_list_dummy():
    return [
        {'criterion_id': 'g1', 'gain': True, 'number_of_linear_segments': 0},
        {'criterion_id': 'g2', 'gain': True, 'number_of_linear_segments': 0},
        {'criterion_id': 'g3', 'gain': True, 'number_of_linear_segments': 0},
    ]


@pytest.fixture()
def comparisons_dummy():
    return [
        Comparison(alternative_1='G', alternative_2='F', criteria=[], sign='>'),
        Comparison(alternative_1='F', alternative_2='E', criteria=[], sign='>'),
        Comparison(alternative_1='D', alternative_2='G', criteria=[], sign='=')
    ]


@pytest.fixture()
def criterions_dummy():
    return [Criterion(criterion_id='g1', gain=True, number_of_linear_segments=0), Criterion(criterion_id='g2', gain=True, number_of_linear_segments=0), Criterion(criterion_id='g3', gain=True, number_of_linear_segments=0)]


@pytest.fixture()
def positions_list_dummy():
    return [Position(alternative_id='M', worst_position=1, best_position=3)]


def test_comparisons(
        comparisons_list_dummy,
        comparisons_dummy
):
    comparisons = [Comparison(**data) for data in comparisons_list_dummy]

    assert comparisons == comparisons_dummy


def test_criterions(
        criterion_list_dummy,
        criterions_dummy
):
    criterions = [Criterion(**data) for data in criterion_list_dummy]

    assert criterions == criterions_dummy


def test_comparison_validation():
    with pytest.raises(ValueError, match="alternative_1 and alternative_2 options must be different."):
        Comparison(alternative_1='A', alternative_2='A')


def test_criterion_linear_segments_validation():
    with pytest.raises(ValueError, match="Number of linear segments can't be negative."):
        Criterion(criterion_id='g1', gain=True, number_of_linear_segments=-1)


def test_data_validator_validate_criteria(
        performance_table_list_dummy,
        criterions_dummy
):
    with pytest.raises(ValueError, match="Criterion IDs in the list and the data dictionary do not match."):
        DataValidator.validate_criteria(performance_table_list_dummy, criterions_dummy)


def test_data_validator_validate_performance_table(
        performance_table_list_dummy
):
    with pytest.raises(ValueError, match="Keys inside the inner dictionaries are not consistent."):
        DataValidator.validate_performance_table(performance_table_list_dummy)


def test_data_validator_validate_positions(
        positions_list_dummy,
        performance_table_list_dummy
):
    with pytest.raises(ValueError, match="Alternative IDs in the Position list and the data dictionary do not match."):
        DataValidator.validate_positions(positions_list_dummy, performance_table_list_dummy)

    with pytest.raises(ValueError, match="worst_position can't be negative."):
        Position(alternative_id='A', worst_position=-1, best_position=2)

    with pytest.raises(ValueError, match="best_position can't be negative."):
        Position(alternative_id='A', worst_position=1, best_position=-2)
