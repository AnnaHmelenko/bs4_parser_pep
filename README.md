# BS4 Parser PEP

Парсер документации Python и документов PEP.

## Описание проекта

Проект собирает данные с официальных страниц документации Python и сайта PEP.  
Программа работает из командной строки и поддерживает несколько режимов:

- `whats-new` — сбор ссылок на статьи о нововведениях Python;
- `latest-versions` — сбор информации о версиях Python и их статусах;
- `download` — скачивание архива документации Python;
- `pep` — сбор статистики по статусам PEP-документов.

Результаты можно вывести в терминал, в таблицу PrettyTable или сохранить в CSV-файл.

## Стек технологий

- Python
- BeautifulSoup4
- requests-cache
- tqdm
- PrettyTable
- pytest

## Как запустить проект

Клонировать репозиторий:

```bash
git clone https://github.com/AnnaHmelenko/bs4_parser_pep.git
cd bs4_parser_pep
```

## Создать и активировать виртуальное окружение:
 ```bash
 python -m venv venv
 ```
  ```bash
 source venv/bin/activate
 ```

## Установить зависимости:
 ```bash
pip install -r requirements.txt
 ```

## Запустить парсер PEP с сохранением результата в CSV:
 ```bash
python src/main.py pep --output file
 ```

## Очистить кеш перед запуском:
 ```bash
python src/main.py pep --output file --clear-cache
 ```

## Очистить кеш перед запуском:
 ```bash
python src/main.py pep --output file --clear-cache
 ```

## Запустить тесты:
 ```bash
pytest
 ```

## Примеры команд
Выведет справку по использованию
```
python main.py pep -h
```

Создаст csv файл с таблицей из двух колонок: «Статус» и «Количество»:
```
python main.py pep -o file
```

Выводит таблицу prettytable с тремя колонками: "Ссылка на документацию", "Версия", "Статус":
```
python main.py latest-versions -o pretty 
```

Выводит ссылки в консоль на нововведения в python:
```
python main.py whats-new
```

Автор: https://github.com/AnnaHmelenko