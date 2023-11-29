from xmcda.XMCDA import XMCDA
from src.utagmsengine.utils.parser_utils import ParserUtils
import _io


def test_load_file():
    with open('tests/files/performance_table.xml', 'rb') as xml_file:
        xml_file_text = _io.TextIOWrapper(xml_file, encoding='utf-8')
        xmcda: XMCDA = ParserUtils.load_xmcda(xml_file_text)

        assert xmcda.alternatives[0].id == 'A'
        assert xmcda.alternatives[5].id == 'F'
        assert xmcda.criteria[0].id == 'g1'
