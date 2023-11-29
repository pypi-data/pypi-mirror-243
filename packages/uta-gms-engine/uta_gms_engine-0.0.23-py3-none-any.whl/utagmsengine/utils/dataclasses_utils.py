from typing import List, Dict
from ..dataclasses import Comparison, Position, Intensity


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
    def refine_comparisons(
            performance_table_dict: Dict[str, Dict[str, float]],
            comparisons
    ) -> List[List[int]]:
        """
        Convert a list of Comparison into a list of indices corresponding to alternatives.

        :param performance_table_dict:
        :param comparisons:
        :return output:
        """
        output = []
        keys: List[str] = list(performance_table_dict.keys())

        for comparison in comparisons:
            alternative_1_index: int = keys.index(comparison.alternative_1)
            alternative_2_index: int = keys.index(comparison.alternative_2)
            sign: str = comparison.sign

            first: Dict[str, float] = next(iter(performance_table_dict.values()))  # Get the first dictionary value
            criteria_index: List[int] = []
            for criteria in comparison.criteria:
                position = list(first.keys()).index(criteria)
                criteria_index.append(position)

            output.append([alternative_1_index, alternative_2_index, criteria_index, sign])

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
            if criterion.number_of_linear_segments == 0:
                linear_segments = 0
            else:
                linear_segments = criterion.number_of_linear_segments + 1
            output.append(linear_segments)

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
            comparisons = []
            positions = []
            intensities = []

            for comparison in inconsistencies[0]:
                comparisons.append(
                    Comparison(alternative_1=alt_idx[comparison[0]], alternative_2=alt_idx[comparison[1]], criteria=[crit_idx[idx] for idx in comparison[2]], sign=comparison[3])
                )

            for position in inconsistencies[1]:
                positions.append(
                    Position(alternative_id=alt_idx[position[0]], worst_position=position[1], best_position=position[2], criteria=[crit_idx[idx] for idx in position[3]])
                )

            for intensity in inconsistencies[2]:
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
                    comparisons,
                    positions,
                    intensities
                 ]
            )

        return output[:-1]
