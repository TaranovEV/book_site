import json
import os
from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
from urllib.parse import quote, urljoin


def main():
    with open('books_description.json', 'r') as file:
        books_description = json.load(file)

    for book in books_description:
        book['image_url'] = quote(
                            urljoin('images/',
                                    os.path.basename(book['image_url'])
                                    )
                                  )

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')
    rendered_page = template.render(
        books_description=books_description
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ in '__main__':
    main()
