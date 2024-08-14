import sys
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def hello():
    return render_template('index.html')

@app.route("/view")
def view():
    return render_template('view.html')

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8210)