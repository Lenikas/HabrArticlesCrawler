from web_scraper.start import start_scraper
from web_scraper.utils import validate_arguments
import argparse


def parse_args():
    parser = argparse.ArgumentParser(description='Habr scraper')
    parser.add_argument(
        '--startscraper',
        nargs=3,
        help=r'python main_console --startscraper {link for start} {articles count} {threads count}',
    )
    return parser.parse_args()


def main():
    args = parse_args()
    if args.startscraper:
        start_link = args.startscraper[0]
        try:
            articles_count = int(args.startscraper[1])
            threads_count = int(args.startscraper[2])
            if not validate_arguments(articles_count, threads_count):
                raise ValueError
        except ValueError:
            raise ValueError('Articles and threads count must be a number above zero')
        start_scraper(start_link, articles_count, threads_count)


if __name__ == "__main__":
    main()

