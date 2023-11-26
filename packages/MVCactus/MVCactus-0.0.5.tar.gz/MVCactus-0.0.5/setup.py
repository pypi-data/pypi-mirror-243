from setuptools import setup, find_packages
from MVCactus.__init__ import __version__


VERSION = __version__
DESCRIPTION = 'MVCactus is a micro-framework for building simple and efficient web applications. It leverages the standard HTTP server capabilities of Python to provide a straightforward environment for web development. MVCactus is ideal for small-scale projects, educational purposes, and rapid prototyping, offering a minimalistic approach to web server architecture with support for dynamic template rendering and static file serving.'
LONG_DESCRIPTION = '''
# MVCactus

## Description

MVCactus is a micro-framework designed for building simple and efficient web applications. Utilizing Python's standard HTTP server capabilities, MVCactus is an ideal choice for small-scale projects, educational purposes, and rapid prototyping. It offers a minimalist approach to web server architecture, supporting dynamic template rendering and static file serving.

## Key Features

- **Easy Routing**: Define routes with simple decorators for GET and POST requests.
- **Dynamic Template Rendering**: Integrated with the Placeholdr templating engine for dynamic content rendering within HTML templates.
- **Static File Serving**: Built-in support for serving CSS, JavaScript, and image files from a `static` directory.
- **Custom Error Handling**: Define responses for various HTTP statuses.
- **Flexible and User-friendly**: Ideal for small to medium-sized web projects and educational environments.

## For More Information
Please refer to the [documentation](https://github.com/Dcohen52/MVCactus/blob/main/DOCS.md) for more information on how to use MVCactus.

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/Dcohen52/MVCactus/blob/main/LICENSE) file for details.
'''

# Setting up
setup(
    name="MVCactus",
    version=VERSION,
    author="Dekel Cohen",
    author_email="<dcohen52@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],  # List your project dependencies here
    keywords=['python', 'web server', 'MVCactus', 'HTTP server', 'framework', 'simple web applications',
              'web development', 'lightweight server', 'educational', 'template rendering', 'static file serving'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
