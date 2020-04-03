from pathlib import Path

import pytest
from bs4 import BeautifulSoup
from web_scraper.parser_article import ArticleParser


@pytest.fixture(autouse=True)
def article_parser():
    with open(Path(__file__).parent / 'test_article.html', 'r') as f:
        soup = BeautifulSoup(f.read(), features='html5lib')
    parser = ArticleParser('name_article', 'url_article', soup)
    yield parser


def test_init_article_parser(article_parser):
    assert article_parser.article_url == 'url_article'
    assert article_parser.article_name == 'name_article'


def test_find_text_and_images(article_parser):
    actual_text, actual_images = article_parser.find_text_and_images()
    assert actual_text is not None
    assert actual_images is not None
