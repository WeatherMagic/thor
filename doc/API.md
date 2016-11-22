# Thor HTTP API

This document outlines the Thor Web API.

## URL-scheme

The URL-scheme are as follows:

```
/api/dimension
```

Where the two schemes gives different resolution on data. The first returns interpolated data for every month, with extreme values for that month. The second URL scheme returns data points for every day during specified month. 

** ''dimension'' is one of the following: **

- temperature
- air-pressure
- precipitation
- water-level


Each request needs to provide parameters either in URL or as a json (OBS: Set the HTTP header "Content-type" to "application/json") data object: 

- return-dimension
- from-longitude
- to-longitude
- from-latitude
- to-latitude

If month is omitted, data returned will be as filtered over a month. If month is specified, data points for each day will be returned. 

Return-dimension is a 3D dimensional list that should contatin integers telling how many steps in each direction to return [time-dimension, lat-dimension, long-dimension]. If the user is only intrested in 2d data then the time-dimension can omitted and return-dimension will be [lat-dimension, long-dimension].

All methods must be called using HTTP(S). Arguments can be passed as GET or POST params, or a mix.

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
- from-month 
- to-month 
- domain
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
	"domain": "EUR-11",
	"climate-model": "MOHC-HadGEM2-ES",
	"exhaust-level": "rcp85"
}
```

## Response

The response contains a JSON object, which at the top level contains a boolean value indicating success status. A non successful request will contain an error message. 

**Example of successful request:**

```json
{
    "ok": true
    "data": [All the goodie simulations here]
}
```

The returned data is three dimensional with the dimensions time, y and x (IN THAT ORDER). There's `12.231 km` between data points in each spatial direction when using zoom-level 1. The time resolution is one month.

**Example of a non successful request:** 

```
{
    "ok": false
    "error": "ERROR MESSAGE"
}
```

For more specific information on each function, please see the respective functions:

- [temperature](temperature.md)
- [air-pressure](air-pressure.md)
- [precipitation](precipitation.md)
- [water-level](water-level.md)

