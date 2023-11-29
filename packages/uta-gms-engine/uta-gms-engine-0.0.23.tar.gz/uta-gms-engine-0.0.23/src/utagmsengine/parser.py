from xmcda.criteria import Criteria
from xmcda.XMCDA import XMCDA
import csv
import _io
from typing import List, Dict

from .utils.parser_utils import ParserUtils
from .dataclasses import Criterion


class Parser:
    @staticmethod
    def get_performance_table_dict_csv(csvfile: _io.TextIOWrapper) -> Dict[str, Dict[str, float]]:
        """
        Method responsible for getting dict of performances from CSV file

        :param csvfile: python file object of csv file

        :return: Dictionary of performances
        """
        csv_reader = csv.reader(csvfile, delimiter=';')
        gains: List[str] = next(csv_reader)[1:]  # skip gains row
        criteria_ids: List[str] = next(csv_reader)[1:]

        performance_table_list: List[List[float]] = []
        alternative_ids: List[str] = []
        for row in csv_reader:
            performance_list: List[float] = [float(value) for value in row[1:]]
            alternative_id: str = [value for value in row[:1]][0]

            performance_table_list.append(performance_list)
            alternative_ids.append(alternative_id)

        result = {}
        for i in range(len(alternative_ids)):
            result[alternative_ids[i]] = {criteria_ids[j]: performance_table_list[i][j] for j in range(len(criteria_ids))}

        return result

    @staticmethod
    def get_criterion_list_csv(csvfile: _io.TextIOWrapper) -> List[Criterion]:
        """
        Method responsible for getting list of criteria

        :param csvfile: Content of file

        :return: List of criteria ex. ['g1', 'g2', 'g3']
        """
        csv_reader = csv.reader(csvfile, delimiter=';')

        gains: List[str] = next(csv_reader)[1:]
        criteria_ids: List[str] = next(csv_reader)[1:]

        criteria_objects = []
        for i in range(len(criteria_ids)):
            gain = True if gains[i].lower() == 'gain' else False
            criteria_objects.append(Criterion(criterion_id=criteria_ids[i], gain=gain, number_of_linear_segments=0))

        return criteria_objects

    @staticmethod
    def get_performance_table_dict_xmcda(xmcda_file: _io.TextIOWrapper) -> Dict[str, Dict[str, float]]:
        """
        Method responsible for getting dictionary representing performance table

        :param xmcda_file: XMCDA file

        :return: Dictionary representing performance table
            ex. {'id1': {'g1': 31.6, 'g2': 6.6, 'c3': 7.2}, 'id2': {'g1': 1.5, 'g2': 14.2, 'c3': 10.0}
        """
        xmcda_data = ParserUtils.load_xmcda(xmcda_file)
        performance_table_dict = {}
        for alternative in xmcda_data.alternatives:
            performance_list = {}
            for criterion in xmcda_data.criteria:
                performance_list[criterion.id] = xmcda_data.performance_tables[0][alternative][criterion]
            performance_table_dict[alternative.id] = performance_list

        return performance_table_dict

    @staticmethod
    def get_alternative_dict_xmcda(xmcda_file: _io.TextIOWrapper) -> Dict[str, str]:
        """
        Method responsible for getting dictionary of alternative

        :param xmcda_file: XMCDA file

        :return: Dictionary of alternatives ex. {'id1': 'Alternative1', 'id2': 'Alternative2', 'id3': 'Alternative3'}
        """
        xmcda_data = ParserUtils.load_xmcda(xmcda_file)
        alternatives = {}
        for alternative in xmcda_data.alternatives:
            alternatives[alternative.id] = alternative.name

        return alternatives

    @staticmethod
    def get_criterion_dict_xmcda(xmcda_file: _io.TextIOWrapper) -> Dict[str, Criterion]:
        """
        Method responsible for getting dictionary of criteria

        :param xmcda_file: XMCDA file

        :return: Dictionary of Criterion objects ex. ['id1': Criterion1,'id2': Criterion2,'id3': Criterion3]
        """
        xmcda_data = ParserUtils.load_xmcda(xmcda_file)
        criterion_dict = {}
        for criterion in xmcda_data.criteria:
            criterion_dict[criterion.id] = Criterion(criterion_id=criterion.name,
                                                     gain=(1 if criterion.id[0] == 'g' else 0),
                                                     number_of_linear_segments=0)

        return criterion_dict
