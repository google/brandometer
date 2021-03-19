from flask import Flask
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config['SECRET_KEY']='supersecretkey'
Bootstrap(app)

from . import forms
from . import routes
