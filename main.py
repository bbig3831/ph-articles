from collections import namedtuple
from urllib.parse import urljoin

from bs4 import BeautifulSoup
from newspaper import Article
import pandas as pd
import requests


KHN_URL = 'https://khn.org/news/'
YEARS = range(2008, 2022)
MONTHS = range(1, 13)

KhnArticleTuple = namedtuple('KhnArticle', 'headline url publish_dat')


def build_article_list(month: int, year: int):
    # Get content
    url = urljoin(KHN_URL, str(year), str(month))
    r = requests.get(url)
    doc = BeautifulSoup(r.content, 'html.parser')
    results_section = doc.find('section', attrs={'class': 'article-list-results'})
    headlines = results_section.find_all('p', attrs={'class': 'headline'})
    # Parse content
    headlines_list = []
    for headline in headlines:
        data_dict = {
            'headline': headline.a.text,
            'url': headline.a.get('href')
        }
        headlines_list.append(data_dict)

    print(headlines_list)


def download_articles():
    pass


def main():
    pass


if __name__ == '__main__':
    build_article_list(month=3, year=2020)