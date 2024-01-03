#!/usr/bin/python3
'''A Flask web application with multiple routes and templates'''
from flask import Flask, render_template


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
    '''Route to display "C ", followed by the value of the text variable'''
    return "C {}".format(text.replace("_", " "))


@app.route("/python/", defaults={'text': 'is cool'}, strict_slashes=False)
@app.route("/python/<text>", strict_slashes=False)
def python_route(text):
    '''Route to display "Python",followed by the value of the text variable'''
    return "Python {}".format(text.replace("_", " "))


@app.route("/number/<int:n>", strict_slashes=False)
def number_route(n):
    '''Route to display "n is a number" only if n is an integer'''
    return "{} is a number".format(n)


@app.route("/number_template/<int:n>", strict_slashes=False)
def number_template_route(n):
    '''Route to display an HTML page with H1 tag "Number: n"
       only if n is an integer
    '''
    return render_template('5-number.html', n=n)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
