# Testing Microservices with Pact & K6

This is a demo project that demonstrates a means of testing a microservice in isolation from a specifically non-functional perspective. The demo includes:

- a dummy test API
- Pact contract tests
- K6 performance tests
- Dockerised execution
- TODO: CircleCI YAML

## Running without Docker

To run the API without Docker, you will first need to have `python 3` installed on your host. A quickstart guide for doing that on a variety of platforms can be found [here](https://realpython.com/installing-python/).

Once you have Python 3 installed, complete the following steps for the full demo execution.

Install the required Python 3 packages:

```
pip3 install -r requirements.txt
```

Now you have installed the packages, its time to run the API application (Note: its currently set up to run on Port 80 natively, this will probably require sudo access, I'll change this at another point).

```
python3 app.py
```

This will start the application at host 0.0.0.0 on port 80 - you will see something similar to:

```
 * Serving Flask app "app" (lazy loading)
 * Environment: production
   WARNING: Do not use the development server in a production environment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Running on http://0.0.0.0:80/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 322-254-862
```

Now you can make an `HTTP GET` request using your favourite HTTP client to the following endpoint:

```
http://0.0.0.0:80/animals/<string>

Currently available animals:
- cat
- dog
```

The dummy API will return a JSON payload with the name of the animal and the noise it makes (top quality APIs!). So, for example:

```
curl -v http://0.0.0.0:80/animal/dog
*   Trying 0.0.0.0...
* TCP_NODELAY set
* Connected to 0.0.0.0 (127.0.0.1) port 80 (#0)
> GET /animal/dog HTTP/1.1
> Host: 0.0.0.0
> User-Agent: curl/7.51.0
> Accept: */*
>
* HTTP 1.0, assume close after body
< HTTP/1.0 200 OK
< Content-Type: application/json
< Content-Length: 50
< Server: Werkzeug/0.14.1 Python/3.6.5
< Date: Tue, 07 Aug 2018 18:59:51 GMT
<
{
    "animal_name": "dog",
    "noise": "bark"
}
* Curl_http_done: called premature == 0
* Closing connection 0
```

Great - the API is now running. It's time to execute some tests against it :-)

### Running the Pact Contract Tests
Pact provides a means of validating a **Consumer's** contract with a Provider. This allows you to test that the Provider adheres to this contract on every code change or deploy. For much more information on this, visit [pact.io].

Since we installed all the required python dependencies, we should be ready to execute the tests:

```
pact-verifier --provider-base-url=http://0.0.0.0:80 ./pacts/
```

This tells the `pact-verifier` script to confirm the pacts against the live endpoint on `http://0.0.0.0:80` and look for any pact json files in `./pacts/`.

All being well, you should see the following:

```
Verifying a pact between Text to Speech Animal Consumer and Animal Noise Service
  A request to determine the noise a dog makes
    with GET /animal/dog
      returns a response which
        has status code 200
        has a matching body
  A request to determine the noise a spider makes
    with GET /animal/spider
      returns a response which
        has status code 404

2 interactions, 0 failures
```

These pact tests assume a **Consumer** of another hypothetical service that is a text to speech service that reads out the value in the Provider's `noise` attribute. As you can see, the two tests here are, does a GET request return a 200 and is the body as expected **and** if we request the noise a non-existant animal in the db makes, do we get a standard HTTP 404.

You're now successfully testing your provider that any changse are now breaking its contract with a consumer.
