from app import app

@app.route('/')
@app.route('/index')
def index():
    return "<center><h1>HELLO</h1></center>"