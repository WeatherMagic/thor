#!/usr/bin/env python3

from flask import Flask, request
import json

thorApp = Flask("thor")

@thorApp.route('/')
def hello_world():
    return 'Hello, World!'

@thorApp.route('/api/<dimension>', methods=["GET", "POST"])
def api(dimension):
    # None if args not given as json
    arguments = request.get_json()
    # Set arguments from URL
    if arguments == None:
        arguments = request.args.to_dict(flat=False)

    if dimension == "temperature":
        pass
    elif dimension == "air-pressure":
        pass
    elif dimension == "precipitation":
        pass
    elif dimension == "water-level":
        pass
    else:
        return json.dumps({"ok": False, "error": "Client sent incorrect dimension: " + dimension})
