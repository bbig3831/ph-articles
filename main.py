from collections import namedtuple
from datetime import datetime
from itertools import product

from bs4 import BeautifulSoup
from newspaper import Article
import pandas as pd
import requests


KHN_URL = 'https://khn.org/news'
YEARS = range(2009, 2011)
MONTHS = range(1, 13)

KhnArticleTuple = namedtuple('KhnArticle', 'headline url publish_dat')


def build_article_list(year: int, month: int) -> list:
    # Get content
    page = 1
    headlines_list = []
    while True:
        url = f'{KHN_URL}/{str(year)}/{str(month)}/page/{page}'
        print(f'Getting {url}')
        r = requests.get(url)
        if r.status_code != requests.codes.ok:
            print(f'{url} not found')
            break
        doc = BeautifulSoup(r.content, 'html.parser')
        results_section = doc.find('section', attrs={'class': 'article-list-results'})
        headlines = results_section.find_all('p', attrs={'class': 'headline'})
        # Parse content
        for headline in headlines:
            data_dict = {
                'headline': headline.a.text,
                'url': headline.a.get('href')
            }
            headlines_list.append(data_dict)
        page += 1

    return headlines_list


def download_articles():
    pass


def main():
    pass


if __name__ == '__main__':

    article_list = []
    now = datetime.now()
    for year, month in product(YEARS, MONTHS):
        if (year < now.year) or (year == now.year and month <= now.month):
            print(f'Building article list for {year}-{month}')
            article_list += build_article_list(year=year, month=month)

    for article in article_list[0:10]:
        print(f"{article['headline']} - {article['url']}")