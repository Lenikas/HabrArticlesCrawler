import os
from pathlib import Path

import pytest
from bs4 import BeautifulSoup
from web_scraper.parser_page import PageParser
from web_scraper.start import prepare_articles, start_scraper


@pytest.fixture()
def page_parser():
    with open(Path(__file__).parent / 'test_page.html', 'r') as f:
        soup = BeautifulSoup(f.read(), features='html5lib')
    parser = PageParser('url', soup)
    yield parser


@pytest.mark.parametrize('needed_count', (5, 25))
def test_prepare_articles(page_parser, needed_count):
    actual = prepare_articles(page_parser.find_articles(), needed_count, page_parser)
    if needed_count == 5:
        assert len(actual) == needed_count
    else:
        assert len(actual) == needed_count


def test_worker():
    #   как мне протестировать это добро,чтобы удостовериться,что все работает нормально,
    #   но при этом не скачивать все картинки в тесте?
    #   проблема еще и в том,что я не могу потом удалить директорию,появившуюся после вызова этого метода, потому что я
    #   не знаю, какую именно статью он скачает. Это проблемы архитектуры проекта?
    start_scraper('https://habr.com', 1, 1)
    assert os.path.isfile('1000 most common words.txt') is True
    os.remove('1000 most common words.txt')
    # shutil.rmtree('/folder_name')


def test_error_worker():
    with pytest.raises(ValueError):
        start_scraper('https://habr.com', -1, -1)
