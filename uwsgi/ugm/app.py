
from flask import Flask
app = Flask(__name__)
@app.route('/')
def mai_page():
    return "<center><h1>HELLO</h1></center>"

