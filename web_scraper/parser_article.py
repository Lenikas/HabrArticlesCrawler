import re
from typing import List

from bs4 import BeautifulSoup


class ArticleParser:
    tag_regex = re.compile(r'<[^>]+>')

    def __init__(self, article_name: str, article_url: str, soup: BeautifulSoup):
        self.article_name = article_name
        self.article_url = article_url
        self.soup = soup
        self.text = ''
        self.images: List[str] = []

    def find_text(self) -> str:
        text = self.soup.findAll(
            'div', {'class': 'post__text post__text-html post__text_v1'}
        )
        self.text = ArticleParser.tag_regex.sub('', text[0].text)
        return self.text

    def find_images(self) -> List[str]:
        text = self.soup.findAll(
            'div', {'class': 'post__text post__text-html post__text_v1'}
        )
        images = text[0].findAll('img')
        for image in images:
            self.images.append(image.get('src'))
        return self.images
