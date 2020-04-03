import argparse
import concurrent.futures as cf

from web_scraper.parser_article import ArticleParser
from web_scraper.parser_page import PageParser
from web_scraper.utils import (
    calculate_words,
    download_images,
    make_dir_article,
    validate_arguments,
    create_count_words_file,
)


def parse_args():
    parser = argparse.ArgumentParser(description="Habr scraper")
    parser.add_argument(
        '--startscraper',
        nargs=3,
        help=r"python main_console --startscraper {link for start} {articles count} {threads count}",
    )
    return parser.parse_args()


def worker(article_data, all_words: list):
    article_name = article_data[0]
    article_url = article_data[1]
    try:
        article_parser = ArticleParser(article_name, article_url)
        text, images = article_parser.find_text_and_images()
        needed_words_article = calculate_words(text)
        all_words.extend(needed_words_article)
        path = make_dir_article(article_name, text, images)
        download_images(images, path)
        return "Download: {0}".format(article_name)
    except (Exception, ConnectionError) as e:
        #   знаю,что плохая практика ловить на эксепшен,но там фиг разберешь,какая ошибка с urrlib придет
        return "Exception {0} in worker {1}".format(e, article_name)


def prepare_articles(articles, articles_count, first_page: PageParser):
    if len(articles) > articles_count:
        result = list(list(articles.items()))
    else:
        next_button = first_page.find_next_button()
        result = list(list(articles.items()))
        while len(result) <= articles_count:
            current_page = PageParser(next_button)
            next_button = current_page.find_next_button()
            next_articles = current_page.find_articles()
            for item in list(list(next_articles.items())):
                result.append(item)
    return result[:articles_count]


def start_scraper(start_link, articles_count, threads_count):
    if validate_arguments(articles_count, threads_count):
        page = PageParser(start_link)
        articles = page.find_articles()
        data_download = prepare_articles(articles, articles_count, page)

        words = []
        with cf.ThreadPoolExecutor(max_workers=threads_count) as executor:
            future_articles = {
                executor.submit(worker, data, words): data for data in data_download
            }
            for future in cf.as_completed(future_articles):
                article = future_articles[future]
                try:
                    data = future.result()
                    print("{0}".format(data))
                except Exception as exc:
                    print("Exception {0} on article: {1}".format(exc, article))
        create_count_words_file(words)
    else:
        raise ValueError("Articles and threads count must be a number above zero")


def main():
    args = parse_args()
    if args.startscraper:
        start_link = args.startscraper[0]
        try:
            articles_count = int(args.startscraper[1])
            threads_count = int(args.startscraper[2])
        except ValueError:
            raise ValueError("Articles and threads count must be a number above zero")
        start_scraper(start_link, articles_count, threads_count)
    else:
        raise SyntaxError("usage: main_console.py [-h] [--startscraper]")
