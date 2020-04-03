from web_scraper.start import start_scraper
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
        except ValueError:
            raise ValueError('Articles and threads count must be a number above zero')
        start_scraper(start_link, articles_count, threads_count)
    else:
        raise SyntaxError('usage: main_console.py [-h] [--startscraper]')


if __name__ == "__main__":
    main()
