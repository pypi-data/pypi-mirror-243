# LightFlask Base

import os
from markdown2 import markdown

class LightFlask:
    def __init__(self, app):
        self.app = app
        self.dir = ''
        self.markdown_routes = {}

    def route(self, url, markdown_file):
        def decorator(view_func):
            self.markdown_routes[url] = {'view_func': view_func, 'markdown_file': markdown_file}
            return view_func
        return decorator

    def get_content(self, markdown_file):
        file_path = os.path.join(self.dir, markdown_file)
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                return markdown(content)
        else:
            return f"Markdown dosyası bulunamadı: {markdown_file}"

    def register_routes(self):
        for url, route_info in self.markdown_routes.items():
            view_func = route_info['view_func']
            markdown_file = route_info['markdown_file']
            html_content = self.get_content(markdown_file)

            self.app.route(url)(view_func)