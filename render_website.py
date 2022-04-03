import json
import os
from livereload import Server
from more_itertools import chunked
from jinja2 import Environment, FileSystemLoader, select_autoescape
from urllib.parse import quote


COUNT_BOOKS_ON_PAGE = 20


def on_reload():

    with open('books_description.json', 'r') as file:
        books_description = json.load(file)

    for book in books_description:
        book['image_url'] = (
            quote('../images/{}'.format(os.path.basename(book['image_url'])))
        )
        book['txt_url'] = (
            '../books/{}.txt'.format(book['title'])
        )
    env = Environment(loader=FileSystemLoader('.'),
                      autoescape=select_autoescape(['html', 'xml']))
    template = env.get_template('template.html')
    os.makedirs('pages', exist_ok=True)
    books_description = list(chunked(books_description, COUNT_BOOKS_ON_PAGE))
    pages_numbers = [num for num, chunk in enumerate(books_description, 1)]
    for page_number, books_chunk in enumerate(books_description, 1):
        books_on_page = list(chunked(books_chunk, 2))
        rendered_page = template.render(books_on_page=books_on_page,
                                        pages_numbers=pages_numbers,
                                        page_number=page_number)
        with open(f'pages/index{page_number}.html',
                  'w', encoding="utf8") as file:
            file.write(rendered_page)


def main():

    on_reload()
    server = Server()
    server.watch('template.html', on_reload)
    server.serve(root='.')


if __name__ in '__main__':
    main()
