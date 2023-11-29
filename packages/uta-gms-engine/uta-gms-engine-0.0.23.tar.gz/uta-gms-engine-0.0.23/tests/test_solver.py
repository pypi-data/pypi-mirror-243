import pytest
from src.utagmsengine.solver import Solver, Inconsistency
from src.utagmsengine.dataclasses import Comparison, Criterion, Position, Intensity


@pytest.fixture()
def performance_table_dict_dummy():
    return {
        'A': {'g1': 26.0, 'g2': 40.0, 'g3': 44.0},
        'B': {'g1': 2.0, 'g2': 2.0, 'g3': 68.0},
        'C': {'g1': 18.0, 'g2': 17.0, 'g3': 14.0},
        'D': {'g1': 35.0, 'g2': 62.0, 'g3': 25.0},
        'E': {'g1': -7.0, 'g2': 55.0, 'g3': 12.0},
        'F': {'g1': 25.0, 'g2': 30.0, 'g3': 12.0},
        'G': {'g1': 9.0, 'g2': 62.0, 'g3': 88.0},
        'H': {'g1': 0.0, 'g2': 24.0, 'g3': 73.0},
        'I': {'g1': 6.0, 'g2': 15.0, 'g3': 100.0},
        'J': {'g1': 16.0, 'g2': -9.0, 'g3': 0.0},
        'K': {'g1': 26.0, 'g2': 17.0, 'g3': 17.0},
        'L': {'g1': 62.0, 'g2': 43.0, 'g3': 0.0}
    }


@pytest.fixture()
def comparison_dummy():
    return [
        Comparison(alternative_1='G', alternative_2='F', sign='>'),
        Comparison(alternative_1='F', alternative_2='E', sign='>'),
        Comparison(alternative_1='D', alternative_2='G', sign='='),
    ]


@pytest.fixture()
def criterions_dummy():
    return [Criterion(criterion_id='g1', gain=True, number_of_linear_segments=0), Criterion(criterion_id='g2', gain=True, number_of_linear_segments=0), Criterion(criterion_id='g3', gain=True, number_of_linear_segments=0)]


@pytest.fixture()
def predefined_criterions_dummy():
    return [Criterion(criterion_id='g1', gain=True, number_of_linear_segments=4), Criterion(criterion_id='g2', gain=True, number_of_linear_segments=4), Criterion(criterion_id='g3', gain=True, number_of_linear_segments=4)]


@pytest.fixture()
def positions_dummy():
    return [Position(alternative_id='A', worst_position=12, best_position=2)]


@pytest.fixture()
def intensities_dummy():
    return [Intensity(alternative_id_1='H', alternative_id_2='G', alternative_id_3='B', alternative_id_4='D', criteria=['g1', 'g2'])]


@pytest.fixture()
def resolved_inconsistencies_dummy():
    return [[[], [], [Position(alternative_id='A', worst_position=12, best_position=9, criteria=[])], []], [[Comparison(alternative_1='G', alternative_2='F', criteria=[], sign='>')], [], [], []], [[], [Comparison(alternative_1='D', alternative_2='G', criteria=[], sign='=')], [], []]]


@pytest.fixture()
def hasse_diagram_dict_dummy():
    return {'A': ['F', 'K'], 'C': ['J'], 'D': ['G'], 'F': ['E', 'J'], 'G': ['B', 'D', 'F', 'H', 'K'], 'I': ['B'], 'K': ['C'], 'L': ['J'], 'B': [], 'E': [], 'H': [], 'J': []}


@pytest.fixture()
def representative_value_function_dict_dummy():
    return {'J': 0.1015, 'E': 0.1821, 'C': 0.2716, 'L': 0.3663, 'F': 0.3889, 'B': 0.4101, 'H': 0.4416, 'K': 0.4417, 'A': 0.6117, 'D': 0.6117, 'G': 0.6117, 'I': 0.629}


@pytest.fixture()
def criterion_functions_dummy():
    return {'g1': [(0.0, 0.0), (2.0, 0.0), (6.0, 0.0), (7.0, 0.0), (9.0, 0.0), (10.25, 0.0), (16.0, 0.10148), (18.0, 0.136777), (25.0, 0.260318), (26.0, 0.277966), (27.5, 0.304439), (35.0, 0.304439), (44.75, 0.304439), (62.0, 0.304439)], 'g2': [(2.0, 0.0), (8.75, 0.0), (9.0, 0.0), (15.0, 0.0), (17.0, 0.0), (24.0, 0.0), (26.5, 0.0), (30.0, 0.0131292), (40.0, 0.050641), (43.0, 0.0618946), (44.25, 0.0665836), (55.0, 0.0665836), (62.0, 0.0665836)], 'g3': [(0.0, 0.0), (12.0, 0.115518), (14.0, 0.134772), (17.0, 0.163651), (25.0, 0.240663), (44.0, 0.283079), (50.0, 0.296473), (68.0, 0.410064), (73.0, 0.441617), (75.0, 0.454239), (88.0, 0.545103), (100.0, 0.628977)]}


@pytest.fixture()
def predefined_hasse_diagram_dict_dummy():
    return {'A': ['F', 'K'], 'C': ['J'], 'D': ['G'], 'F': ['E', 'J'], 'G': ['B', 'D', 'F', 'H', 'K'], 'I': ['B'], 'K': ['C'], 'L': ['J'], 'B': [], 'E': [], 'H': [], 'J': []}


def test_get_hasse_diagram_dict(
        performance_table_dict_dummy,
        comparison_dummy,
        criterions_dummy,
        positions_dummy,
        intensities_dummy,
        hasse_diagram_dict_dummy
):
    solver = Solver(show_logs=True)

    hasse_diagram_list = solver.get_hasse_diagram_dict(
        performance_table_dict_dummy,
        comparison_dummy,
        criterions_dummy,
        positions_dummy,
        intensities_dummy
    )

    assert hasse_diagram_list == hasse_diagram_dict_dummy


def test_get_representative_value_function_dict(
        performance_table_dict_dummy,
        comparison_dummy,
        predefined_criterions_dummy,
        criterions_dummy,
        positions_dummy,
        intensities_dummy,
        representative_value_function_dict_dummy,
        criterion_functions_dummy,
        resolved_inconsistencies_dummy
):
    solver = Solver(show_logs=True)

    try:
        representative_value_function_dict, criterion_functions, sampler_metrics = solver.get_representative_value_function_dict(
            performance_table_dict_dummy,
            comparison_dummy,
            predefined_criterions_dummy,
            positions_dummy,
            intensities_dummy,
            'files/polyrun-1.1.0-jar-with-dependencies.jar',
            '10'
        )

        assert representative_value_function_dict == representative_value_function_dict_dummy
        assert criterion_functions == criterion_functions_dummy

    except Inconsistency as e:
        resolved_inconsistencies = e.data

        assert resolved_inconsistencies == resolved_inconsistencies_dummy


def test_predefined_get_hasse_diagram_dict(
        performance_table_dict_dummy,
        comparison_dummy,
        predefined_criterions_dummy,
        positions_dummy,
        predefined_hasse_diagram_dict_dummy
):
    solver = Solver(show_logs=True)

    hasse_diagram_list = solver.get_hasse_diagram_dict(
        performance_table_dict_dummy,
        comparison_dummy,
        predefined_criterions_dummy,
        positions_dummy
    )

    assert hasse_diagram_list == predefined_hasse_diagram_dict_dummy
