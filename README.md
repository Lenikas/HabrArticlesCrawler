# Web scraper

### Description:
    Автор: Леонид Сагалов
    
    Scraper collects articles from the habrahabr website.
    
    Directory with the article text and images is created for each article.
    
    Also you can find out 1000 of the most popular words in the article,
    which are saved to a file after the script is running.

### Run Scraper:
    python --startscraper https://habr.com/ {articles count} {threads count}
    python app.py --startscraper https://habr.com/ 10 10

### Create venv:
    make venv

### Run tests:
    make test

### Run linters:
    make lint

### Run formatters:
    make format
