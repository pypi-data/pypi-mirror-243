from pydantic import BaseModel, field_validator
from typing import List


class Comparison(BaseModel):
    """
    Pydantic dataclass - Represents a comparison between two options.
    """
    alternative_1: str
    alternative_2: str
    criteria: List[str] = []
    sign: str = '>'

    @field_validator("alternative_2")
    def check_different(cls, alternative_2, values):
        if "alternative_1" in values.data and alternative_2 == values.data["alternative_1"]:
            raise ValueError("alternative_1 and alternative_2 options must be different.")
        return alternative_2

    @field_validator("criteria")
    def check_unique_criteria(cls, criteria):
        if criteria and len(set(criteria)) != len(criteria):
            raise ValueError("Criteria list must contain unique elements.")
        return criteria


class Criterion(BaseModel):
    """
    Pydantic dataclass - Represents a decision criterion.

    Attributes:
        criterion_id (str): The unique identifier for the criterion.
        gain (bool): Whether the criterion represents a gain (True) or cost (False).
        number_of_linear_segments (int): The number of linear segments that the criterion has, if 0 then general function will be used
    """
    criterion_id: str
    gain: bool
    number_of_linear_segments: int

    @field_validator("number_of_linear_segments")
    def check_number_of_linear_segments(cls, number_of_linear_segments):
        if number_of_linear_segments < 0:
            raise ValueError("Number of linear segments can't be negative.")
        return number_of_linear_segments


class Position(BaseModel):
    alternative_id: str
    worst_position: int
    best_position: int
    criteria: List[str] = []

    @field_validator("worst_position")
    def check_worst_position(cls, worst_position):
        if worst_position < 0:
            raise ValueError("worst_position can't be negative.")
        return worst_position

    @field_validator("best_position")
    def check_max_position(cls, best_position):
        if best_position < 0:
            raise ValueError("best_position can't be negative.")
        return best_position

    @field_validator("criteria")
    def check_unique_criteria(cls, criteria):
        if criteria and len(set(criteria)) != len(criteria):
            raise ValueError("Criteria list must contain unique elements.")
        return criteria


class Intensity(BaseModel):
    """
    alternative_id_1 - alternative_id_2 >= alternative_id_3 - alternative_id_4 on given criteria
    """
    alternative_id_1: str
    alternative_id_2: str
    alternative_id_3: str
    alternative_id_4: str
    criteria: List[str] = []
    sign: str = '>='


class DataValidator:
    @staticmethod
    def validate_criteria(performance_table, criteria_list):
        """Validate whether Criterion IDs in performance_table and criteria_list match."""
        criteria_ids = {criterion.criterion_id for criterion in criteria_list}
        performance_table_ids = {key for item in performance_table.values() for key in item.keys()}

        if criteria_ids != performance_table_ids:
            raise ValueError("Criterion IDs in the list and the data dictionary do not match.")

    @staticmethod
    def validate_performance_table(performance_table):
        """Validate whether performance_table IDs are consistent"""
        keys_list = [set(inner_dict.keys()) for inner_dict in performance_table.values()]
        first_keys = keys_list[0]

        for keys in keys_list[1:]:
            if keys != first_keys:
                raise ValueError("Keys inside the inner dictionaries are not consistent.")

    @staticmethod
    def validate_positions(positions_list, performance_table):
        """Validate whether Alternative IDs in positions_list and performance_table match."""
        positions_ids = {position.alternative_id for position in positions_list}
        performance_table_ids = {key for key in performance_table.keys()}

        for position_id in positions_ids:
            if position_id not in performance_table_ids:
                raise ValueError("Alternative IDs in the Position list and the data dictionary do not match.")

        for position in positions_list:
            if position.worst_position < position.best_position:
                raise ValueError(f"worst_position can't be lower than best_position")

    @staticmethod
    def validate_comparisons_criteria(comparisons, positions, criteria):
        """Validate whether Alternative IDs in positions_list and performance_table match."""
        partial_criteria_list = []
        for comparison in comparisons:
            for criterion in comparison.criteria:
                if criterion not in partial_criteria_list:
                    partial_criteria_list.append(criterion)

        for position in positions:
            for criterion in position.criteria:
                if criterion not in partial_criteria_list:
                    partial_criteria_list.append(criterion)

        criteria_list = [criterion.criterion_id for criterion in criteria]

        for criterion in partial_criteria_list:
            if criterion not in criteria_list:
                raise ValueError("Criteria name from partial criteria does not match name in Criterion")
