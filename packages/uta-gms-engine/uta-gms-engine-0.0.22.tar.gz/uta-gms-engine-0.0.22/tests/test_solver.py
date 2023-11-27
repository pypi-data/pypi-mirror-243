import pytest
from src.utagmsengine.solver import Solver, Inconsistency
from src.utagmsengine.dataclasses import Preference, Indifference, Criterion, Position, Intensity


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
def preferences_dummy():
    return [Preference(superior='G', inferior='F'), Preference(superior='F', inferior='E')]


@pytest.fixture()
def indifferences_dummy():
    return [Indifference(equal1='D', equal2='G')]


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
    return [[[], [], [Position(alternative_id='A', worst_position=12, best_position=9, criteria=[])], []], [[Preference(superior='G', inferior='F', criteria=[])], [], [], []], [[], [Indifference(equal1='D', equal2='G', criteria=[])], [], []]]


@pytest.fixture()
def hasse_diagram_dict_dummy():
    return {'A': ['F', 'K'], 'C': ['J'], 'D': ['G'], 'F': ['E', 'J'], 'G': ['B', 'D', 'F', 'H', 'K'], 'I': ['B'], 'K': ['C'], 'L': ['J'], 'B': [], 'E': [], 'H': [], 'J': []}


@pytest.fixture()
def representative_value_function_dict_dummy():
    return {'J': 0.0338, 'E': 0.1663, 'C': 0.196, 'F': 0.3015, 'K': 0.3311, 'B': 0.3344, 'H': 0.3972, 'L': 0.3972, 'A': 0.5323, 'D': 0.5756, 'G': 0.5756, 'I': 0.6227}


@pytest.fixture()
def criterion_functions_dummy():
    return {'g1': [(0.0, 0.0102816), (2.0, 0.0132191), (6.0, 0.0190943), (7.0, 0.0), (9.0, 0.0235007), (16.0, 0.0337822), (18.0, 0.0606056), (25.0, 0.154487), (26.0, 0.167899), (35.0, 0.288604), (39.0, 0.342251), (62.0, 0.342251)], 'g2': [(2.0, 0.0), (9.0, 0.0), (14.666666666666664, 0.0), (15.0, 0.000773555), (17.0, 0.00541489), (24.0, 0.0216596), (30.0, 0.0355836), (38.33333333333333, 0.0549224), (40.0, 0.0549224), (43.0, 0.0549224), (55.0, 0.0549224), (62.0, 0.0549224)], 'g3': [(0.0, 0.0), (12.0, 0.11142), (14.0, 0.12999), (17.0, 0.157845), (25.0, 0.232125), (33.33333333333333, 0.309501), (44.0, 0.309501), (66.66666666666666, 0.309501), (68.0, 0.321234), (73.0, 0.365232), (88.0, 0.497229), (100.0, 0.602826)]}


@pytest.fixture()
def predefined_hasse_diagram_dict_dummy():
    return {'A': ['F', 'K'], 'C': ['J'], 'D': ['G'], 'F': ['E', 'J'], 'G': ['B', 'D', 'F', 'H', 'K'], 'I': ['B'], 'K': ['C'], 'L': ['J'], 'B': [], 'E': [], 'H': [], 'J': []}


def test_get_hasse_diagram_dict(
        performance_table_dict_dummy,
        preferences_dummy,
        indifferences_dummy,
        criterions_dummy,
        positions_dummy,
        intensities_dummy,
        hasse_diagram_dict_dummy
):
    solver = Solver(show_logs=True)

    hasse_diagram_list = solver.get_hasse_diagram_dict(
        performance_table_dict_dummy,
        preferences_dummy,
        indifferences_dummy,
        criterions_dummy,
        positions_dummy,
        intensities_dummy
    )

    assert hasse_diagram_list == hasse_diagram_dict_dummy


def test_get_representative_value_function_dict(
        performance_table_dict_dummy,
        preferences_dummy,
        indifferences_dummy,
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
            preferences_dummy,
            indifferences_dummy,
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
        preferences_dummy,
        indifferences_dummy,
        predefined_criterions_dummy,
        positions_dummy,
        predefined_hasse_diagram_dict_dummy
):
    solver = Solver(show_logs=True)

    hasse_diagram_list = solver.get_hasse_diagram_dict(
        performance_table_dict_dummy,
        preferences_dummy,
        indifferences_dummy,
        predefined_criterions_dummy,
        positions_dummy
    )

    assert hasse_diagram_list == predefined_hasse_diagram_dict_dummy
