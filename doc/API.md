# Thor HTTP API

This document outlines the Thor Web API.

## URL-scheme

The URL-scheme are as follows:

```
/api/dimension/zoom-level/long/lat/year
/api/dimension/zoom-level/long/lat/year/month
```

Where the two schemes gives different resolution on data. The first returns interpolated data for every month, with extreme values for that month. The second URL scheme returns data points for every day during specified month. 

** ''dimension'' is one of the following: **

- temperature
- air-pressure
- precipitation
- water-level

**Zoom level is one of a predefined set of zoom levels, these are not yet specified.**

All methods must be called using HTTP(S). Arguments can be passed as GET or POST params, or a mix.

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

