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

- zoom-level
- fromLongitude
- toLongitude
- fromLatitude
- toLatitude
- year
- month (optional)

If month is omitted, data returned will be as filtered over a month. If month is specified, data points for each day will be returned. 

**Zoom level is one of a predefined set of zoom levels, it can be any rational value between 1 and a 100**

1 returns every data point that the server has in the area requested.

100 returns four data point in the area requested.

All methods must be called using HTTP(S). Arguments can be passed as GET or POST params, or a mix.

### Example

```
{
	"year": "2012",
	"month": "12",
	"fromLongitude": "1",
	"toLongitude": "5",
	"fromLatitude": "37",
	"toLatitude": "45",
	"zoom-level": "1"
}
```


## Response

The response contains a JSON object, which at the top level contains a boolean value indicating success status. A non successful request will contain an error message. 

Example of successful request:

```json
{
    "ok": true
    "other-stuff": [All the goodie simulations here]
}
```

Example of a non successful request: 

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

