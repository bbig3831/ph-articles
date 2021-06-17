import csv
from datetime import datetime
from itertools import product

from bs4 import BeautifulSoup
import requests


KHN_URL = 'https://khn.org/stories'
PAGES = range(1, 610)


def build_article_list() -> list:
    article_list = []
    for page in PAGES:
        url = f'{KHN_URL}/page/{page}'
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
            article_list.append(data_dict)

    return article_list


def main():
    pass


if __name__ == '__main__':

    article_list = build_article_list()

    with open('khn_articles_urls.csv', 'w') as myfile:
        print(f'Saving data')
        writer = csv.DictWriter(myfile, fieldnames=['headline', 'url'])
        writer.writeheader()
        for article in article_list:
            writer.writerow(article)