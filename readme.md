# Septic system API
This API will accept an address and return `{"septic": "yes"}` if the property at the given address has a septic system, `{"septic": "no"}` if it does not, `{"septic": "unknown"}` if we cannot tell, and `{"error": error message}` on an error returned from the underlying property information API.

## Installation 
I only have a Linux PC at home, but these instruction should work on MacOS (I hope).
1. `git clone https://github.com/blauser/toy-api.git`
1. `cd toy-api/`
1. `python -m venv .venv`
1. `source .venv/bin/activate`
1. `pip install -r requirements.txt`

## Usage
Start the local server with `python -m propsapi`.

This is running the default local Flask server at `http://127.0.0.1:5000`, with API version `v0`, and the API endpoint is `/props`. Therefore, the sole endpoint is access via `http://127.0.0.1:5000/v0/props?address=address_string`.

Given this is toy API, and not connected to a live valid source of information, the type of sewer system is determined by words appearing the address string.
- `"septic"` will yield a response of `yes`
- `"error"` will yield a generic error response
- `"noinfo"` will yield an error response corresponding to no information being available from the HouseCanary API (i.e. api return code `204`)  
- `"unknown"` or `"null"` will yield a response of `unknown`
- anything else will yield a response of `no`

### Examples of use
- `curl http://127.0.0.1:5000/v0/props?address=123+septic+st+90210` will yield 
  ```
  {"props": {
    "api_result": "success",
    "sewer": "yes"
    }
  }
  ```
- `curl http://127.0.0.1:5000/v0/props?address=123+main+st+90210` will yield 
  ```
  {"props": {
    "api_result": "success",
    "sewer": "no"
    }
  }
  ```
- `curl http://127.0.0.1:5000/v0/props?address=123+null+ave+90210` will yield 
  ```
  {"props": {
    "api_result": "success",
    "sewer": "unknown"
    }
  }
  ```
- `curl http://127.0.0.1:5000/v0/props?address=unknown+rd+90210` will yield 
  ```
  {"props": {
    "api_result": "success",
    "sewer": "unknown"
    }
  }
  ```
- `curl http://127.0.0.1:5000/v0/props?address=123+error+st+90210` will yield 
  ```
  {"props": {
    "api_result": "error",
    "error": "error in source"
    }
  }
  ```
- `curl http://127.0.0.1:5000/v0/props?address=345+noinfo+blvd+90210` will yield 
  ```
  {"props": {
    "api_result": "error",
    "error": "no content"
    }
  }
  ```

## Dependencies
As I mentioned before, we're using Flask, so we need the following.
- `flask`
- `flask-restful`

Also, we are using the official HouseCanary API python client, `housecanary`.

However, since we do not have an API key for the HouseCanary API, we will mock its responses with `requests-mock`.

## Improvements
There is much I would improve and expand, and I hope we can discuss it at length. 
- Although I'm using the [HouseCanary Python API client](https://github.com/housecanary/hc-api-python), its responses are mocked. With valid API credentials, the mocking would be moved the testing functions.
- I would imagine you have some sort of address validator (I assume it would 3rd party), which I would make use of before trying to send an API request to HouseCanary.
- The API could easily be extended in a few ways depending on the needs of the client.
  - We can add a parameter to get other pieces of property data (e.g. `props?address=123+fake+st+90210&detail=basement`).
  - We can add a parameter to specify a source API (e.g. `props?address=123+fake+st+90210&detail=septic&source=housecanary`).
- We should add authentication and rate limiting before deploying an API such as this.
