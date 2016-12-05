# Thor HTTP API

This document outlines the Thor Web API.

## URL-scheme

The URL-scheme are as follows:

```
/api/variable
```

Returned data variable and dimensionality is decided by in-arguments given by the client. 

** ''variable'' is one of the following: **

- temperature
- air-pressure
- precipitation
- water-level


Each request needs to provide parameters either in URL or as a json (OBS: Set the HTTP header "Content-type" to "application/json") data object: 

- from-year
- from-month
- return-dimension
- from-longitude
- to-longitude
- from-latitude
- to-latitude

If month is omitted, data returned will be as filtered over a month. If month is specified, data points for each day will be returned. 

Return-dimension is a 2-element list that should contatin integers telling how many steps in each direction to return [ lat-dimension, long-dimension].

All methods must be called using HTTP(S). Arguments can be passed as GET or POST params.

### Example

```
{
	"from-year": "2082",
	"from-month": "6",
	"from-longitude": "1",
	"to-longitude": "5",
	"from-latitude": "37",
	"to-latitude": "45",
	"return-dimension": [4,3]
}
```
### Optional arguments
Several arguments can be added to the request in order to get more control over what data is recived.

- from-year
- to-year
- to-month 
- climate-model
- exhaust-level

### Example with optional arguments

```
{
	"from-year": "2082",
	"from-month": 3,
	"to-year": 2083,
	"to-month": 4,
	"from-longitude": "33",
	"to-longitude": "34",
	"from-latitude": "27",
	"to-latitude": "28",
	"return-dimension": [2,10,20],
	"climate-model": "MOHC-HadGEM2-ES",
	"exhaust-level": "rcp85"
}
```

## Response

If the requested data contains 2 dimensions, the response is a PNG image containing the data. Otherwise the response contains a JSON object, which at the top level contains a boolean value indicating success status. A non successful request will contain an error message. 

**Example of a non successful response:** 

```
{
    "ok": false
    "error": "ERROR MESSAGE"
}
```

### Temperature

Temperature returned as a PNG image is clamped to 0-255 integer range since limited by PNG integer range. The temperature is centered with 0 around 128, and the total temperature range is -63 to 62 degrees celcius. This means that each step in the PNG integer range represents half a degree Celius/Kelvin. Formula for getting temperature in Celcius from a pixel value in returned image is as follows.

```
celcius = (pixel_value + 128) / 2.0 # FLOAT!
```

If a data point is equal to 

### Percipitation

Percipitation returned as a PNG image is clamped to 0-255 integer range since limited by PNG integer range. The total percipitation range is 0 to 62 mm/day. This means that each step in the PNG integer range represents 0,25 mm/day of rain. Formula for getting percipitation in Celcius from a pixel value in returned image is as follows.

```
mm/day = pixel_value / 4.0 # FLOAT!
```



For more specific information on each function, please see the respective functions:

- [temperature](temperature.md)
- [air-pressure](air-pressure.md)
- [precipitation](precipitation.md)
- [water-level](water-level.md)

