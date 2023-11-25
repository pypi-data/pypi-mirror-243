# LightFlask Markdown Router

LightFlask Markdown Router is a tool that allows you to easily integrate Markdown files into Flask applications. Users can create dynamic content by linking Markdown files to specific URLs.

## Installation

Before starting your project, run the following command in the terminal or command prompt to install the required packages:

```bash
pip install lightflask
```

## Usage
Add LightFlask to your main file (app.py or similar) as follows:

```python
from flask import Flask, render_template
from lightflask import LightFlask

app = Flask(__name__)
lightflask = LightFlask(app)

@lightflask.route('/', 'index.md')
def markdown1():
    return lightflask.get_content('index.md')

lightflask.register_routes()

if __name__ == '__main__':
    app.run(debug=True)

```

In the example above, the /markdown1 URL is linked to the markdown1.md Markdown file.

## Contributing
Your contribution is welcome! Please fork the project, add improvements, and submit pull requests.

## License
This project is licensed under the MIT License. For more information, see the [LICENSE](LICENSE) file.
