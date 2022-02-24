import json
import os
from livereload import Server
from more_itertools import chunked
from jinja2 import Environment, FileSystemLoader, select_autoescape
from urllib.parse import quote, urljoin


def on_reload():

    with open('books_description.json', 'r') as file:
        books_description = json.load(file)

    for book in books_description:
        book['image_url'] = quote(
                            urljoin('images/',
                                    os.path.basename(book['image_url'])
                                    )
                                  )
        book['txt_url'] = (
            quote('books/{title}.txt'.format(title=book['title']))
        )
    env = Environment(loader=FileSystemLoader('.'),
                      autoescape=select_autoescape(['html', 'xml']))

    template = env.get_template('template.html')
    books_description = list(chunked(books_description, 2))
    rendered_page = template.render(books_description=books_description)
    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

def main():

    on_reload()
    server = Server()
    server.watch('template.html', on_reload)
    server.serve(root='.')


if __name__ in '__main__':
    main()
