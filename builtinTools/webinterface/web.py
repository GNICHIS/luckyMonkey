from flask import Flask, render_template

def easyReadContent(file):
    f = open(file, "r")
    return f.read()

app = Flask(__name__)

@app.route('/')
def index():
    return easyReadContent("www/index.html")

@app.route('/main.js')
def index():
    return easyReadContent("www/main.js")

@app.route('/main.css')
def index():
    return easyReadContent("www/main.css")

@app.route('/api/')
def api():
    return "api"

if __name__ == '__main__':
   app.run()