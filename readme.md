# Septic system API
This API will accept an address and return `{"septic": "yes"}` if the property at the given address has a septic system, `{"septic": "no"}` if it does not, `{"septic": "unknown"}` if we cannot tell, and `{"error": error message}` on an error returned from the property information API.

## Usage
This is running the default local Flask server at `http://127.0.0.1:5000`, the API path is `/props`. Given this is toy API, and not connected to a live valid source of information, the type of sewer system is determined by words appearing the address string.
- `"septic"` will yield a response of `yes`
- `"error"` will yield an error response
- `"unknown"` or `"null"` will yield a response of `unknown`
- anything else will yield a response of `no`

### Examples of use
- `curl http://127.0.0.1:5000/props/address=123+septic+st+90210` will yield `{"septic": "yes"}`
- `curl http://127.0.0.1:5000/props/address=123+main+st+90210` will yield `{"septic": "no"}`
- `curl http://127.0.0.1:5000/props/address=123+null+ave+90210` will yield `{"septic": "unknown"}`
- `curl http://127.0.0.1:5000/props/address=unknown+rd+90210` will yield `{"septic": "unknown"}`
- `curl http://127.0.0.1:5000/props/address=123+error+st+90210` will yield `{"error": "error in source"}`

## Dependencies
As I mentioned before, we're using Flask, so we need
- `flask`
- `flask-restful`

## Improvements
There is much I would improve and expand, and I hope we can discuss it at length. 
- I would use the extant [HouseCanary Python API client](https://github.com/housecanary/hc-api-python) to get valid source data.
- I would imagine you have some sort of address validator (I assume it would 3rd party), which I would make use of before trying to send an API request to HouseCanary.
- The API could easily be extended in a few ways depending on the needs of the client.
  - We can add a parameter to get other pieces of property data (e.g. `props/address=123+fake+st+90210&detail=basement`).
  - We can add a parameter to specify a source API (e.g. `props/address=123+fake+st+90210&detail=septic&source=housecanary`).
  - We should add authentication and rate limiting before deploying an API such as this.
- I used Flask because it was more light-weight than Django, but I know you're a Django shop. I would rewrite this in Django with extra time.
- I would also go back to add more testing coverage and documentation.
