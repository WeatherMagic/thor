#!/usr/bin/env python3

from flask import Flask, request, g
import json,os
import thor.init,thor.temperature
import thor.const as const


thorApp = Flask("thor")

@thorApp.route('/')
def hello_world():
    return 'Hello, World!'


@thorApp.route('/api/<dimension>', methods=["GET", "POST"])
def api(dimension):
    # None if args not given as json
    arguments = request.get_json()
    # Set arguments from URL if not from json
    if arguments is None:
        arguments = request.args.to_dict(flat=False)

    if dimension == "temperature":
        return thor.temperature.handleRequest(arguments, const.ncFiles, const.log)
    elif dimension == "air-pressure":
        pass
    elif dimension == "precipitation":
        pass
    elif dimension == "water-level":
        pass
    else:
        return json.dumps({"ok": False,
                           "error":
                           "Client sent incorrect dimension: " + dimension})
