from os import path

from flask import Flask

config = {
    "template_folder": path.abspath("resources/templates"),
    "static_folder": path.abspath("resources/static"),
}

app = Flask(__name__, **config)
