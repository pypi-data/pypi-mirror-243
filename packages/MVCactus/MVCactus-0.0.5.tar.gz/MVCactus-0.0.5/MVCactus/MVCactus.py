import cgi
import http.server
import mimetypes
import os
import re
import socketserver
from Placeholdr.placeholdr import Placeholdr


class MVCactus(http.server.BaseHTTPRequestHandler):
    routes = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # current_dir = os.path.dirname(os.path.abspath(__file__))
        # print(f'Current dir: {current_dir}')
        templates_dir = os.path.join('templates')
        self.template_engine = Placeholdr(templates_dir)

    @classmethod
    def route(cls, pattern):
        def wrapper(callback):
            regex_pattern = f'^{pattern}$'
            cls.routes.append((regex_pattern, callback))
            return callback

        return wrapper

    def url_for_static(self, filename):
        return f'/static/{filename}'

    def handle_error(self, status, message, template_name='upload.html', context=None):
        self.send_error(status, message)
        if context is None:
            context = {}
        context['status'] = status
        context['message'] = message
        self.render_template(template_name, context)

    def send_response_headers(self, content_type, content_length=None):
        self.send_response(200)
        self.send_header('Content-Type', content_type)
        if content_length is not None:
            self.send_header('Content-Length', str(content_length))
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.send_header('X-Frame-Options', 'SAMEORIGIN')
        self.send_header('X-XSS-Protection', '1; mode=block')
        self.send_header('Referrer-Policy', 'no-referrer')
        self.send_header('Feature-Policy', "geolocation 'none'; microphone 'none'; camera 'none'")
        self.end_headers()

    def do_GET(self):
        if self.path.startswith('/static/'):
            path = self.path[7:]
            self.serve_static_file(path)
            return

        for pattern, callback in self.routes:
            match = re.match(pattern, self.path)
            if match:
                callback(self, match)
                return

        self.send_response(404)
        self.end_headers()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        content_type = self.headers['Content-Type']

        if 'multipart/form-data' in content_type:
            fields = cgi.FieldStorage(fp=self.rfile, headers=self.headers, environ={
                'REQUEST_METHOD': 'POST',
                'CONTENT_TYPE': content_type,
            })

            if 'file' in fields:
                file_item = fields['file']
                filename = os.path.join('uploads', file_item.filename)
                with open(filename, 'wb') as f:
                    f.write(file_item.file.read())
                self.send_response(200)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(b'Successfully uploaded file')

                return
        else:
            body = self.rfile.read(content_length).decode('utf-8')

            for pattern, callback in self.routes:
                if self.path == pattern and callback.__name__ == 'handle_post':
                    callback(self, body)
                    return

        self.send_response(404)
        self.end_headers()

    @classmethod
    def post(cls, path):
        def wrapper(callback):
            cls.routes.append((path, callback))
            return callback

        return wrapper

    @staticmethod
    def handle_post(handler, body):
        handler.send_response(200)
        handler.send_header('Content-type', 'text/plain')
        handler.end_headers()
        handler.wfile.write(body.encode('utf-8'))

    def serve_static_file(self, path):
        print(f'Path: {path}')
        try:
            current_dir = os.path.abspath("static")
            file_path = f"{current_dir}{path}"
            print(f'Serving static file: {file_path}')

            if not os.path.isfile(file_path):
                raise IOError

            mime_type, _ = mimetypes.guess_type(path)
            content_length = os.path.getsize(file_path)

            self.send_response_headers(mime_type, content_length)

            with open(file_path, 'rb') as f:
                chunk_size = 8192
                while True:
                    chunk = f.read(chunk_size)
                    if not chunk:
                        break
                    self.wfile.write(chunk)
        except IOError:
            self.send_error(404, 'File not found')

    def validate_input(self, data, fields):
        missing_fields = []
        for field in fields:
            if field not in data:
                missing_fields.append(field)
        if missing_fields:
            self.send_error(400, f'Missing fields: {", ".join(missing_fields)}')
            return False
        return True

    def change_placeholdr_syntax(self, open_tag, close_tag):
        # Assuming Placeholdr has a method to update its syntax
        self.template_engine.specify_syntax(open_tag, close_tag)

    def render_template(self, template_name, style_path, script_path, context=None):
        print(f'Rendering template: {template_name}')
        if context is None:
            context = {}

        # Add URLs for static files
        context['styles_css'] = self.url_for_static(style_path)
        context['script_js'] = self.url_for_static(script_path)

        # Use Placeholdr to render the template
        template_path = os.path.join('templates', template_name)
        template = Placeholdr(template_path)
        output = template.render(context)
        self.send_response_headers('text/html', len(output))
        self.wfile.write(output.encode('utf-8'))



class MVCactusRun:

    def __init__(self, address='localhost', port=8080):
        self.ADDRESS = address
        self.PORT = port

    def run(self, app_class):
        with socketserver.TCPServer((self.ADDRESS, self.PORT), app_class) as httpd:
            print(f"Running on {self.ADDRESS}:{self.PORT}")
            print(f"Enter here: http://{self.ADDRESS}:{self.PORT}/")
            if "static" or "templates" not in os.listdir():
                if "static" not in os.listdir():
                    os.mkdir("static")
                    print("* Static folder created")
                elif "templates" not in os.listdir():
                    os.mkdir("templates")
                    print("* Templates folder created")
            print("* Press Ctrl+C to stop")
            print("========================================")

            httpd.serve_forever()



"""
File structure:

    your_project_directory/
    │
    ├── MVCactus/             # Directory containing your MVCactus class
    │   └── ...
    │
    ├── templates/            # Directory containing your HTML templates
    │   ├── home.html
    │   ├── about.html
    │   └── ...
    │
    ├── static/               # Directory containing all static files like CSS, JS, images
    │   ├── css/              # Subdirectory for CSS files
    │   │   ├── home.css
    │   │   ├── about.css
    │   │   └── ...
    │   │
    │   ├── js/               # Subdirectory for JavaScript files
    │   │   ├── home.js
    │   │   ├── about.js
    │   │   └── ...
    │   │
    │   └── img/              # Subdirectory for images
    │       ├── logo.png
    │       └── ...
    │
    └── main.py               # Main Python file to run your web server

"""