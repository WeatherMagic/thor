#!/usr/bin/env python3

import flask
import json
import os
import scipy
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


@thorApp.route('/api/<dimension>', methods=["GET", "POST"])
def api(dimension):
    # None if args not given as json
    arguments = flask.request.get_json()
    # Set arguments from URL if not from json
    if arguments is None:
        arguments = flask.request.args.to_dict(flat=False)

    # Check arguments given by client
    argCheckDict = util.argumentsHandler(arguments)
    if argCheckDict["ok"] is False:
        return json.dumps(argCheckDict)

    if dimension == "temperature":
        argCheckDict["arguments"]["dimension"] = "tas"
    elif dimension == "air-pressure":
        pass
    elif dimension == "precipitation":
        argCheckDict["arguments"]["dimension"] = "pr"
    elif dimension == "water-level":
        pass

    if "dimension" not in arguments.keys():
        return json.dumps({"ok": False,
                           "errorMessage":
                           "Client sent incorrect dimension: " + dimension})

    returnData = request.handleRequest(argCheckDict["arguments"],
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
        # Kelvin->Celsius and fit into PNG integer range (0 to 255)
        if dimension == "temperature":
            # -145 = -273 + 128
            returnData["data"] = returnData["data"] - 145
        # Return a PNG as requested by weather-front
        output = io.BytesIO()
        image = scipy.misc.toimage(returnData["data"])
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
