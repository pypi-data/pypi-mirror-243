from pprint import pprint

from yandex_parser import YandexParser
from yandex_parser.tests.test_yandex import BaseYandexParserTest

parser = YandexParser(BaseYandexParserTest().get_data('case24--different-unicode-char-in-advertisment-parser-data.html'))
pprint(parser.get_serp())
