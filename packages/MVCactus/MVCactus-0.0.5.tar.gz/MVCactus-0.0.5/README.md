# MVCactus
#### Version: 0.0.5
## Description

MVCactus is a micro-framework designed for building simple and efficient web applications. Utilizing Python's standard HTTP server capabilities, MVCactus is an ideal choice for small-scale projects, educational purposes, and rapid prototyping. It offers a minimalist approach to web server architecture, supporting dynamic template rendering and static file serving.

## Key Features

# MVCactus Features

MVCactus, a Python-based web micro-framework, provides a range of features for efficient and straightforward web development:

- **Route Definition**: Ability to define URL patterns and associate them with Python functions using decorators.
    - Supports both `GET` and `POST` requests.
- **Dynamic Template Rendering**: Uses the `Placeholdr` templating engine to render HTML templates dynamically.
- **Static File Serving**: Serves static content such as CSS, JavaScript, and images from a designated `static` directory.
- **Custom Error Handling**: Provides methods to handle various HTTP errors with custom responses.
- **HTTP Headers Management**: Allows setting and managing various HTTP response headers.
- **File Upload Handling**: Supports handling of file uploads through multipart/form-data.
- **Input Validation**: Provides functionality to validate request data against specified required fields.
- **Customizable Placeholdr Syntax**: Offers the capability to change the placeholder syntax used in templates.
## Installation

To use MVCactus, ensure you have Python installed on your system; then, install MVCactus using `pip`:
```bash
pip install MVCactus
```

This will install the latest version of MVCactus and its dependencies.

## Quick Start

### Rendering Templates & Serving Static Files
    
        ```python
        class MyApp(MVCactus):
        
            @MVCactus.route('/')
            def index(self, match):
                context = {
                    'title': 'MVCactus',
                }
                self.render_template('templates/index.html', 'css/styles.css', 'js/script.js', context)
        ```

### Running the Server
    
            ```python
            if __name__ == '__main__':
                app = MyApp
                server = MVCactusRun(port=8080)
                server.run(app)
            ```
            
## File Structure
```bash
your_project_directory/
│
├── templates/            # HTML templates
│   ├── home.html
│   ├── about.html
│   └── ...
│
├── static/               # Static files (CSS, JS, images)
│   ├── css/              # CSS files
│   │   ├── home.css
│   │   └── ...
│   ├── js/               # JavaScript files
│   │   ├── home.js
│   │   └── ...
│   └── img/              # Images
│       ├── logo.png
│       └── ...
│
└── main.py               # Main Python file to run your server