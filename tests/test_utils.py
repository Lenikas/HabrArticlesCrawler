import os

import pytest
from bs4 import BeautifulSoup
from web_scraper.utils import (
    create_count_words_file,
    do_request,
    extract_words,
    make_dir_with_article,
    validate_arguments,
)


def test_do_request_bad():
    with pytest.raises(ConnectionError):
        do_request('https://bad_link')


def test_do_request():
    actual = do_request('https://habr.com/')
    assert actual is not None
    assert isinstance(actual, BeautifulSoup)


def test_validate_arguments():
    assert validate_arguments(1, 1) is True
    assert validate_arguments(-1, -1) is False


def test_calculate_words():
    text = 'Привет, как дела?'
    actual = extract_words(text)
    assert len(actual) == 2
    assert actual[1] == 'дела'


def test_create_count_words_file():
    words = ['привет', 'дела']
    create_count_words_file(words)
    assert os.path.isfile('1000 most common words.txt') is True
    os.remove('1000 most common words.txt')


def test_make_dir_with_article():
    make_dir_with_article('article_name', 'article_text')
    assert os.path.isdir('article_name') is True
    assert os.path.isfile('article_name/article_name.txt') is True
    os.remove('article_name/article_name.txt')
    os.rmdir('article_name')
