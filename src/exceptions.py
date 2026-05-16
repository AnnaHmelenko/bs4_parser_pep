class ParserFindTagException(Exception):
    """Вызывается, когда парсер не может найти тег."""


class ParserResponseException(Exception):
    """Вызывается, когда страница не загрузилась."""


class ParserListException(Exception):
    """Вызывается, когда парсер не может найти нужный список."""


class ParserDownloadException(Exception):
    """Вызывается, когда парсер не может найти архив документации."""


class ParserStatusException(Exception):
    """Вызывается, когда парсер не может найти статус PEP."""
