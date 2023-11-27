from typing import List, Dict
from ..dataclasses import Preference, Indifference, Position, Intensity


class DataclassesUtils:

    @staticmethod
    def refine_performance_table_dict(
            performance_table_dict: Dict[str, Dict[str, float]]
    ) -> List[List[float]]:
        """
        Convert a dictionary of performance table values into a 2D list of floats.

        :param performance_table_dict:
        :return output_list:
        """
        output_list = []
        for key in performance_table_dict:
            inner_list = list(performance_table_dict[key].values())
            output_list.append(inner_list)

        return output_list

    @staticmethod
    def refine_preferences(
            performance_table_dict: Dict[str, Dict[str, float]],
            preferences
    ) -> List[List[int]]:
        """
        Convert a list of Preferences into a list of indices corresponding to alternatives.

        :param performance_table_dict:
        :param preferences:
        :return output:
        """
        output = []
        keys = list(performance_table_dict.keys())

        for preference in preferences:
            superior_index = keys.index(preference.superior)
            inferior_index = keys.index(preference.inferior)

            first = next(iter(performance_table_dict.values()))  # Get the first dictionary value
            criteria_index = []
            for criteria in preference.criteria:
                position = list(first.keys()).index(criteria)
                criteria_index.append(position)

            output.append([superior_index, inferior_index, criteria_index])

        return output

    @staticmethod
    def refine_indifferences(
            performance_table_dict: Dict[str, Dict[str, float]],
            indifferences
    ) -> List[List[int]]:
        """
        Convert a list of Indifferences into a list of indices corresponding to alternatives.

        :param performance_table_dict:
        :param indifferences:
        :return output:
        """
        output = []
        keys = list(performance_table_dict.keys())

        for indifference in indifferences:
            equal1_index = keys.index(indifference.equal1)
            equal2_index = keys.index(indifference.equal2)

            first = next(iter(performance_table_dict.values()))  # Get the first dictionary value
            criteria_index = []
            for criteria in indifference.criteria:
                position = list(first.keys()).index(criteria)
                criteria_index.append(position)

            output.append([equal1_index, equal2_index, criteria_index])

        return output

    @staticmethod
    def refine_gains(
            criterions
    ) -> List[bool]:
        """
        Extract gains/costs from a list of Criterion objects.

        :param criterions:

        :return output:
        """
        output = []

        for criterion in criterions:
            output.append(criterion.gain)

        return output

    @staticmethod
    def refine_linear_segments(
            criterions
    ) -> List[int]:
        """
        Extract number of linear segments from a list of Criterion objects.

        :param criterions:

        :return output:
        """
        output = []

        for criterion in criterions:
            output.append(criterion.number_of_linear_segments)

        return output

    @staticmethod
    def refine_positions(
            positions,
            performance_table_dict
    ) -> List[List[int]]:
        """
        Refined list[Positions] to [[alternative_ID, worst_position, best_position], ...] format

        :param positions:
        :param performance_table_dict:

        :return output:
        """
        output = []
        tmp = {}

        for i, key in enumerate(performance_table_dict.keys()):
            tmp[key] = i

        for position in positions:
            first = next(iter(performance_table_dict.values()))  # Get the first dictionary value
            criteria_index = []
            for criteria in position.criteria:
                index = list(first.keys()).index(criteria)
                criteria_index.append(index)

            output.append([tmp[position.alternative_id], position.worst_position, position.best_position, criteria_index])

        return output

    @staticmethod
    def refine_intensities(
            intensities,
            performance_table_dict
    ) -> List[List[int]]:
        """
        Refine into [[1,[],3,[],4,[],5,[],'>']], meaning 1-3 > 4-5

        :param intensities:
        :param performance_table_dict:

        :return output:
        """
        output = []
        tmp = {}

        for i, key in enumerate(performance_table_dict.keys()):
            tmp[key] = i

        for intensity in intensities:
            first = next(iter(performance_table_dict.values()))  # Get the first dictionary value
            criteria_index = []
            for criteria in intensity.criteria:
                index = list(first.keys()).index(criteria)
                criteria_index.append(index)

            output.append(
                [
                    tmp[intensity.alternative_id_1],
                    criteria_index,
                    tmp[intensity.alternative_id_2],
                    criteria_index,
                    tmp[intensity.alternative_id_3],
                    criteria_index,
                    tmp[intensity.alternative_id_4],
                    criteria_index,
                    intensity.sign
                ]
            )

        return output

    @staticmethod
    def refine_resolved_inconsistencies(
            resolved_inconsistencies,
            performance_table_dict,
    ) -> List[List[int]]:
        """
        Refine from [[1,[],3,[],4,[],5,[],'>']], meaning 1-3 > 4-5 into dataclasses

        :param resolved_inconsistencies:
        :param performance_table_dict:

        :return output:
        """
        output = []
        alt_idx = {}
        crit_idx = {}

        for i, key in enumerate(performance_table_dict.keys()):
            alt_idx[i] = key

        for i, key in enumerate(performance_table_dict[alt_idx[0]]):
            crit_idx[i] = key

        for inconsistencies in resolved_inconsistencies:
            preferences = []
            indifferences = []
            positions = []
            intensities = []

            for preference in inconsistencies[0]:
                preferences.append(
                    Preference(superior=alt_idx[preference[0]], inferior=alt_idx[preference[1]], criteria=preference[2])
                )

            for indifference in inconsistencies[1]:
                indifferences.append(
                    Indifference(equal1=alt_idx[indifference[0]], equal2=alt_idx[indifference[1]], criteria=indifference[2])
                )

            for position in inconsistencies[2]:
                positions.append(
                    Position(alternative_id=alt_idx[position[0]], worst_position=position[1], best_position=position[2], criteria=position[3])
                )

            for intensity in inconsistencies[3]:
                intensities.append(
                    Intensity(
                        alternative_id_1=alt_idx[intensity[0]],
                        alternative_id_2=alt_idx[intensity[2]],
                        alternative_id_3=alt_idx[intensity[4]],
                        alternative_id_4=alt_idx[intensity[6]],
                        criteria=[crit_idx[idx] for idx in intensity[1]],
                        sign=intensity[8]
                    )
                )

            output.append(
                [
                    preferences,
                    indifferences,
                    positions,
                    intensities
                 ]
            )

        return output[:-1]
