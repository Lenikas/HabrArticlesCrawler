import re

from web_scraper.utils import do_request


class ArticleParser:
    def __init__(self, article_name, article_url):
        self.article_name = article_name
        self.article_url = article_url
        self.soup = do_request(self.article_url)
        self.text = []
        self.images = []

    def find_text_and_images(self):
        text = self.soup.findAll(
            'div', {'class': 'post__text post__text-html post__text_v1'}
        )

        images = text[0].findAll('img')
        for image in images:
            self.images.append(image.get('src'))

        tag_regex = re.compile(r'<[^>]+>')
        self.text = tag_regex.sub('', text[0].text)
        return self.text, self.images
