from pathlib import Path

import pytest
from bs4 import BeautifulSoup
from web_scraper.parser_page import PageParser


@pytest.fixture(autouse=True)
def page_parser():
    with open(Path(__file__).parent / 'test_page.html', 'r') as f:
        soup = BeautifulSoup(f.read(), features='html5lib')
    parser = PageParser('url', soup)
    yield parser


def test_init_page_parser(page_parser):
    assert page_parser.page == 'url'
    assert page_parser.soup is not None


def test_find_articles(page_parser):
    actual = page_parser.find_articles()
    assert len(page_parser.articles) == len(actual)
    assert len(actual) == 20


def test_find_next_button(page_parser):
    actual = page_parser.find_next_button()
    assert actual is not None
    assert 'page2' in actual
