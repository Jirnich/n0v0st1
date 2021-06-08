from newspaper import Article
from newsapi.newsapi_client import NewsApiClient
import re


def get_newsurls(limit=5, query=None):
    """Возвращаем список URL-адресов новостей с newsapi.org."""

    #инициализируем newsapi
    KEY = 'ec61773970ad4be09fe56978064fbae6'  # введите свой newsapi ключ
    newsapi = NewsApiClient(api_key=KEY)

    results = list()
    if query is None:  # Получаем топ заголовков русских новостей
        top_headlines_results = newsapi.get_top_headlines(language='ru', country='ru')
        results.extend(top_headlines_results['articles'][:limit])

    else:  # получаем результаты поиска по запросу
        search_results = newsapi.get_everything(q=query, language='ru',
                                                domains='tass.ru, ria.ru, vesti.ru, life.ru , iz.ru')
        results.extend(search_results['articles'][:limit])

    urls = [article['url'] for article in results]

    return urls

def get_newsfeed():
    """Возвращаем список полученных новостных статей"""

    urls = get_newsurls()
    newsfeed = list()
    for num, url in enumerate(urls, start=1):
        article = Article(url)
        article.download()
        article.parse()
        title = str(article.title)

        newsfeed.append(
            (num, url, title)
        )

    return newsfeed

def get_searchfeed(query):
    """Возвращаем список найденных новостных статей."""

    urls = get_newsurls(query=query)

    if urls is not None:
        searchfeed = list()
        for num, url in enumerate(urls, start=1):
            article = Article(url)
            article.download()
            article.parse()
            title = str(article.title)

            searchfeed.append(
                (num, url, title)
            )

        return searchfeed

    else: return None


def summarise(url):
    """Резюмируем полученную новостную статью."""

    article = Article(url)
    article.download()
    article.parse()
    article.nlp()

    return cleanup(article.summary)


def cleanup(text):
    """Удаляем нежелательные слова из текста"""

    junk = re.compile("(AdvertisementAdvertisement)|(.*\(Photo:.*\))")

    return junk.sub('', text)
