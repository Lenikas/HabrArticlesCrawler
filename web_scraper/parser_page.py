from web_scraper.utils import do_request


class PageParser:
    def __init__(self, page_url: str):
        self.page = page_url
        self.soup = do_request(self.page)
        self.articles = {}
        self.next_page = ''

    def find_articles(self):
        links = self.soup.findAll('a', {'class': 'post__title_link'})
        for link in links:
            self.articles[link.string] = link.get('href')
        return self.articles

    def find_next_button(self):
        next_button = self.soup.find_all(
            'a',
            {'class': 'arrows-pagination__item-link arrows-pagination__item-link_next'},
        )
        self.next_page = 'https://habr.com' + next_button[0].get('href')
        return self.next_page
