import os
import re
import urllib
from pathlib import Path

import pymorphy2
import requests
from bs4 import BeautifulSoup
from collections import Counter

def do_request(link: str):
    try:
        page = requests.get(link)
    except requests.exceptions.ConnectionError:
        raise ConnectionError
    data = page.text
    soup = BeautifulSoup(data, features="html5lib")
    return soup


def download_images(images, path):
    try:
        for image in images:
            urllib.request.urlretrieve(image, path / os.path.basename(image))
    except Exception as e:
        raise e


def make_dir_article(article_name, article_text, article_images):
    path = Path.cwd() / article_name
    Path.mkdir(path)
    # download_images(article_images, path)
    with open(path / '{0}.txt'.format(article_name), 'w') as f:
        f.write(article_text)
    return path


def validate_arguments(articles_count, threads_count):
    return articles_count > 0 and threads_count > 0


def calculate_words(text: str):
    words = re.findall(r'\w+', text.lower())
    morph = pymorphy2.MorphAnalyzer()
    needed_words = []
    for word in words:
        tag = (morph.parse(word)[0]).tag
        if 'INTJ' in tag or 'PRCL' in tag or 'CONJ' in tag or 'PREP' in tag:
            continue
        needed_words.append(word)
    return needed_words


def create_count_words_file(words):
    with open('1000 most common words.txt', 'w') as f:
        counter = Counter(words)
        sorted_counter = Counter(
            {k: v for k, v in sorted(counter.items(), key=lambda pair: pair[1])}
        ).most_common(1000)
        for item in sorted_counter:
            f.write('{0} - {1}'.format(item[0], item[1]) + '\n')