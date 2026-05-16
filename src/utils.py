from bs4 import BeautifulSoup
from requests import RequestException

from exceptions import ParserFindTagException, ParserResponseException


def get_response(session, url):
    """Загружает страницу и возвращает HTTP-ответ."""
    try:
        session.trust_env = False
        response = session.get(url, proxies={})
        response.encoding = 'utf-8'
        return response
    except RequestException as error:
        raise ParserResponseException(
            f'Возникла ошибка при загрузке страницы {url}'
        ) from error


def get_soup(session, url):
    """Загружает страницу и возвращает объект BeautifulSoup."""
    response = get_response(session, url)
    return BeautifulSoup(response.text, 'lxml')


def find_tag(soup, tag, attrs=None):
    """Ищет тег в HTML-структуре и вызывает исключение, если тег не найден."""
    searched_tag = soup.find(tag, attrs=(attrs or {}))

    if searched_tag is None:
        raise ParserFindTagException(f'Не найден тег {tag} {attrs}')

    return searched_tag
