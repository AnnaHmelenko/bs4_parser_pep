import argparse
import logging
from logging.handlers import RotatingFileHandler

from constants import LOG_DIR, LOG_FILE, OUTPUT_FILE, OUTPUT_PRETTY


LOG_FORMAT = '"%(asctime)s - [%(levelname)s] - %(message)s"'
DT_FORMAT = '%d.%m.%Y %H:%M:%S'


def configure_argument_parser(available_modes):
    """Создаёт и настраивает парсер аргументов командной строки."""
    parser = argparse.ArgumentParser(
        description='Парсер документации Python'
    )

    parser.add_argument(
        'mode',
        choices=available_modes,
        help='Режимы работы парсера',
    )

    parser.add_argument(
        '-c',
        '--clear-cache',
        action='store_true',
        help='Очистка кеша',
    )

    parser.add_argument(
        '-o',
        '--output',
        choices=(OUTPUT_PRETTY, OUTPUT_FILE),
        help='Дополнительные способы вывода данных',
    )

    return parser


def configure_logging():
    """Создаёт директорию логов и настраивает логирование."""
    LOG_DIR.mkdir(exist_ok=True)

    rotating_handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=10 ** 6,
        backupCount=5,
        encoding='utf-8',
    )

    logging.basicConfig(
        datefmt=DT_FORMAT,
        format=LOG_FORMAT,
        level=logging.INFO,
        encoding='utf-8',
        handlers=(rotating_handler, logging.StreamHandler()),
    )
