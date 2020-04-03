import concurrent.futures as cf
import urllib.error
from typing import Dict, List, Tuple

from web_scraper.parser_article import ArticleParser
from web_scraper.parser_page import PageParser
from web_scraper.utils import (
    create_count_words_file,
    do_request,
    download_images,
    extract_words,
    make_dir_with_article,
    validate_arguments,
)


def worker(article_data: Tuple[str, str], all_words: List[str]) -> str:
    article_name = article_data[0]
    article_url = article_data[1]
    try:
        article_parser = ArticleParser(
            article_name, article_url, do_request(article_url)
        )
        text, images = article_parser.find_text_and_images()
        needed_words_article = extract_words(text)
        all_words.extend(needed_words_article)
        path = make_dir_with_article(article_name, text)
        download_images(images, path)
        return 'Download: {0}'.format(article_name)
    except (urllib.error.URLError, ConnectionError) as e:
        #   знаю,что плохая практика ловить на эксепшен,
        #   но там фиг разберешь,какая ошибка с urrlib придет
        return 'Exception {0} in worker {1}'.format(e, article_name)


def prepare_articles(
    articles: Dict[str, str], needed_count: int, first_page: PageParser
) -> List[Tuple[str, str]]:
    if len(articles) > needed_count:
        result = list(list(articles.items()))
    else:
        next_button = first_page.find_next_button()
        result = list(list(articles.items()))

        while len(result) <= needed_count:
            current_page = PageParser(next_button, do_request(next_button))
            next_button = current_page.find_next_button()
            next_articles = current_page.find_articles()
            for item in list(list(next_articles.items())):
                result.append(item)
    return result[:needed_count]


def start_scraper(start_link: str, articles_count: int, threads_count: int) -> None:
    if validate_arguments(articles_count, threads_count):
        page = PageParser(start_link, do_request(start_link))
        articles = page.find_articles()
        data_download = prepare_articles(articles, articles_count, page)

        words: List[str] = []
        with cf.ThreadPoolExecutor(max_workers=threads_count) as executor:
            future_articles = {
                executor.submit(worker, data, words): data for data in data_download
            }
            for future in cf.as_completed(future_articles):
                article = future_articles[future]
                try:
                    data = future.result()
                    print('{0}'.format(data))
                except urllib.error.URLError as exc:
                    print('Exception {0} on article: {1}'.format(exc, article))
        create_count_words_file(words)
    else:
        raise ValueError('Articles and threads count must be a number above zero')
