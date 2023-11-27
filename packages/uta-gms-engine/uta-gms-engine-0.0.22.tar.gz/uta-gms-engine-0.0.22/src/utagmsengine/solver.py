from typing import List, Dict, Optional, Tuple
from .utils.solver_utils import SolverUtils
from .utils.dataclasses_utils import DataclassesUtils
from .dataclasses import Preference, Indifference, Criterion, DataValidator, Position, Intensity


class Inconsistency(Exception):
    def __init__(self, message, data=None):
        super().__init__(message)
        self.data = data


class Solver:

    def __init__(self, show_logs: Optional[bool] = False):
        self.name = 'UTA GMS Solver'
        self.show_logs = show_logs

    def __str__(self):
        return self.name

    def get_hasse_diagram_dict(
            self,
            performance_table_dict: Dict[str, Dict[str, float]],
            preferences: List[Preference],
            indifferences: List[Indifference],
            criteria: List[Criterion],
            positions: Optional[List[Position]] = [],
            intensities: Optional[List[Intensity]] = [],
    ) -> Dict[str, List[str]]:
        """
        Method for getting hasse diagram dict

        :param intensities:
        :param performance_table_dict:
        :param preferences: List of Preference objects
        :param indifferences: List of Indifference objects
        :param criteria: List of Criterion objects
        :param positions: List of Position objects

        :return direct_relations:
        """
        DataValidator.validate_criteria(performance_table_dict, criteria)
        DataValidator.validate_performance_table(performance_table_dict)
        DataValidator.validate_positions(positions, performance_table_dict)

        refined_performance_table_dict: List[List[float]] = DataclassesUtils.refine_performance_table_dict(
            performance_table_dict=performance_table_dict
        )

        refined_preferences: List[List[int]] = DataclassesUtils.refine_preferences(
            performance_table_dict=performance_table_dict,
            preferences=preferences
        )

        refined_indifferences: List[List[int]] = DataclassesUtils.refine_indifferences(
            performance_table_dict=performance_table_dict,
            indifferences=indifferences
        )

        refined_gains: List[bool] = DataclassesUtils.refine_gains(
            criterions=criteria
        )

        refined_linear_segments: List[int] = DataclassesUtils.refine_linear_segments(
            criterions=criteria
        )

        refined_worst_best_position: List[List[int]] = DataclassesUtils.refine_positions(
            positions=positions,
            performance_table_dict=performance_table_dict
        )

        refined_intensities: List[List[int]] = DataclassesUtils.refine_intensities(
            intensities=intensities,
            performance_table_dict=performance_table_dict
        )

        alternatives_id_list: List[str] = list(performance_table_dict.keys())

        necessary_preference = SolverUtils.get_necessary_relations(
            performance_table_list=refined_performance_table_dict,
            alternatives_id_list=alternatives_id_list,
            preferences=refined_preferences,
            indifferences=refined_indifferences,
            criteria=refined_gains,
            worst_best_position=refined_worst_best_position,
            number_of_points=refined_linear_segments,
            comprehensive_intensities=refined_intensities,
            show_logs=self.show_logs
        )

        direct_relations: Dict[str, List[str]] = SolverUtils.calculate_direct_relations(necessary_preference)

        for alternatives_id in alternatives_id_list:
            if alternatives_id not in direct_relations.keys():
                direct_relations[alternatives_id] = []

        return direct_relations

    def get_representative_value_function_dict(
            self,
            performance_table_dict: Dict[str, Dict[str, float]],
            preferences: List[Preference],
            indifferences: List[Indifference],
            criteria: List[Criterion],
            positions: Optional[List[Position]] = [],
            intensities: Optional[List[Intensity]] = [],
            sampler_path: str = 'files/polyrun-1.1.0-jar-with-dependencies.jar',
            number_of_samples: str = '100'
    ) -> Tuple[Dict[str, float], Dict[str, List[Tuple[float, float]]], Dict[str, List[int]]]:
        """
        Method for getting The Most Representative Value Function

        :param intensities:
        :param performance_table_dict:
        :param preferences: List of Preference objects
        :param indifferences: List of Indifference objects
        :param criteria: List of Criterion objects
        :param positions: List of Position objects
        :param sampler_path:
        :param number_of_samples:


        :return:
        """
        DataValidator.validate_criteria(performance_table_dict, criteria)
        DataValidator.validate_performance_table(performance_table_dict)
        DataValidator.validate_positions(positions, performance_table_dict)
        DataValidator.validate_preferences_indifferences_criteria(preferences, indifferences, positions, criteria)

        refined_performance_table_dict: List[List[float]] = DataclassesUtils.refine_performance_table_dict(
            performance_table_dict=performance_table_dict
        )

        refined_preferences: List[List[int]] = DataclassesUtils.refine_preferences(
            performance_table_dict=performance_table_dict,
            preferences=preferences
        )

        refined_indifferences: List[List[int]] = DataclassesUtils.refine_indifferences(
            performance_table_dict=performance_table_dict,
            indifferences=indifferences
        )

        refined_gains: List[bool] = DataclassesUtils.refine_gains(
            criterions=criteria
        )

        refined_linear_segments: List[int] = DataclassesUtils.refine_linear_segments(
            criterions=criteria
        )

        refined_worst_best_position: List[List[int]] = DataclassesUtils.refine_positions(
            positions=positions,
            performance_table_dict=performance_table_dict
        )

        refined_intensities: List[List[int]] = DataclassesUtils.refine_intensities(
            intensities=intensities,
            performance_table_dict=performance_table_dict
        )

        alternatives_id_list: List[str] = list(performance_table_dict.keys())

        problem, sampler_metrics = SolverUtils.calculate_the_most_representative_function(
            performance_table_list=refined_performance_table_dict,
            alternatives_id_list=alternatives_id_list,
            preferences=refined_preferences,
            indifferences=refined_indifferences,
            criteria=refined_gains,
            worst_best_position=refined_worst_best_position,
            number_of_points=refined_linear_segments,
            comprehensive_intensities=refined_intensities,
            show_logs=self.show_logs,
            sampler_path=sampler_path,
            number_of_samples=number_of_samples
        )

        for variable in problem.variables():
            if variable.name == 'epsilon':
                if variable.varValue <= 0.0:
                    resolved_inconsistencies = SolverUtils.resolve_incosistency(
                        performance_table_list=refined_performance_table_dict,
                        preferences=refined_preferences,
                        indifferences=refined_indifferences,
                        criteria=refined_gains,
                        worst_best_position=refined_worst_best_position,
                        number_of_points=refined_linear_segments,
                        comprehensive_intensities=refined_intensities,
                        subsets_to_remove=[],
                        show_logs=self.show_logs
                    )

                    refined_resolved_inconsistencies = DataclassesUtils.refine_resolved_inconsistencies(
                        resolved_inconsistencies=resolved_inconsistencies,
                        performance_table_dict=performance_table_dict
                    )

                    raise Inconsistency("Found inconsistencies", refined_resolved_inconsistencies)
                break

        variables_and_values_dict: Dict[str, float] = {variable.name: variable.varValue for variable in problem.variables()}

        criterion_functions: Dict[str, List[Tuple[float, float]]] = SolverUtils.get_criterion_functions(
            variables_and_values_dict=variables_and_values_dict,
            criteria=criteria,
        )

        alternatives_and_utilities_dict: Dict[str, float] = SolverUtils.get_alternatives_and_utilities_dict(
            variables_and_values_dict=variables_and_values_dict,
            performance_table_list=refined_performance_table_dict,
            alternatives_id_list=alternatives_id_list,
        )

        return alternatives_and_utilities_dict, criterion_functions, sampler_metrics
