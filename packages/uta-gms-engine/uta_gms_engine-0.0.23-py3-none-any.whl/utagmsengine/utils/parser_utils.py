from xmcda.XMCDA import XMCDA
import _io

import os


class ParserUtils:

    @staticmethod
    def load_xmcda(file: _io.TextIOWrapper) -> XMCDA:
        """
        Private method responsible for loading XMCDA files from python file objects.

        :param file: XMCDA file

        :return: XMCDA
        """
        xmcda: XMCDA = XMCDA()
        xmcda_file: XMCDA = xmcda.load(file)
        return xmcda_file


