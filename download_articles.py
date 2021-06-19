import csv
from multiprocessing.dummy import Pool

from newspaper import Article
import pandas as pd

def open_csv():
    with open('khn_articles_urls.csv', 'r') as myfile:
        reader = csv.DictReader(myfile)
        dict_list = []
        for line in reader:
            dict_list.append(line)

    return dict_list


def get_article_data(article_dict: dict):
    article = Article(article_dict['url'], fetch_images=False)
    article.download()
    article.parse()
    article.nlp()

    article_data = {
        'headline': article_dict['headline'],
        'url': article_dict['url'],
        'tags': article.tags,
        'summary': article.summary,
        'keywords': article.keywords,
        'publish_date': article.publish_date,
        'authors': article.authors
    }
    return article_data


def main():
    article_list = open_csv()
    pool = Pool(10)
    results = pool.map(get_article_data, article_list)
    with open('khn_data.csv', 'w') as myfile:
        print('Saving data')
        writer = csv.DictWriter(myfile, fieldnames=['headline', 'url', 'tags', 'summary', 'keywords', 'publish_date', 'authors'])
        writer.writeheader()
        for result in results:
            writer.writerow(result)


if __name__ == '__main__':
    main()