#!/usr/bin/env python3

import flask
import json
import os
import scipy
import numpy as np
import io
import thor.util as util
import thor.request as request
import thor.const as const
import PIL


thorApp = flask.Flask("thor")


@thorApp.route('/')
def hello_world():
    # Redirect to description of API
    return flask.redirect(
            "https://github.com/WeatherMagic/thor/blob/master/doc/API.md",
            code=302)


@thorApp.route('/api/<variable>', methods=["GET", "POST"])
def api(variable):
    # None if args not given as json
    arguments = flask.request.get_json()
    # Set arguments from URL if not from json
    if arguments is None:
        arguments = flask.request.args.to_dict(flat=False)
        # Some way every argument is nested in list
        # Remove this somehow
        for arg, value in arguments.items():
            arguments[arg] = value[0]

    # Check arguments given by client
    argCheckDict = util.argumentsHandler(arguments)
    if argCheckDict["ok"] is False:
        return json.dumps(argCheckDict)

    if variable == "temperature":
        argCheckDict["variable"] = "tas"
    elif variable == "air-pressure":
        pass
    elif variable == "precipitation":
        argCheckDict["variable"] = "pr"
    elif variable == "water-level":
        pass

    if "variable" not in argCheckDict.keys():
        return json.dumps({"ok": False,
                           "errorMessage":
                           "Client sent incorrect variable: " + variable})

    returnData = request.handleRequest(argCheckDict,
                                       const.ncFiles,
                                       const.log)

    if not returnData["ok"]:
        # Error message returned
        return json.dumps(returnData)
    elif len(returnData["data"].shape) != 2:
        # If OK but not 2D weather-front doesn't want it
        # We still think this is applicable so we will return this
        returnData["ok"] = False
        returnData["data"] = returnData["data"].tolist()
        return json.dumps(returnData)
    else:
        # Convert data to integer range.
        returnData["data"]\
                = util.convertToPNGRange(returnData["data"], variable)
        # Return a PNG as requested by weather-front
        output = io.BytesIO()
        image = PIL.Image.fromarray(returnData["data"], "LA")
        # Flip since top left corner is 0,0 in image
        image = image.transpose(PIL.Image.FLIP_TOP_BOTTOM)
        image.save(output, 'PNG')
        output.seek(0)
        return flask.send_file(
                    output,
                    attachment_filename="climate.png",
                    mimetype="image/png",
                    as_attachment=True
                         )
