from flask import Flask, render_template, abort, Response
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def main():
    app.debug = True
    app.run(port=5001, threaded=False)
