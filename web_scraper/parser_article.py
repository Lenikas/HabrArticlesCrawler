import re
from typing import List, Tuple

from bs4 import BeautifulSoup


class ArticleParser:
    def __init__(self, article_name: str, article_url: str, soup: BeautifulSoup):
        self.article_name = article_name
        self.article_url = article_url
        # self.soup = do_request(self.article_url)
        self.soup = soup
        self.text = ''
        self.images: List[str] = []

    def find_text_and_images(self) -> Tuple[str, List[str]]:
        text = self.soup.findAll(
            'div', {'class': 'post__text post__text-html post__text_v1'}
        )

        images = text[0].findAll('img')
        for image in images:
            self.images.append(image.get('src'))

        tag_regex = re.compile(r'<[^>]+>')
        self.text = tag_regex.sub('', text[0].text)
        return self.text, self.images
