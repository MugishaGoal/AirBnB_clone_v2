#!/usr/bin/python3
'''A Flask web application with three routes'''
from flask import Flask

app = Flask(__name__)
'''A Flask application instance'''


@app.route("/", strict_slashes=False)
def hello_hbnb():
    '''Route to display "Hello HBNB!"'''
    return "Hello HBNB!"


@app.route("/hbnb", strict_slashes=False)
def hbnb():
    '''Route to display "HBNB"'''
    return "HBNB"


@app.route("/c/<text>", strict_slashes=False)
def c_route(text):
    '''Route to display "C " followed by the value of the text variable'''
    return "C {}".format(text.replace("_", " "))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
