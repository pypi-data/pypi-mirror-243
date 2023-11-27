from tempfile import TemporaryFile
from typing import Tuple, List, Dict

from pulp import LpVariable, LpProblem, LpMaximize, LpMinimize, lpSum, GLPK
from collections import defaultdict
import re
import subprocess


class SolverUtils:

    @staticmethod
    def calculate_solved_problem(
            performance_table_list: List[List[float]],
            preferences: List[List[int]],
            indifferences: List[List[int]],
            criteria: List[bool],
            worst_best_position: List[List[int]],
            number_of_points: List[int],
            comprehensive_intensities: List[List[int]],
            alternative_id_1: int = -1,
            alternative_id_2: int = -1,
            show_logs: bool = False,
    ) -> LpProblem:
        """
        Main calculation method for problem-solving.
        The idea is that this should be a generic method used across different problems

        :param comprehensive_intensities:
        :param performance_table_list:
        :param preferences:
        :param indifferences:
        :param criteria:
        :param worst_best_position:
        :param number_of_points:
        :param alternative_id_1: used only in calculation for hasse graphs
        :param alternative_id_2: used only in calculation for hasse graphs
        :param show_logs: default None

        :return problem:
        """
        problem: LpProblem = LpProblem("UTA-GMS", LpMaximize)

        epsilon: LpVariable = LpVariable("epsilon")

        u_list, u_list_dict = SolverUtils.create_variables_list_and_dict(performance_table_list)

        characteristic_points: List[List[float]] = SolverUtils.calculate_characteristic_points(
            number_of_points, performance_table_list, u_list_dict, u_list
        )

        u_list = [sorted(lp_var_list, key=lambda var: -float(var.name.split("_")[-1]) if len(var.name.split("_")) == 4 else float(var.name.split("_")[-1])) for lp_var_list in u_list]

        # Normalization constraints
        the_greatest_performance: List[LpVariable] = []
        for i in range(len(u_list)):
            if criteria[i]:
                the_greatest_performance.append(u_list[i][-1])
                problem += u_list[i][0] == 0
            else:
                the_greatest_performance.append(u_list[i][0])
                problem += u_list[i][-1] == 0

        problem += lpSum(the_greatest_performance) == 1

        u_list_of_characteristic_points: List[List[LpVariable]] = []
        for i in range(len(characteristic_points)):
            pom = []
            for j in range(len(characteristic_points[i])):
                pom.append(u_list_dict[i][float(characteristic_points[i][j])])
            u_list_of_characteristic_points.append(pom[:])

        # Monotonicity constraint
        for i in range(len(u_list_of_characteristic_points)):
            for j in range(1, len(u_list_of_characteristic_points[i])):
                if criteria[i]:
                    problem += u_list_of_characteristic_points[i][j] >= u_list_of_characteristic_points[i][j - 1]
                else:
                    problem += u_list_of_characteristic_points[i][j - 1] >= u_list_of_characteristic_points[i][j]

        # Bounds constraint
        for i in range(len(u_list_of_characteristic_points)):
            for j in range(1, len(u_list_of_characteristic_points[i]) - 1):
                if criteria[i]:
                    problem += u_list_of_characteristic_points[i][-1] >= u_list_of_characteristic_points[i][j]
                    problem += u_list_of_characteristic_points[i][j] >= u_list_of_characteristic_points[i][0]
                else:
                    problem += u_list_of_characteristic_points[i][0] >= u_list_of_characteristic_points[i][j]
                    problem += u_list_of_characteristic_points[i][j] >= u_list_of_characteristic_points[i][-1]

        # Preference constraint
        for preference in preferences:
            left_alternative: List[float] = performance_table_list[preference[0]]
            right_alternative: List[float] = performance_table_list[preference[1]]

            indices_to_keep: List[int] = preference[2]
            if indices_to_keep:
                left_alternative: List[float] = [left_alternative[i] for i in indices_to_keep]
                right_alternative: List[float] = [right_alternative[i] for i in indices_to_keep]
                left_side: List[LpVariable] = []
                right_side: List[LpVariable] = []
                for i in range(len(indices_to_keep)):
                    left_side.append(u_list_dict[indices_to_keep[i]][left_alternative[i]])
                    right_side.append(u_list_dict[indices_to_keep[i]][right_alternative[i]])
            else:
                left_side: List[LpVariable] = []
                right_side: List[LpVariable] = []
                for i in range(len(left_alternative)):
                    left_side.append(u_list_dict[i][left_alternative[i]])
                    right_side.append(u_list_dict[i][right_alternative[i]])

            problem += lpSum(left_side) >= lpSum(right_side) + epsilon

        # Indifference constraint
        for indifference in indifferences:
            left_alternative: List[float] = performance_table_list[indifference[0]]
            right_alternative: List[float] = performance_table_list[indifference[1]]

            indices_to_keep: List[int] = indifference[2]
            if indices_to_keep:
                left_alternative: List[float] = [left_alternative[i] for i in indices_to_keep]
                right_alternative: List[float] = [right_alternative[i] for i in indices_to_keep]
                left_side: List[LpVariable] = []
                right_side: List[LpVariable] = []
                for i in range(len(indices_to_keep)):
                    left_side.append(u_list_dict[indices_to_keep[i]][left_alternative[i]])
                    right_side.append(u_list_dict[indices_to_keep[i]][right_alternative[i]])
            else:
                left_side: List[LpVariable] = []
                right_side: List[LpVariable] = []
                for i in range(len(left_alternative)):
                    left_side.append(u_list_dict[i][left_alternative[i]])
                    right_side.append(u_list_dict[i][right_alternative[i]])

            problem += lpSum(left_side) == lpSum(right_side)

        if alternative_id_1 >= 0 and alternative_id_2 >= 0:
            left_alternative: List[float] = performance_table_list[alternative_id_2]
            right_alternative: List[float] = performance_table_list[alternative_id_1]

            left_side: List[LpVariable] = []
            right_side: List[LpVariable] = []
            for i in range(len(u_list_dict)):
                left_side.append(u_list_dict[i][left_alternative[i]])
                right_side.append(u_list_dict[i][right_alternative[i]])

            problem += lpSum(left_side) >= lpSum(right_side) + epsilon

        # Worst and Best position
        alternatives_variables: List[List[LpVariable]] = []
        for i in range(len(performance_table_list)):
            pom = []
            for j in range(len(u_list_dict)):
                pom.append(u_list_dict[j][performance_table_list[i][j]])
            alternatives_variables.append(pom[:])

        alternatives_binary_variables: Dict[int, List[Dict[int, LpVariable]]] = {}
        all_binary_variables = {}
        for i in worst_best_position:
            pom_dict = {}
            for j in range(len(performance_table_list)):
                pom = []
                if i[0] != j:
                    variable_1_name: str = f"v_{i[0]}_higher_than_{j}_criteria_{'_'.join(map(str, i[3]))}"
                    if variable_1_name not in all_binary_variables:
                        variable_1: LpVariable = LpVariable(variable_1_name, cat='Binary')
                        pom.append(variable_1)
                        all_binary_variables[variable_1_name] = variable_1
                    else:
                        pom.append(all_binary_variables[variable_1_name])

                    variable_2_name: str = f"v_{j}_higher_than_{i[0]}_criteria_{'_'.join(map(str, i[3]))}"
                    if variable_2_name not in all_binary_variables:
                        variable_2: LpVariable = LpVariable(variable_2_name, cat='Binary')
                        pom.append(variable_2)
                        all_binary_variables[variable_2_name] = variable_2
                    else:
                        pom.append(all_binary_variables[variable_2_name])

                    pom_dict[j] = pom[:]

            if i[0] not in alternatives_binary_variables:
                alternatives_binary_variables[i[0]] = []

            alternatives_binary_variables[i[0]].append(pom_dict)

        big_M: int = 1e20
        x: int = 0
        for worst_best in worst_best_position:
            if len(alternatives_binary_variables[worst_best[0]]) == 1:
                x: int = 0
            for i in range(len(performance_table_list)):
                if i != worst_best[0]:
                    position_constraints: List[LpVariable] = alternatives_variables[worst_best[0]]
                    compared_constraints: List[LpVariable] = alternatives_variables[i]

                    indices_to_keep: List[int] = worst_best[3]
                    if indices_to_keep:
                        position_constraints: List[LpVariable] = [position_constraints[i] for i in indices_to_keep]
                        compared_constraints: List[LpVariable] = [compared_constraints[i] for i in indices_to_keep]

                    problem += lpSum(position_constraints) - lpSum(compared_constraints) + big_M * alternatives_binary_variables[worst_best[0]][x][i][0] >= epsilon

                    problem += lpSum(compared_constraints) - lpSum(position_constraints) + big_M * alternatives_binary_variables[worst_best[0]][x][i][1] >= 0

                    problem += alternatives_binary_variables[worst_best[0]][x][i][0] + alternatives_binary_variables[worst_best[0]][x][i][1] <= 1

            pom_higher = []
            pom_lower = []
            for j in alternatives_binary_variables[worst_best[0]][x]:
                pom_higher.append(alternatives_binary_variables[worst_best[0]][x][j][0])
                pom_lower.append(alternatives_binary_variables[worst_best[0]][x][j][1])
            problem += lpSum(pom_higher) <= worst_best[1] - 1
            problem += lpSum(pom_lower) <= len(performance_table_list) - worst_best[2]

            # If there are more Positions than one, relevant to one alternative
            if len(alternatives_binary_variables[worst_best[0]]) > 1:
                x += 1

        # Use linear interpolation to create constraints
        for i in range(len(u_list_of_characteristic_points)):
            for j in u_list_dict[i]:
                if_characteristic = 0

                for z in range(len(u_list_of_characteristic_points[i])):
                    if u_list_dict[i][j].name == u_list_of_characteristic_points[i][z].name:
                        if_characteristic = 1
                        break

                if if_characteristic == 0:
                    point_before = 0
                    point_after = 1

                    if len(u_list_dict[i][j].name.split("_")) == 4:
                        val = -float(u_list_dict[i][j].name.split("_")[-1])
                    else:
                        val = float(u_list_dict[i][j].name.split("_")[-1])
                    while characteristic_points[i][point_before] > val or val > characteristic_points[i][point_after]:
                        point_before += 1
                        point_after += 1
                    value = SolverUtils.linear_interpolation(val, characteristic_points[i][point_before],
                                                             u_list_dict[i][
                                                                 float(characteristic_points[i][point_before])],
                                                             characteristic_points[i][point_after], u_list_dict[i][
                                                                 float(characteristic_points[i][point_after])])

                    problem += u_list_dict[i][j] == value

        # comprehensive comparisons of intensities of preference
        for intensity in comprehensive_intensities:
            left_alternative_1: List[float] = performance_table_list[intensity[0]]
            left_alternative_2: List[float] = performance_table_list[intensity[2]]
            right_alternative_1: List[float] = performance_table_list[intensity[4]]
            right_alternative_2: List[float] = performance_table_list[intensity[6]]

            left_side_1: List[LpVariable] = []
            left_side_2: List[LpVariable] = []
            right_side_1: List[LpVariable] = []
            right_side_2: List[LpVariable] = []

            indices_to_keep: List[List[int]] = [intensity[1], intensity[3], intensity[5], intensity[7]]
            print(indices_to_keep)
            if indices_to_keep[0]:
                left_alternative_1: List[float] = [left_alternative_1[i] for i in indices_to_keep[0]]
                for i in range(len(indices_to_keep[0])):
                    left_side_1.append(u_list_dict[indices_to_keep[0][i]][left_alternative_1[i]])
            else:
                for i in range(len(left_alternative_1)):
                    left_side_1.append(u_list_dict[i][left_alternative_1[i]])

            if indices_to_keep[1]:
                left_alternative_2: List[float] = [left_alternative_2[i] for i in indices_to_keep[1]]
                for i in range(len(indices_to_keep[1])):
                    left_side_2.append(u_list_dict[indices_to_keep[1][i]][left_alternative_2[i]])
            else:
                for i in range(len(left_alternative_2)):
                    left_side_2.append(u_list_dict[i][left_alternative_2[i]])

            if indices_to_keep[2]:
                right_alternative_1: List[float] = [right_alternative_1[i] for i in indices_to_keep[2]]
                for i in range(len(indices_to_keep[2])):
                    right_side_1.append(u_list_dict[indices_to_keep[2][i]][right_alternative_1[i]])
            else:
                for i in range(len(right_alternative_1)):
                    right_side_1.append(u_list_dict[i][right_alternative_1[i]])

            if indices_to_keep[3]:
                right_alternative_2: List[float] = [right_alternative_2[i] for i in indices_to_keep[3]]
                for i in range(len(indices_to_keep[3])):
                    right_side_2.append(u_list_dict[indices_to_keep[3][i]][right_alternative_2[i]])
            else:
                for i in range(len(right_alternative_2)):
                    right_side_2.append(u_list_dict[i][right_alternative_2[i]])

            if intensity[-1] == '>':
                problem += lpSum(left_side_1) - lpSum(left_side_2) >= lpSum(right_side_1) - lpSum(
                    right_side_2) + epsilon
            elif intensity[-1] == '>=':
                problem += lpSum(left_side_1) - lpSum(left_side_2) >= lpSum(right_side_1) - lpSum(right_side_2)
            else:
                problem += lpSum(left_side_1) - lpSum(left_side_2) == lpSum(right_side_1) - lpSum(right_side_2)

        problem += epsilon

        problem.solve(solver=GLPK(msg=show_logs))

        return problem

    @staticmethod
    def calculate_the_most_representative_function(
            performance_table_list: List[List[float]],
            alternatives_id_list: List[str],
            preferences: List[List[int]],
            indifferences: List[List[int]],
            criteria: List[bool],
            worst_best_position: List[List[int]],
            number_of_points: List[int],
            comprehensive_intensities: List[List[int]],
            show_logs: bool = False,
            sampler_path: str = 'files/polyrun-1.1.0-jar-with-dependencies.jar',
            number_of_samples: str = '100'
    ) -> Tuple[LpProblem, Dict[str, List[int]]]:
        """
        Main method used in getting the most representative value function.

        :param comprehensive_intensities:
        :param performance_table_list:
        :param alternatives_id_list:
        :param preferences:
        :param indifferences:
        :param criteria:
        :param worst_best_position:
        :param number_of_points:
        :param show_logs: default None
        :param sampler_path:
        :param number_of_samples:

        :return problem:
        """
        problem: LpProblem = LpProblem("UTA-GMS", LpMaximize)

        epsilon: LpVariable = LpVariable("epsilon")

        delta: LpVariable = LpVariable("delta")

        u_list, u_list_dict = SolverUtils.create_variables_list_and_dict(performance_table_list)

        characteristic_points: List[List[float]] = SolverUtils.calculate_characteristic_points(
            number_of_points, performance_table_list, u_list_dict, u_list
        )

        u_list = [sorted(lp_var_list, key=lambda var: -float(var.name.split("_")[-1]) if len(var.name.split("_")) == 4 else float(var.name.split("_")[-1])) for lp_var_list in u_list]

        u_list_of_characteristic_points: List[List[LpVariable]] = []
        for i in range(len(characteristic_points)):
            pom = []
            for j in range(len(characteristic_points[i])):
                pom.append(u_list_dict[i][float(characteristic_points[i][j])])
            u_list_of_characteristic_points.append(pom[:])

        # Normalization constraints
        the_greatest_performance: List[LpVariable] = []
        for i in range(len(u_list)):
            if criteria[i]:
                the_greatest_performance.append(u_list[i][-1])
                problem += u_list[i][0] == 0
            else:
                the_greatest_performance.append(u_list[i][0])
                problem += u_list[i][-1] == 0

        problem += lpSum(the_greatest_performance) == 1

        # Monotonicity constraint
        for i in range(len(u_list_of_characteristic_points)):
            for j in range(1, len(u_list_of_characteristic_points[i])):
                if criteria[i]:
                    problem += u_list_of_characteristic_points[i][j] >= u_list_of_characteristic_points[i][j - 1]
                else:
                    problem += u_list_of_characteristic_points[i][j - 1] >= u_list_of_characteristic_points[i][j]

        # Bounds constraint
        for i in range(len(u_list_of_characteristic_points)):
            for j in range(1, len(u_list_of_characteristic_points[i]) - 1):
                if criteria[i]:
                    problem += u_list_of_characteristic_points[i][-1] >= u_list_of_characteristic_points[i][j]
                    problem += u_list_of_characteristic_points[i][j] >= u_list_of_characteristic_points[i][0]
                else:
                    problem += u_list_of_characteristic_points[i][0] >= u_list_of_characteristic_points[i][j]
                    problem += u_list_of_characteristic_points[i][j] >= u_list_of_characteristic_points[i][-1]

        # Preference constraint
        for preference in preferences:
            left_alternative: List[float] = performance_table_list[preference[0]]
            right_alternative: List[float] = performance_table_list[preference[1]]

            indices_to_keep: List[int] = preference[2]
            if indices_to_keep:
                left_alternative: List[float] = [left_alternative[i] for i in indices_to_keep]
                right_alternative: List[float] = [right_alternative[i] for i in indices_to_keep]
                left_side: List[LpVariable] = []
                right_side: List[LpVariable] = []
                for i in range(len(indices_to_keep)):
                    left_side.append(u_list_dict[indices_to_keep[i]][left_alternative[i]])
                    right_side.append(u_list_dict[indices_to_keep[i]][right_alternative[i]])
            else:
                left_side: List[LpVariable] = []
                right_side: List[LpVariable] = []
                for i in range(len(left_alternative)):
                    left_side.append(u_list_dict[i][left_alternative[i]])
                    right_side.append(u_list_dict[i][right_alternative[i]])

            problem += lpSum(left_side) >= lpSum(right_side) + epsilon

        # Indifference constraint
        for indifference in indifferences:
            left_alternative: List[float] = performance_table_list[indifference[0]]
            right_alternative: List[float] = performance_table_list[indifference[1]]

            indices_to_keep: List[int] = indifference[2]
            if indices_to_keep:
                left_alternative: List[float] = [left_alternative[i] for i in indices_to_keep]
                right_alternative: List[float] = [right_alternative[i] for i in indices_to_keep]
                left_side: List[LpVariable] = []
                right_side: List[LpVariable] = []
                for i in range(len(indices_to_keep)):
                    left_side.append(u_list_dict[indices_to_keep[i]][left_alternative[i]])
                    right_side.append(u_list_dict[indices_to_keep[i]][right_alternative[i]])
            else:
                left_side: List[LpVariable] = []
                right_side: List[LpVariable] = []
                for i in range(len(left_alternative)):
                    left_side.append(u_list_dict[i][left_alternative[i]])
                    right_side.append(u_list_dict[i][right_alternative[i]])

            problem += lpSum(left_side) == lpSum(right_side)

        sampler_metrics: Dict[str, List[int]] = SolverUtils.get_sampler_metrics(
            problem=problem,
            performance_table_list=performance_table_list,
            alternatives_id_list=alternatives_id_list,
            sampler_path=sampler_path,
            number_of_samples=number_of_samples,
            u_list_of_characteristic_points=u_list_of_characteristic_points,
            u_list_dict=u_list_dict,
            characteristic_points=characteristic_points
        )

        # Use linear interpolation to create constraints
        for i in range(len(u_list_of_characteristic_points)):
            for j in u_list_dict[i]:
                if_characteristic = 0

                for z in range(len(u_list_of_characteristic_points[i])):
                    if u_list_dict[i][j].name == u_list_of_characteristic_points[i][z].name:
                        if_characteristic = 1
                        break

                if if_characteristic == 0:
                    point_before = 0
                    point_after = 1

                    if len(u_list_dict[i][j].name.split("_")) == 4:
                        val = -float(u_list_dict[i][j].name.split("_")[-1])
                    else:
                        val = float(u_list_dict[i][j].name.split("_")[-1])
                    while characteristic_points[i][point_before] > val or val > characteristic_points[i][point_after]:
                        point_before += 1
                        point_after += 1
                    value = SolverUtils.linear_interpolation(val, characteristic_points[i][point_before], u_list_dict[i][float(characteristic_points[i][point_before])], characteristic_points[i][point_after], u_list_dict[i][float(characteristic_points[i][point_after])])

                    problem += u_list_dict[i][j] == value

        necessary_preference: Dict[str, List[str]] = SolverUtils.get_necessary_relations(
            performance_table_list=performance_table_list,
            alternatives_id_list=alternatives_id_list,
            preferences=preferences,
            indifferences=indifferences,
            criteria=criteria,
            worst_best_position=worst_best_position,
            number_of_points=number_of_points,
            comprehensive_intensities=comprehensive_intensities
        )

        for i in range(len(alternatives_id_list) - 1):
            for j in range(i + 1, len(alternatives_id_list)):
                name_i = alternatives_id_list[i]
                name_j = alternatives_id_list[j]
                pom1 = []
                pom2 = []
                for k in range(len(performance_table_list[i])):
                    pom1.append(u_list_dict[k][float(performance_table_list[i][k])])
                    pom2.append(u_list_dict[k][float(performance_table_list[j][k])])
                sum_i = lpSum(pom1[:])
                sum_j = lpSum(pom2[:])

                if (name_i not in necessary_preference and name_j in necessary_preference and name_i in
                    necessary_preference[name_j]) or \
                        (name_i in necessary_preference and name_j in necessary_preference and name_i in
                         necessary_preference[name_j] and name_j not in necessary_preference[name_i]):
                    problem += sum_j >= sum_i + epsilon
                elif (name_j not in necessary_preference and name_i in necessary_preference and name_j in
                      necessary_preference[name_i]) or \
                        (name_i in necessary_preference and name_j in necessary_preference and name_j in
                         necessary_preference[name_i] and name_i not in necessary_preference[name_j]):
                    problem += sum_i >= sum_j + epsilon
                elif (name_i not in necessary_preference and name_j not in necessary_preference) or \
                        (name_i not in necessary_preference and name_j in necessary_preference and name_i not in
                         necessary_preference[name_j]) or \
                        (name_j not in necessary_preference and name_i in necessary_preference and name_j not in
                         necessary_preference[name_i]) or \
                        (name_i in necessary_preference and name_j not in necessary_preference[
                            name_i] and name_j in necessary_preference and name_i not in necessary_preference[name_j]):
                    problem += sum_i <= delta + sum_j
                    problem += sum_j <= delta + sum_i

        # Worst and Best position
        alternatives_variables: List[List[LpVariable]] = []
        for i in range(len(performance_table_list)):
            pom = []
            for j in range(len(u_list_dict)):
                pom.append(u_list_dict[j][performance_table_list[i][j]])
            alternatives_variables.append(pom[:])

        alternatives_binary_variables: Dict[int, List[Dict[int, LpVariable]]] = {}
        all_binary_variables = {}
        for i in worst_best_position:
            pom_dict = {}
            for j in range(len(performance_table_list)):
                pom = []
                if i[0] != j:
                    variable_1_name: str = f"v_{i[0]}_higher_than_{j}_criteria_{'_'.join(map(str, i[3]))}"
                    if variable_1_name not in all_binary_variables:
                        variable_1: LpVariable = LpVariable(variable_1_name, cat='Binary')
                        pom.append(variable_1)
                        all_binary_variables[variable_1_name] = variable_1
                    else:
                        pom.append(all_binary_variables[variable_1_name])

                    variable_2_name: str = f"v_{j}_higher_than_{i[0]}_criteria_{'_'.join(map(str, i[3]))}"
                    if variable_2_name not in all_binary_variables:
                        variable_2: LpVariable = LpVariable(variable_2_name, cat='Binary')
                        pom.append(variable_2)
                        all_binary_variables[variable_2_name] = variable_2
                    else:
                        pom.append(all_binary_variables[variable_2_name])

                    pom_dict[j] = pom[:]

            if i[0] not in alternatives_binary_variables:
                alternatives_binary_variables[i[0]] = []

            alternatives_binary_variables[i[0]].append(pom_dict)

        big_M: int = 1e20
        x: int = 0
        for worst_best in worst_best_position:
            if len(alternatives_binary_variables[worst_best[0]]) == 1:
                x: int = 0
            for i in range(len(performance_table_list)):
                if i != worst_best[0]:
                    position_constraints: List[LpVariable] = alternatives_variables[worst_best[0]]
                    compared_constraints: List[LpVariable] = alternatives_variables[i]

                    indices_to_keep: List[int] = worst_best[3]
                    if indices_to_keep:
                        position_constraints: List[LpVariable] = [position_constraints[i] for i in indices_to_keep]
                        compared_constraints: List[LpVariable] = [compared_constraints[i] for i in indices_to_keep]

                    problem += lpSum(position_constraints) - lpSum(compared_constraints) + big_M * alternatives_binary_variables[worst_best[0]][x][i][0] >= epsilon

                    problem += lpSum(compared_constraints) - lpSum(position_constraints) + big_M * alternatives_binary_variables[worst_best[0]][x][i][1] >= 0

                    problem += alternatives_binary_variables[worst_best[0]][x][i][0] + alternatives_binary_variables[worst_best[0]][x][i][1] <= 1

            pom_higher = []
            pom_lower = []
            for j in alternatives_binary_variables[worst_best[0]][x]:
                pom_higher.append(alternatives_binary_variables[worst_best[0]][x][j][0])
                pom_lower.append(alternatives_binary_variables[worst_best[0]][x][j][1])
            problem += lpSum(pom_higher) <= worst_best[1] - 1
            problem += lpSum(pom_lower) <= len(performance_table_list) - worst_best[2]

            # If there are more Positions than one, relevant to one alternative
            if len(alternatives_binary_variables[worst_best[0]]) > 1:
                x += 1

        # comprehensive comparisons of intensities of preference
        for intensity in comprehensive_intensities:
            left_alternative_1: List[float] = performance_table_list[intensity[0]]
            left_alternative_2: List[float] = performance_table_list[intensity[2]]
            right_alternative_1: List[float] = performance_table_list[intensity[4]]
            right_alternative_2: List[float] = performance_table_list[intensity[6]]

            left_side_1: List[LpVariable] = []
            left_side_2: List[LpVariable] = []
            right_side_1: List[LpVariable] = []
            right_side_2: List[LpVariable] = []

            indices_to_keep: List[List[int]] = [intensity[1], intensity[3], intensity[5], intensity[7]]
            print(indices_to_keep)
            if indices_to_keep[0]:
                left_alternative_1: List[float] = [left_alternative_1[i] for i in indices_to_keep[0]]
                for i in range(len(indices_to_keep[0])):
                    left_side_1.append(u_list_dict[indices_to_keep[0][i]][left_alternative_1[i]])
            else:
                for i in range(len(left_alternative_1)):
                    left_side_1.append(u_list_dict[i][left_alternative_1[i]])

            if indices_to_keep[1]:
                left_alternative_2: List[float] = [left_alternative_2[i] for i in indices_to_keep[1]]
                for i in range(len(indices_to_keep[1])):
                    left_side_2.append(u_list_dict[indices_to_keep[1][i]][left_alternative_2[i]])
            else:
                for i in range(len(left_alternative_2)):
                    left_side_2.append(u_list_dict[i][left_alternative_2[i]])

            if indices_to_keep[2]:
                right_alternative_1: List[float] = [right_alternative_1[i] for i in indices_to_keep[2]]
                for i in range(len(indices_to_keep[2])):
                    right_side_1.append(u_list_dict[indices_to_keep[2][i]][right_alternative_1[i]])
            else:
                for i in range(len(right_alternative_1)):
                    right_side_1.append(u_list_dict[i][right_alternative_1[i]])

            if indices_to_keep[3]:
                right_alternative_2: List[float] = [right_alternative_2[i] for i in indices_to_keep[3]]
                for i in range(len(indices_to_keep[3])):
                    right_side_2.append(u_list_dict[indices_to_keep[3][i]][right_alternative_2[i]])
            else:
                for i in range(len(right_alternative_2)):
                    right_side_2.append(u_list_dict[i][right_alternative_2[i]])

            if intensity[-1] == '>':
                problem += lpSum(left_side_1) - lpSum(left_side_2) >= lpSum(right_side_1) - lpSum(
                    right_side_2) + epsilon
            elif intensity[-1] == '>=':
                problem += lpSum(left_side_1) - lpSum(left_side_2) >= lpSum(right_side_1) - lpSum(right_side_2)
            else:
                problem += lpSum(left_side_1) - lpSum(left_side_2) == lpSum(right_side_1) - lpSum(right_side_2)

        problem += big_M * epsilon - delta

        problem.solve(solver=GLPK(msg=show_logs))

        return problem, sampler_metrics

    @staticmethod
    def get_necessary_relations(
            performance_table_list: List[List[float]],
            alternatives_id_list: List[str],
            preferences: List[List[int]],
            indifferences: List[List[int]],
            criteria: List[bool],
            worst_best_position: List[List[int]],
            number_of_points: List[int],
            comprehensive_intensities: List[List[int]],
            show_logs: bool = False
    ) -> Dict[str, List[str]]:
        """
        Method used for getting necessary relations.

        :param comprehensive_intensities:
        :param performance_table_list:
        :param alternatives_id_list:
        :param preferences:
        :param indifferences:
        :param criteria:
        :param worst_best_position:
        :param number_of_points:
        :param show_logs: default None

        :return necessary:
        """
        necessary: Dict[str, List[str]] = {}
        for i in range(len(performance_table_list)):
            for j in range(len(performance_table_list)):
                if i == j:
                    continue

                problem: LpProblem = SolverUtils.calculate_solved_problem(
                    performance_table_list=performance_table_list,
                    preferences=preferences,
                    indifferences=indifferences,
                    criteria=criteria,
                    worst_best_position=worst_best_position,
                    number_of_points=number_of_points,
                    comprehensive_intensities=comprehensive_intensities,
                    alternative_id_1=i,
                    alternative_id_2=j,
                    show_logs=show_logs
                )

                if problem.variables()[0].varValue <= 0:
                    if alternatives_id_list[i] not in necessary:
                        necessary[alternatives_id_list[i]] = []
                    necessary[alternatives_id_list[i]].append(alternatives_id_list[j])

        return necessary

    @staticmethod
    def create_variables_list_and_dict(performance_table: List[list]) -> Tuple[List[list], List[dict]]:
        """
        Method responsible for creating a technical list of variables and a technical dict of variables that are used
        for adding constraints to the problem.

        :param performance_table:

        :return u_list, u_list_dict: ex. Tuple([[u_0_0.0, u_0_2.0], [u_1_2.0, u_1_9.0]], [{26.0: u_0_26.0, 2.0: u_0_2.0}, {40.0: u_1_40.0, 2.0: u_1_2.0}])
        """
        u_list: List[List[LpVariable]] = []
        u_list_dict: List[Dict[float, LpVariable]] = []

        for i in range(len(performance_table[0])):
            row: List[LpVariable] = []
            row_dict: Dict[float, LpVariable] = {}

            for j in range(len(performance_table)):
                variable_name: str = f"u_{i}_{float(performance_table[j][i])}"
                variable: LpVariable = LpVariable(variable_name)

                if performance_table[j][i] not in row_dict:
                    row_dict[float(performance_table[j][i])] = variable

                flag: int = 1
                for var in row:
                    if str(var) == variable_name:
                        flag: int = 0
                if flag:
                    row.append(variable)

            u_list_dict.append(row_dict)

            row = sorted(row, key=lambda var: -float(var.name.split("_")[-1]) if len(var.name.split("_")) == 4 else float(var.name.split("_")[-1]))
            u_list.append(row)

        return u_list, u_list_dict

    @staticmethod
    def calculate_direct_relations(necessary: Dict[str, List[str]]) -> Dict[str, List[str]]:
        """
        Method for getting only direct relations in Hasse Diagram
        :param necessary:
        :return direct_relations:
        """
        direct_relations: Dict[str, List[str]] = {}
        # first create the relation list for each node
        for node1, relations in necessary.items():
            direct_relations[node1] = sorted(relations)
        # then prune the indirect relations
        for node1, related_nodes in list(direct_relations.items()):  # make a copy of items
            related_nodes_copy: List[str] = related_nodes.copy()
            for node2 in related_nodes:
                # Check if node2 is also related to any other node that is related to node1
                for other_node in related_nodes:
                    if other_node != node2 and other_node in direct_relations and node2 in direct_relations[other_node]:
                        # If such a relationship exists, remove the relation between node1 and node2
                        related_nodes_copy.remove(node2)
                        break
            direct_relations[node1] = sorted(related_nodes_copy)  # sort the list

        return direct_relations

    @staticmethod
    def get_alternatives_and_utilities_dict(
            variables_and_values_dict,
            performance_table_list,
            alternatives_id_list,
    ) -> Dict[str, float]:
        """
        Method for getting alternatives_and_utilities_dict

        :param variables_and_values_dict:
        :param performance_table_list:
        :param alternatives_id_list:

        :return sorted_dict:
        """

        utilities: List[float] = []
        for i in range(len(performance_table_list)):
            utility: float = 0.0
            for j in range(len(performance_table_list[i])):
                variable_name: str = f"u_{j}_{performance_table_list[i][j]}"
                if '-' in variable_name:
                    variable_name: str = variable_name.replace('-', '_')
                utility += round(variables_and_values_dict[variable_name], 4)

            utilities.append(round(utility, 4))

        utilities_dict: Dict[str, float] = {}
        # TODO: Sorting possibly unnecessary, but for now it's nicer for human eye :)
        for i in range(len(utilities)):
            utilities_dict[alternatives_id_list[i]] = utilities[i]
        sorted_dict: Dict[str, float] = dict(sorted(utilities_dict.items(), key=lambda item: item[1]))

        return sorted_dict

    @staticmethod
    def calculate_characteristic_points(
            number_of_points,
            performance_table_list,
            u_list_dict,
            u_list
    ) -> List[List[float]]:
        """
        Method for calculating characteristic points

        :param number_of_points:
        :param performance_table_list:
        :param u_list_dict:
        :param u_list:

        :return characteristic_points:
        """
        columns: List[Tuple[float]] = list(zip(*performance_table_list))
        worst_values: List[float] = [min(col) for col in columns]
        best_values: List[float] = [max(col) for col in columns]
        characteristic_points: List[List[float]] = []

        for i in range(len(worst_values)):
            pom = []
            if number_of_points[i] != 0:
                for j in range(number_of_points[i]):
                    x = worst_values[i] + (j / (number_of_points[i] - 1)) * (best_values[i] - worst_values[i])
                    if x not in u_list_dict[i]:
                        new: str = f"u_{i}_{x}"
                        variable: LpVariable = LpVariable(new)
                        new: Dict[float, LpVariable] = {x: variable}
                        u_list_dict[i].update(new)
                        u_list[i].append(variable)
                    pom.append(x)
                characteristic_points.append(pom[:])
            else:
                for j in range(len(performance_table_list)):
                    if float(performance_table_list[j][i]) not in pom:
                        pom.append(float(performance_table_list[j][i]))
                pom.sort()
                characteristic_points.append(pom[:])
        return characteristic_points

    @staticmethod
    def linear_interpolation(x, x1, y1, x2, y2) -> float:
        """Perform linear interpolation to estimate a value at a specific point on a straight line"""
        result = y1 + ((x - x1) * (y2 - y1)) / (x2 - x1)
        return result

    @staticmethod
    def get_criterion_functions(
            variables_and_values_dict,
            criteria
    ) -> Dict[str, List[Tuple[float, float]]]:
        """
        Method responsible for getting criterion functions

        :param variables_and_values_dict:
        :param criteria:
        :return:
        """
        criterion_functions: Dict[str, List[Tuple[float, float]]] = defaultdict(list)

        criterion_ids: List[str] = []
        for crit in criteria:
            criterion_ids.append(crit.criterion_id)

        for key, value in variables_and_values_dict.items():
            if key.startswith('u'):
                first_part, x_value = key.rsplit('_', 1)
                if first_part.endswith('_'):
                    _, i, __ = first_part.rsplit('_', 2)
                else:
                    _, i = first_part.rsplit('_', 1)

                criterion_functions[criterion_ids[int(i)]].append((float(x_value), value))

        for key, values in criterion_functions.items():
            criterion_functions[key] = sorted(values, key=lambda x: x[0])

        return dict(criterion_functions)

    @staticmethod
    def get_sampler_metrics(
            problem,
            performance_table_list,
            alternatives_id_list,
            sampler_path,
            number_of_samples,
            u_list_of_characteristic_points,
            u_list_dict,
            characteristic_points
    ) -> Dict[str, List[int]]:
        # Write input file for Sampler
        with TemporaryFile("w+") as input_file, TemporaryFile("w+") as output_file:
            # Write header, useful only for testing
            variable_names = [var.name for var in problem.variables()]

            for constraint in problem.constraints.values():
                constraint_values = []
                for var in problem.variables():
                    if var in constraint:
                        constraint_values.append(str(constraint[var]))
                    else:
                        constraint_values.append("0")
                constraint_values.append(re.search(r'([<>=]=?)', str(constraint)).group(1))
                constraint_values.append(str(-constraint.constant))
                input_file.write(" ".join(constraint_values) + "\n")

            input_file.seek(0)
            # Write Sampler output file
            subprocess.call(
                ['java', '-jar', sampler_path, '-n', number_of_samples],
                stdin=input_file,
                stdout=output_file
            )

            output: Dict[str, List[float]] = {}
            for alternative in alternatives_id_list:
                output[alternative] = [0] * len(alternatives_id_list)

            output_file.seek(0)
            for line in output_file:
                variables_and_values_dict: Dict[str, float] = {}

                if 'epsilon' in variable_names:
                    var_names = variable_names[1:]
                    values = line.strip().split('\t')[1:]
                else:
                    var_names = variable_names
                    values = line.strip().split('\t')

                for var_name, var_value in zip(var_names, values):
                    variables_and_values_dict[var_name] = float(var_value)

                # need to add interpolation here to variables_and_values_dict
                # Use linear interpolation to create constraints
                for i in range(len(u_list_of_characteristic_points)):
                    for j in u_list_dict[i]:
                        if_characteristic = 0

                        for z in range(len(u_list_of_characteristic_points[i])):
                            if u_list_dict[i][j].name == u_list_of_characteristic_points[i][z].name:
                                if_characteristic = 1
                                break

                        if if_characteristic == 0:
                            point_before = 0
                            point_after = 1

                            if len(u_list_dict[i][j].name.split("_")) == 4:
                                val = -float(u_list_dict[i][j].name.split("_")[-1])
                            else:
                                val = float(u_list_dict[i][j].name.split("_")[-1])
                            while characteristic_points[i][point_before] > val or val > characteristic_points[i][point_after]:
                                point_before += 1
                                point_after += 1
                            value = SolverUtils.linear_interpolation(val, characteristic_points[i][point_before], u_list_dict[i][float(characteristic_points[i][point_before])], characteristic_points[i][point_after], u_list_dict[i][float(characteristic_points[i][point_after])])

                            result: float  = sum(coef * variables_and_values_dict[var.name] for var, coef in value.items())
                            variable_name: str = str(u_list_dict[i][j])
                            variables_and_values_dict[variable_name] = result

                alternatives_and_utilities_dict: Dict[str, float] = SolverUtils.get_alternatives_and_utilities_dict(
                    variables_and_values_dict=variables_and_values_dict,
                    performance_table_list=performance_table_list,
                    alternatives_id_list=alternatives_id_list,
                )

                letter_value_pairs = [(letter, value) for letter, value in alternatives_and_utilities_dict.items()]

                letter_value_pairs.sort(key=lambda x: x[1], reverse=True)

                single_ranking = {}
                place = 1
                for i in range(len(letter_value_pairs)):
                    letter, value = letter_value_pairs[i]

                    # Check if the current value is the same as the previous value
                    if i > 0 and value == letter_value_pairs[i - 1][1]:
                        single_ranking[letter] = single_ranking[letter_value_pairs[i - 1][0]]
                    else:
                        single_ranking[letter] = place

                    place += 1

                for key, value in single_ranking.items():
                    output[key][value-1] = output[key][value-1] + 1

            for key, value in output.items():
                try:
                    output[key] = [round(val / sum(output[key]) * 100, 10) for val in value]
                except:
                    output[key] = []

            return output

    @staticmethod
    def resolve_incosistency(
            performance_table_list: List[List[float]],
            preferences: List[List[int]],
            indifferences: List[List[int]],
            criteria: List[bool],
            worst_best_position: List[List[int]],
            number_of_points: List[int],
            comprehensive_intensities: List[List[int]],
            subsets_to_remove: List[List[List[List[int]]]],
            show_logs: bool = False,
    ):
        """
        Main calculation method for problem-solving.
        The idea is that this should be a generic method used across different problems

        :param subsets_to_remove:
        :param performance_table_list:
        :param preferences:
        :param indifferences:
        :param criteria:
        :param worst_best_position:
        :param number_of_points:
        :param comprehensive_intensities:
        :param alternative_id_1: used only in calculation for hasse graphs
        :param alternative_id_2: used only in calculation for hasse graphs
        :param show_logs: default None

        :return problem:
        """
        problem: LpProblem = LpProblem("UTA-GMS", LpMinimize)

        epsilon: LpVariable = LpVariable("epsilon")

        u_list, u_list_dict = SolverUtils.create_variables_list_and_dict(performance_table_list)

        characteristic_points: List[List[float]] = SolverUtils.calculate_characteristic_points(
            number_of_points, performance_table_list, u_list_dict, u_list
        )

        u_list = [sorted(lp_var_list,
                         key=lambda var: -float(var.name.split("_")[-1]) if len(var.name.split("_")) == 4 else float(
                             var.name.split("_")[-1])) for lp_var_list in u_list]

        u_list_of_characteristic_points: List[List[LpVariable]] = []
        for i in range(len(characteristic_points)):
            pom = []
            for j in range(len(characteristic_points[i])):
                pom.append(u_list_dict[i][float(characteristic_points[i][j])])
            u_list_of_characteristic_points.append(pom[:])

        problem += epsilon == 0.0001

        # Normalization constraints
        the_greatest_performance: List[LpVariable] = []

        for i in range(len(u_list)):

            if criteria[i]:
                the_greatest_performance.append(u_list[i][-1])
                problem += u_list[i][0] == 0
            else:
                the_greatest_performance.append(u_list[i][0])
                problem += u_list[i][-1] == 0

        problem += lpSum(the_greatest_performance) == 1

        # Monotonicity constraint
        for i in range(len(u_list_of_characteristic_points)):
            for j in range(1, len(u_list_of_characteristic_points[i])):
                if criteria[i]:
                    problem += u_list_of_characteristic_points[i][j] >= u_list_of_characteristic_points[i][j - 1]
                else:
                    problem += u_list_of_characteristic_points[i][j - 1] >= u_list_of_characteristic_points[i][j]

        # Bounds constraint
        for i in range(len(u_list_of_characteristic_points)):
            for j in range(1, len(u_list_of_characteristic_points[i]) - 1):
                if criteria[i]:
                    problem += u_list_of_characteristic_points[i][-1] >= u_list_of_characteristic_points[i][j]
                    problem += u_list_of_characteristic_points[i][j] >= u_list_of_characteristic_points[i][0]
                else:
                    problem += u_list_of_characteristic_points[i][0] >= u_list_of_characteristic_points[i][j]
                    problem += u_list_of_characteristic_points[i][j] >= u_list_of_characteristic_points[i][-1]

        binary_variables_inconsistency_dict = {}
        binary_variables_inconsistency_list_worst_best = []
        # Worst and Best position
        alternatives_variables: List[List[LpVariable]] = []
        for i in range(len(performance_table_list)):
            pom = []
            for j in range(len(u_list_dict)):
                pom.append(u_list_dict[j][performance_table_list[i][j]])
            alternatives_variables.append(pom[:])

        alternatives_binary_variables: Dict[int, List[Dict[int, LpVariable]]] = {}
        all_binary_variables = {}
        for i in worst_best_position:
            pom_dict = {}
            for j in range(len(performance_table_list)):
                pom = []
                if i[0] != j:
                    variable_1_name: str = f"v_{i[0]}_higher_than_{j}_criteria_{'_'.join(map(str, i[3]))}"
                    if variable_1_name not in all_binary_variables:
                        variable_1: LpVariable = LpVariable(variable_1_name, cat='Binary')
                        pom.append(variable_1)
                        all_binary_variables[variable_1_name] = variable_1
                    else:
                        pom.append(all_binary_variables[variable_1_name])

                    variable_2_name: str = f"v_{j}_higher_than_{i[0]}_criteria_{'_'.join(map(str, i[3]))}"
                    if variable_2_name not in all_binary_variables:
                        variable_2: LpVariable = LpVariable(variable_2_name, cat='Binary')
                        pom.append(variable_2)
                        all_binary_variables[variable_2_name] = variable_2
                    else:
                        pom.append(all_binary_variables[variable_2_name])

                    pom_dict[j] = pom[:]

            if i[0] not in alternatives_binary_variables:
                alternatives_binary_variables[i[0]] = []

            alternatives_binary_variables[i[0]].append(pom_dict)

        big_M: float = 1e20
        x: int = 0
        for worst_best in worst_best_position:
            if len(alternatives_binary_variables[worst_best[0]]) == 1:
                x: int = 0
            for i in range(len(performance_table_list)):
                if i != worst_best[0]:

                    position_constraints: List[LpVariable] = alternatives_variables[worst_best[0]]
                    compared_constraints: List[LpVariable] = alternatives_variables[i]

                    indices_to_keep: List[int] = worst_best[3]
                    if indices_to_keep:
                        position_constraints: List[LpVariable] = [position_constraints[i] for i in indices_to_keep]
                        compared_constraints: List[LpVariable] = [compared_constraints[i] for i in indices_to_keep]

                    variable: str = f"vwb_{worst_best[0]}_{worst_best[1]}_{worst_best[2]}_criteria_{'_'.join(map(str, worst_best[3]))}"
                    if variable not in binary_variables_inconsistency_dict:
                        variable_1: LpVariable = LpVariable(variable, cat='Binary')
                        binary_variables_inconsistency_dict[variable] = variable_1
                        binary_variables_inconsistency_list_worst_best.append(variable_1)

                    problem += lpSum(position_constraints) - lpSum(compared_constraints) + variable_1 * big_M + big_M * \
                               alternatives_binary_variables[worst_best[0]][x][i][0] >= epsilon

                    problem += lpSum(compared_constraints) - lpSum(position_constraints) + variable_1 * big_M + big_M * \
                               alternatives_binary_variables[worst_best[0]][x][i][1] >= 0

                    problem += alternatives_binary_variables[worst_best[0]][x][i][0] + \
                               alternatives_binary_variables[worst_best[0]][x][i][1] <= 1 + variable_1 * big_M

            pom_higher = []
            pom_lower = []
            for j in alternatives_binary_variables[worst_best[0]][x]:
                pom_higher.append(alternatives_binary_variables[worst_best[0]][x][j][0])
                pom_lower.append(alternatives_binary_variables[worst_best[0]][x][j][1])
            problem += lpSum(pom_higher) <= worst_best[1] - 1 + big_M * variable_1
            problem += lpSum(pom_lower) <= len(performance_table_list) - worst_best[2] + big_M * variable_1

            # If there are more Positions than one, relevant to one alternative
            if len(alternatives_binary_variables[worst_best[0]]) > 1:
                x += 1

        binary_variables_inconsistency_list_preferences = []
        # Preference constraint
        for preference in preferences:
            left_alternative: List[float] = performance_table_list[preference[0]]
            right_alternative: List[float] = performance_table_list[preference[1]]

            indices_to_keep: List[int] = preference[2]
            if indices_to_keep:
                left_alternative: List[float] = [left_alternative[i] for i in indices_to_keep]
                right_alternative: List[float] = [right_alternative[i] for i in indices_to_keep]
                left_side: List[LpVariable] = []
                right_side: List[LpVariable] = []
                for i in range(len(indices_to_keep)):
                    left_side.append(u_list_dict[indices_to_keep[i]][left_alternative[i]])
                    right_side.append(u_list_dict[indices_to_keep[i]][right_alternative[i]])
            else:
                left_side: List[LpVariable] = []
                right_side: List[LpVariable] = []
                for i in range(len(left_alternative)):
                    left_side.append(u_list_dict[i][left_alternative[i]])
                    right_side.append(u_list_dict[i][right_alternative[i]])

            variable: str = f"vp_{preference[0]}_{preference[1]}_criteria_{'_'.join(map(str, preference[2]))}"
            if variable not in binary_variables_inconsistency_dict:
                variable_1: LpVariable = LpVariable(variable, cat='Binary')
                binary_variables_inconsistency_dict[variable] = variable_1
                binary_variables_inconsistency_list_preferences.append(variable_1)

            if preference[0] == preference[1]:
                problem += lpSum(left_side) >= lpSum(right_side) + epsilon - big_M * variable_1
                problem += variable_1 == 1
            else:
                problem += lpSum(left_side) >= lpSum(right_side) + epsilon - big_M * variable_1

        binary_variables_inconsistency_list_indifferences = []
        # Indifference constraint
        for indifference in indifferences:
            left_alternative: List[float] = performance_table_list[indifference[0]]
            right_alternative: List[float] = performance_table_list[indifference[1]]

            indices_to_keep: List[int] = indifference[2]
            if indices_to_keep:
                left_alternative: List[float] = [left_alternative[i] for i in indices_to_keep]
                right_alternative: List[float] = [right_alternative[i] for i in indices_to_keep]
                left_side: List[LpVariable] = []
                right_side: List[LpVariable] = []
                for i in range(len(indices_to_keep)):
                    left_side.append(u_list_dict[indices_to_keep[i]][left_alternative[i]])
                    right_side.append(u_list_dict[indices_to_keep[i]][right_alternative[i]])
            else:
                left_side: List[LpVariable] = []
                right_side: List[LpVariable] = []
                for i in range(len(left_alternative)):
                    left_side.append(u_list_dict[i][left_alternative[i]])
                    right_side.append(u_list_dict[i][right_alternative[i]])

            variable: str = f"vi_{indifference[0]}_{indifference[1]}_criteria_{'_'.join(map(str, indifference[2]))}"
            if variable not in binary_variables_inconsistency_dict:
                variable_1: LpVariable = LpVariable(variable, cat='Binary')
                binary_variables_inconsistency_dict[variable] = variable_1
                binary_variables_inconsistency_list_indifferences.append(variable_1)

            problem += lpSum(left_side) + big_M * variable_1 >= lpSum(right_side)
            problem += lpSum(right_side) + big_M * variable_1 >= lpSum(left_side)

        binary_variables_inconsistency_list_comprehensive_intensities = []
        # comprehensive comparisons of intensities of preference
        for intensity in comprehensive_intensities:
            left_alternative_1: List[float] = performance_table_list[intensity[0]]
            left_alternative_2: List[float] = performance_table_list[intensity[2]]
            right_alternative_1: List[float] = performance_table_list[intensity[4]]
            right_alternative_2: List[float] = performance_table_list[intensity[6]]

            left_side_1: List[LpVariable] = []
            left_side_2: List[LpVariable] = []
            right_side_1: List[LpVariable] = []
            right_side_2: List[LpVariable] = []

            indices_to_keep: List[List[int]] = [intensity[1], intensity[3], intensity[5], intensity[7]]

            if indices_to_keep[0]:
                left_alternative_1: List[float] = [left_alternative_1[i] for i in indices_to_keep[0]]
                for i in range(len(indices_to_keep[0])):
                    left_side_1.append(u_list_dict[indices_to_keep[0][i]][left_alternative_1[i]])
            else:
                for i in range(len(left_alternative_1)):
                    left_side_1.append(u_list_dict[i][left_alternative_1[i]])

            if indices_to_keep[1]:
                left_alternative_2: List[float] = [left_alternative_2[i] for i in indices_to_keep[1]]
                for i in range(len(indices_to_keep[1])):
                    left_side_2.append(u_list_dict[indices_to_keep[1][i]][left_alternative_2[i]])
            else:
                for i in range(len(left_alternative_2)):
                    left_side_2.append(u_list_dict[i][left_alternative_2[i]])

            if indices_to_keep[2]:
                right_alternative_1: List[float] = [right_alternative_1[i] for i in indices_to_keep[2]]
                for i in range(len(indices_to_keep[2])):
                    right_side_1.append(u_list_dict[indices_to_keep[2][i]][right_alternative_1[i]])
            else:
                for i in range(len(right_alternative_1)):
                    right_side_1.append(u_list_dict[i][right_alternative_1[i]])

            if indices_to_keep[3]:
                right_alternative_2: List[float] = [right_alternative_2[i] for i in indices_to_keep[3]]
                for i in range(len(indices_to_keep[3])):
                    right_side_2.append(u_list_dict[indices_to_keep[3][i]][right_alternative_2[i]])
            else:
                for i in range(len(right_alternative_2)):
                    right_side_2.append(u_list_dict[i][right_alternative_2[i]])

            if intensity[8] == '=':
                relation = 'e'
            elif intensity[8] == '>':
                relation = 'g'
            elif intensity[8] == '>=':
                relation = 'ge'

            variable: str = f"vci_{intensity[0]}_{intensity[2]}_{intensity[4]}_{intensity[6]}_{relation}_c_{'_'.join(map(str, intensity[1]))}_c_{'_'.join(map(str, intensity[3]))}_c_{'_'.join(map(str, intensity[5]))}_c_{'_'.join(map(str, intensity[7]))}"
            if variable not in binary_variables_inconsistency_dict:
                variable_1: LpVariable = LpVariable(variable, cat='Binary')
                binary_variables_inconsistency_dict[variable] = variable_1
                binary_variables_inconsistency_list_comprehensive_intensities.append(variable_1)

            if intensity[-1] == '>':
                if (intensity[0] == intensity[2] and intensity[1] == intensity[3] and intensity[4] == intensity[6] and
                    intensity[5] == intensity[7]) or (
                        intensity[0] == intensity[4] and intensity[1] == intensity[5] and intensity[2] == intensity[
                    6] and intensity[3] == intensity[7]):
                    problem += lpSum(left_side_1) - lpSum(left_side_2) >= lpSum(right_side_1) - lpSum(
                        right_side_2) + epsilon - big_M * variable_1
                    problem += variable_1 == 1
                else:
                    problem += lpSum(left_side_1) - lpSum(left_side_2) >= lpSum(right_side_1) - lpSum(
                        right_side_2) + epsilon - big_M * variable_1
            elif intensity[-1] == '>=':
                problem += lpSum(left_side_1) - lpSum(left_side_2) + big_M * variable_1 >= lpSum(right_side_1) - lpSum(
                    right_side_2)
            else:
                problem += lpSum(left_side_1) - lpSum(left_side_2) + big_M * variable_1 >= lpSum(right_side_1) - lpSum(
                    right_side_2)
                problem += lpSum(left_side_1) - lpSum(left_side_2) <= lpSum(right_side_1) - lpSum(
                    right_side_2) + big_M * variable_1

        # Use linear interpolation to create constraints
        for i in range(len(u_list_of_characteristic_points)):
            for j in u_list_dict[i]:
                if_characteristic = 0

                for z in range(len(u_list_of_characteristic_points[i])):
                    if u_list_dict[i][j].name == u_list_of_characteristic_points[i][z].name:
                        if_characteristic = 1
                        break

                if if_characteristic == 0:
                    point_before = 0
                    point_after = 1

                    if len(u_list_dict[i][j].name.split("_")) == 4:
                        val = -float(u_list_dict[i][j].name.split("_")[-1])
                    else:
                        val = float(u_list_dict[i][j].name.split("_")[-1])
                    while characteristic_points[i][point_before] > val or val > characteristic_points[i][point_after]:
                        point_before += 1
                        point_after += 1
                    value = SolverUtils.linear_interpolation(val, characteristic_points[i][point_before],
                                                             u_list_dict[i][
                                                                 float(characteristic_points[i][point_before])],
                                                             characteristic_points[i][point_after], u_list_dict[i][
                                                                 float(characteristic_points[i][point_after])])

                    problem += u_list_dict[i][j] == value

        if subsets_to_remove != []:
            for i in range(len(subsets_to_remove)):
                pom = []
                for j in range(len(subsets_to_remove[i])):
                    for k in range(len(subsets_to_remove[i][j])):
                        if j == 0:
                            variable: str = f"vp_{subsets_to_remove[i][j][k][0]}_{subsets_to_remove[i][j][k][1]}_criteria_{'_'.join(map(str, subsets_to_remove[i][j][k][2]))}"
                            pom.append(binary_variables_inconsistency_dict[variable])
                        elif j == 1:
                            variable: str = f"vi_{subsets_to_remove[i][j][k][0]}_{subsets_to_remove[i][j][k][1]}_criteria_{'_'.join(map(str, subsets_to_remove[i][j][k][2]))}"
                            pom.append(binary_variables_inconsistency_dict[variable])
                        elif j == 2:
                            variable: str = f"vwb_{subsets_to_remove[i][j][k][0]}_{subsets_to_remove[i][j][k][1]}_{subsets_to_remove[i][j][k][2]}_criteria_{'_'.join(map(str, subsets_to_remove[i][j][k][3]))}"
                            pom.append(binary_variables_inconsistency_dict[variable])
                        elif j == 3:

                            if subsets_to_remove[i][j][k][8] == '=':
                                relation = 'e'
                            elif subsets_to_remove[i][j][k][8] == '>':
                                relation = 'g'
                            elif subsets_to_remove[i][j][k][8] == '>=':
                                relation = 'ge'

                            variable: str = f"vci_{subsets_to_remove[i][j][k][0]}_{subsets_to_remove[i][j][k][2]}_{subsets_to_remove[i][j][k][4]}_{subsets_to_remove[i][j][k][6]}_{relation}_c_{'_'.join(map(str, subsets_to_remove[i][j][k][1]))}_c_{'_'.join(map(str, subsets_to_remove[i][j][k][3]))}_c_{'_'.join(map(str, subsets_to_remove[i][j][k][5]))}_c_{'_'.join(map(str, subsets_to_remove[i][j][k][7]))}"
                            pom.append(binary_variables_inconsistency_dict[variable])

                problem += lpSum(pom[:]) <= len(subsets_to_remove[i][0]) + len(subsets_to_remove[i][1]) + len(
                    subsets_to_remove[i][2]) + len(subsets_to_remove[i][3]) - 1

        v = lpSum(binary_variables_inconsistency_list_preferences) + lpSum(
            binary_variables_inconsistency_list_indifferences) + lpSum(
            binary_variables_inconsistency_list_worst_best) + lpSum(
            binary_variables_inconsistency_list_comprehensive_intensities)
        problem += v

        problem.solve(solver=GLPK(msg=show_logs))

        result = []
        resultp = []
        resulti = []
        resultwb = []
        resultci = []
        for i in problem.variables():
            pom = []
            name = i.name
            numbers_in_string = name.split("_")
            if i.name[0] == "v" and i.name[1] == "i" and i.varValue == 1:
                criterion = []
                for j in range(1, len(numbers_in_string)):
                    if j == 3:
                        continue
                    elif j > 2:
                        if numbers_in_string[j] == "":
                            continue
                        else:
                            criterion.append(int(numbers_in_string[j]))
                    else:
                        pom.append(int(numbers_in_string[j]))
                pom.append(criterion[:])
                resulti.append(pom[:])
            elif i.name[0] == "v" and i.name[1] == "p" and i.name[2] != 'i' and i.varValue == 1:
                criterion = []
                for j in range(1, len(numbers_in_string)):
                    if j == 3:
                        continue
                    elif j > 2:
                        if numbers_in_string[j] == "":
                            continue
                        else:
                            criterion.append(int(numbers_in_string[j]))
                    else:
                        pom.append(int(numbers_in_string[j]))
                pom.append(criterion[:])
                resultp.append(pom[:])
            elif i.name[0] == "v" and i.name[1] == "w" and i.name[2] == "b" and i.varValue == 1:
                criterion = []
                for j in range(1, len(numbers_in_string)):
                    if j == 4:
                        continue
                    elif j > 4:
                        if numbers_in_string[j] == "":
                            continue
                        else:
                            criterion.append(int(numbers_in_string[j]))
                    else:
                        pom.append(int(numbers_in_string[j]))
                pom.append(criterion[:])
                resultwb.append(pom[:])
            elif i.name[0] == "v" and i.name[1] == "c" and i.name[2] == "i" and i.varValue == 1:
                criterion = []
                for x in range(1, 5):
                    pom.append(int(numbers_in_string[x]))
                if numbers_in_string[5] == 'e':
                    relation = '='
                elif numbers_in_string[5] == 'g':
                    relation = '>'
                elif numbers_in_string[5] == 'ge':
                    relation = '>='
                pom.append(relation)
                x = 7
                pom_criteria = []
                for y in range(4):
                    while numbers_in_string[x] != "c" and numbers_in_string[x] != "":
                        pom_criteria.append(int(numbers_in_string[x]))
                        x = x + 1

                        if x >= len(numbers_in_string):
                            break
                    criterion.append(pom_criteria[:])
                    x = x + 1

                    pom_criteria = []

                pom_final = []
                for x in range(5):
                    if x == 4:
                        pom_final.append(pom[x])
                    else:
                        pom_final.append(pom[x])
                        pom_final.append(criterion[x])
                resultci.append(pom_final[:])

        result.append(resultp)
        result.append(resulti)
        result.append(resultwb)
        result.append(resultci)
        subsets_to_remove.append(result)

        if subsets_to_remove[-1][0] == [] and subsets_to_remove[-1][1] == [] and subsets_to_remove[-1][2] == [] and \
                subsets_to_remove[-1][3] == []:
            return subsets_to_remove
        else:
            return SolverUtils.resolve_incosistency(
                performance_table_list,
                preferences,
                indifferences,
                criteria,
                worst_best_position,
                number_of_points,
                comprehensive_intensities,
                subsets_to_remove
            )
