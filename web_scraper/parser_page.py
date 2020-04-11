from typing import Dict

from bs4 import BeautifulSoup


class PageParser:
    def __init__(self, page_url: str, soup: BeautifulSoup):
        self.page = page_url
        self.soup = soup
        self.articles: Dict[str, str] = {}
        self.next_page = ''

    def find_articles(self) -> Dict[str, str]:
        links = self.soup.findAll('a', {'class': 'post__title_link'})
        for link in links:
            self.articles[link.string] = link.get('href')
        return self.articles

    def find_next_button(self) -> str:
        next_button = self.soup.find_all(
            'a',
            {'class': 'arrows-pagination__item-link arrows-pagination__item-link_next'},
        )
        button_url = next_button[0].get('href')
        if button_url[0:5] != 'https':
            self.next_page = 'https://habr.com' + button_url
        else:
            self.next_page = button_url
        print(self.next_page)
        return self.next_page
