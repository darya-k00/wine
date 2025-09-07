from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
from datetime import datetime
from pandas import read_excel
from collections import defaultdict
from argparse import ArgumentParser


def define_word(year=1920):
    year1 = ' лет'
    year2 = ' год'
    year3 = ' года'

    now = datetime.now()
    number = now.year - year
    if number % 100 in range(11, 21):
        return f'{number}{year1}'
    elif number % 10 == 1:
        return f'{number}{year2}'
    elif number % 10 in range(2, 5):
        return f"{number}{year3}"
    else:
        return f"{number}{year1}"


def format_attributes(drink_number: int, drinks_info: dict):
    attributes = [drinks_info[attribute][drink_number] for attribute in drinks_info]
    formatted_attributes = {
        "Картинка": attributes[4],
        "Категория": attributes[0],
        "Название": attributes[1],
        "Сорт": attributes[2],
        "Цена": attributes[3],
        "Акция": attributes[5]
    }
    return formatted_attributes


def main():
    parser = ArgumentParser(description="Сайт с напиткамию.")
    parser.add_argument("--file", type=str, default="wine3.xlsx", help="Файл таблицы, из которого будут взяты данные, есои файл не указан, то по умолчанию будет использоваться 'wine.xlsx'")
    args = parser.parse_args()
    excel_data = read_excel(args.file, na_values=["nan"], keep_default_na=False).to_dict(orient='list')
    wines_by_category = defaultdict(list)
    
    for wine in wines:
        wines_by_category[wine['Категория']].append(wine)

    env = Environment(loader=FileSystemLoader('templates')) 
    template = env.get_template('template.html')
    
    rendered_page = template.render(
        year_logo= word_define(),
        wines_by_category=wines_by_category
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == "__main__":
    main()
