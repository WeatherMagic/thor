#!/usr/bin/env python3

from flask import Flask
thor = Flask(__name__)

@thor.route('/')
def hello_world():
    return 'Hello, World!'

