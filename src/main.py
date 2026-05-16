import logging
import re
from collections import defaultdict
from urllib.parse import urljoin

import requests_cache
from tqdm import tqdm

from configs import configure_argument_parser, configure_logging
from constants import (
    BASE_DIR,
    DOWNLOADS_DIR_NAME,
    EXPECTED_STATUS,
    MAIN_DOC_URL,
    MIN_PEP_TABLE_COLUMNS,
    MODE_DOWNLOAD,
    MODE_LATEST_VERSIONS,
    MODE_PEP,
    MODE_WHATS_NEW,
    PEP_NUMERICAL_URL,
    PEP_URL,
)
from exceptions import (
    ParserDownloadException,
    ParserFindTagException,
    ParserListException,
    ParserResponseException,
    ParserStatusException,
)
from outputs import control_output
from utils import find_tag, get_response, get_soup


def whats_new(session):
    """Парсит ссылки на статьи о нововведениях Python."""
    whats_new_url = urljoin(MAIN_DOC_URL, 'whatsnew/')
    soup = get_soup(session, whats_new_url)

    main_div = find_tag(
        soup,
        'section',
        attrs={'id': 'what-s-new-in-python'}
    )
    div_with_ul = find_tag(
        main_div,
        'div',
        attrs={'class': 'toctree-wrapper'}
    )

    sections_by_python = div_with_ul.find_all(
        'li',
        attrs={'class': 'toctree-l1'}
    )

    results = [('Ссылка на статью', 'Заголовок', 'Редактор, автор')]
    errors = []

    for section in tqdm(sections_by_python):
        try:
            version_a_tag = find_tag(section, 'a')
            version_link = urljoin(whats_new_url, version_a_tag['href'])

            soup = get_soup(session, version_link)

            h1 = find_tag(soup, 'h1')
            dl = find_tag(soup, 'dl')
            dl_text = dl.text.replace('\n', ' ')

            results.append((version_link, h1.text, dl_text))
        except (ParserResponseException, ParserFindTagException) as error:
            errors.append(str(error))

    if errors:
        logging.warning('\n'.join(errors))

    return results


def latest_versions(session):
    """Парсит версии Python, ссылки на документацию и статусы версий."""
    soup = get_soup(session, MAIN_DOC_URL)

    sidebar = find_tag(
        soup,
        'div',
        attrs={'class': 'sphinxsidebarwrapper'}
    )
    ul_tags = sidebar.find_all('ul')

    for ul in ul_tags:
        if 'All versions' in ul.text:
            a_tags = ul.find_all('a')
            break
    else:
        raise ParserListException('Не найден список c версиями Python')

    results = [('Ссылка на документацию', 'Версия', 'Статус')]
    pattern = r'Python (?P<version>\d\.\d+) \((?P<status>.*)\)'

    for a_tag in a_tags:
        link = a_tag['href']
        text_match = re.search(pattern, a_tag.text)

        if text_match is not None:
            version, status = text_match.groups()
        else:
            version, status = a_tag.text, ''

        results.append((link, version, status))

    return results


def download(session):
    """Скачивает архив документации Python."""
    downloads_url = urljoin(MAIN_DOC_URL, 'download.html')
    soup = get_soup(session, downloads_url)

    archive_tag = soup.find(
        'a',
        attrs={'href': re.compile(r'.+\.zip$')}
    )

    if archive_tag is None:
        raise ParserDownloadException(
            'Не найдена ссылка на архив документации'
        )

    archive_url = urljoin(downloads_url, archive_tag['href'])

    downloads_dir = BASE_DIR / DOWNLOADS_DIR_NAME
    downloads_dir.mkdir(exist_ok=True)

    archive_path = downloads_dir / archive_url.split('/')[-1]

    response = get_response(session, archive_url)

    with open(archive_path, 'wb') as file:
        file.write(response.content)

    logging.info(f'Архив был загружен и сохранён: {archive_path}')


def get_pep_status(soup):
    """Извлекает статус PEP со страницы документа."""
    match = re.search(
        r'Status:\s+([A-Za-z -]+)',
        soup.get_text()
    )

    if match is None:
        raise ParserStatusException('Не найден статус PEP')

    return match.group(1).strip()


def process_pep_row(session, row):
    """Обрабатывает одну строку таблицы PEP."""
    columns = row.find_all('td')

    if len(columns) < MIN_PEP_TABLE_COLUMNS:
        return None

    first_column_tag = columns[0]
    preview_status = first_column_tag.text.strip()[1:]

    pep_link_tag = row.find('a')

    if pep_link_tag is None:
        return None

    href = pep_link_tag['href']

    if not re.search(r'pep-\d+', href):
        return None

    pep_link = urljoin(PEP_URL, href)

    if re.search(r'pep-0+/?$', pep_link):
        return None

    pep_soup = get_soup(session, pep_link)
    status = get_pep_status(pep_soup)

    return pep_link, preview_status, status


def pep(session):
    """Парсит статусы PEP и считает количество документов по статусам."""
    soup = get_soup(session, PEP_NUMERICAL_URL)
    rows = soup.find_all('tr')

    status_counter = defaultdict(int)
    errors = []
    mismatched_statuses = []

    for row in tqdm(rows):
        try:
            result = process_pep_row(session, row)

            if result is None:
                continue

            pep_link, preview_status, status = result

        except (
            ParserResponseException,
            ParserStatusException,
        ) as error:
            errors.append(str(error))
            continue

        expected_statuses = EXPECTED_STATUS.get(preview_status, ())

        if status not in expected_statuses:
            mismatched_statuses.append(
                'Несовпадающие статусы:\n'
                f'{pep_link}\n'
                f'Статус в карточке: {status}\n'
                f'Ожидаемые статусы: {list(expected_statuses)}'
            )

        status_counter[status] += 1

    if errors:
        logging.warning('\n'.join(errors))

    if mismatched_statuses:
        logging.info('\n'.join(mismatched_statuses))

    return [
        ('Статус', 'Количество'),
        *sorted(status_counter.items()),
        ('Total', sum(status_counter.values())),
    ]


MODE_TO_FUNCTION = {
    MODE_WHATS_NEW: whats_new,
    MODE_LATEST_VERSIONS: latest_versions,
    MODE_DOWNLOAD: download,
    MODE_PEP: pep,
}


def main():
    """Запускает выбранный режим парсера."""
    configure_logging()

    try:
        logging.info('Парсер запущен!')

        arg_parser = configure_argument_parser(MODE_TO_FUNCTION.keys())
        args = arg_parser.parse_args()

        logging.info(f'Аргументы командной строки: {args}')

        session = requests_cache.CachedSession()

        if args.clear_cache:
            session.cache.clear()

        parser_mode = args.mode
        results = MODE_TO_FUNCTION[parser_mode](session)

        if results is not None:
            control_output(results, args)

        logging.info('Парсер завершил работу.')
    except Exception:
        logging.exception('Парсер завершился с ошибкой', stack_info=True)


if __name__ == '__main__':
    main()
