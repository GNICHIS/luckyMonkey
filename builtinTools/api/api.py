from flask import Flask, render_template
import base64

#config part
#define the emplacement of database files (the JSON files)

app = Flask(__name__)

@app.route('/api/')
def api():
    return "api"

if __name__ == '__main__':
   app.run()