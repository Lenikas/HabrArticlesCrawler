import os
import re
import urllib
from collections import Counter
from pathlib import Path
from typing import List

import pymorphy2
import requests
from bs4 import BeautifulSoup


def do_request(link: str) -> BeautifulSoup:
    try:
        page = requests.get(link)
    except requests.exceptions.ConnectionError as e:
        raise ConnectionError from e
    data = page.text
    soup = BeautifulSoup(data, features='html5lib')
    return soup


def download_images(images: List[str], path: Path) -> None:
    try:
        for image in images:
            urllib.request.urlretrieve(image, path / os.path.basename(image))
    except urllib.error.URLError as e:
        raise e


def make_dir_with_article(article_name: str, article_text: str) -> Path:
    path = Path.cwd() / article_name
    Path.mkdir(path)
    with open(path / '{0}.txt'.format(article_name), 'w') as f:
        f.write(article_text)
    return path


def validate_arguments(articles_count: int, threads_count: int) -> bool:
    return articles_count > 0 and threads_count > 0


def extract_words(text: str) -> List[str]:
    words = re.findall(r'\w+', text.lower())
    morph = pymorphy2.MorphAnalyzer()
    needed_words = []
    for word in words:
        tag = (morph.parse(word)[0]).tag
        if 'INTJ' in tag or 'PRCL' in tag or 'CONJ' in tag or 'PREP' in tag:
            continue
        needed_words.append(word)
    return needed_words


def create_count_words_file(words: List[str]) -> None:
    with open('1000 most common words.txt', 'w') as f:
        counter = Counter(words)
        sorted_counter = Counter(
            {v: k for k, v in sorted(counter.items(), key=lambda pair: pair[1])}
        ).most_common(1000)
        for item in sorted_counter:
            f.write(f'{item[1]} - {item[0]} \n')
