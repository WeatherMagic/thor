# Thor HTTP API

This document outlines the Thor Web API.

## URL-scheme

The URL-scheme are as follows:

```
/api/<variable>
```

Returned data variable and dimensionality is decided by in-arguments given by the client. 

** ''variable'' is one of the following: **

- temperature
- precipitation
[//]: # (- air-pressure)

Each request needs to provide parameters either in URL or as a json (OBS: Set the HTTP header "Content-type" to "application/json") data object: 

 - year                 (int)
 - month                (int)
 - from-longitude       (float)
 - to-longitude         (float)
 - from-latitude        (float)
 - to-latitude          (float)
 - exhaust-level        (int)
 - climate-model        (int)
 - height-resolution    (int)

All methods must be called using HTTP(S). Arguments can be passed as GET or POST params, either in URL or as "Content-Type: application/json"when doing a POST.

### Example

```
{
	"year": "2083",
	"month": 1,
	"from-longitude": "-180",
	"to-longitude": "180",
  	"from-latitude": "-80",
	"to-latitude": "80",
	"exhaust-level": "rcp45",
	"climate-model": "CNRM-CERFACS-CNRM-CM5",
    "height-resolution": 1024
}
```

## Response

If the result is successful, the response is a PNG image containing the data. in the event of a non-successfull request the response contains a JSON object, which at the top level contains a boolean value indicating success status as well as an error message. 

**Example of a non successful response:** 

```
{
    "ok": false
    "error": "ERROR MESSAGE"
}
```

### Temperature

Temperature returned as a PNG image is clamped to 0-255 integer range since limited by PNG integer range. The temperature is centered with 0 around 128, and the total temperature range is -64 to 63 degrees celcius. This means that each step in the PNG integer range represents half a degree Celius/Kelvin. Formula for getting temperature in Celcius from a pixel value in returned image is as follows.

```
celcius = (pixel_value - 128) / 2.0 # FLOAT!
```

### Percipitation

Percipitation returned as a PNG image is clamped to 0-255 integer range since limited by PNG integer range. The total precipitation range is 0 to 62 mm/day. This means that each step in the PNG integer range represents 0,25 mm/day of rain. Formula for getting precipitation in Celcius from a pixel value in returned image is as follows.

```
mm/day = pixel_value / 4.0 # FLOAT!
```

## Finding available climate models

It is possible to ask the server for available data. To do this, send a GET or POST request to:

```
/api/<variable>
```

This will return a json with something like this: 

```
{
	"exhaust-levels": [
		"rcp45",
		"rcp85"
	],
	"models": [
		"ICHEC-EC-EARTH",
		"CNRM-CERFACS-CNRM-CM5",
		"IPSL-IPSL-CM5A-MR"
	],
	"ok": true,
	"domains": [
		"NAM-44i",
		"CAM-44i",
		"EUR-11i",
		"WAS-44i",
		"EUR-44i",
		"MNA-22i",
		"AFR-44i",
		"SAM-44i",
		"ARC-44i",
		"MNA-44i"
	]
}
```

It is also possible for the server to return the entire internal tree structure of the server by setting the argument "with-tree". This is however very taxing for the server and will give a much longer response time (seconds!). 

