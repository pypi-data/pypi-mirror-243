# Test App

from flask import Flask
from lightflask import LightFlask


app = Flask(__name__)

lightflask = LightFlask(app)
lightflask.dir = 'public'

@lightflask.route('/', 'index.md')
def index():
    return lightflask.get_content('index.md')

lightflask.register_routes()
app.run(debug=True)