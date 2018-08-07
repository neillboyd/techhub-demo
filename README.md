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

### Running the K6 Performance Tests

You may also want to monitor your microservice for changes that impact the performance of your service. This can be achieved using a Go based performance test tool called **K6**. You can find out more about K6 at [k6.io].

The test files for K6 are written in `Javascript` so it assumes some JS knowledge.

The test in this example repo assumes a performance test on the API that:

- Performance tests only the happy path
- Ensures a 200 OK is returned
- Each response is returned within 100ms
- Assumes 5 concurrent users
- A total of 2000 iterations will be executed across the 5 users.

This is a scenario plucked out of thin air, you will obviously want to tailor your tests towards a real life scenario.

To execute the K6 tests, you will need to install the K6 binaries. Again, a handy guide for doing this across all platforms can be found [here](https://docs.k6.io/docs/installation)

Once installed, you will just need to tell K6 where to execute the tests against and which test file to run. The K6 script int his case uses *environment varialbes* to set the endpoint, so you will need to set these in your local environment, such as:

```
export API_HOST=0.0.0.0
export API_PORT=80
```

Once this is done, you can execute the script like:

```
k6 run /performance/happy_path_test.js
```

You will see the tests starting to run **assuming that the API is live on the stated host and port**. Once completed, you will see a result like:

```
    █ single_api_call

      ✓ is status 200
      ✓ response time is < 100ms

    checks.....................: 100.00% ✓ 4000 ✗ 0
    data_received..............: 392 kB  104 kB/s
    data_sent..................: 174 kB  46 kB/s
    group_duration.............: avg=9.35ms   min=4.46ms   med=8.45ms   max=83.04ms p(90)=12.01ms  p(95)=14.07ms
    http_req_blocked...........: avg=285.35µs min=138.84µs med=255.82µs max=2.81ms  p(90)=353.49µs p(95)=460.25µs
    http_req_connecting........: avg=207.58µs min=96.27µs  med=183.3µs  max=2.71ms  p(90)=257.77µs p(95)=327.45µs
    http_req_duration..........: avg=8.89ms   min=3.48ms   med=8.01ms   max=82.45ms p(90)=11.54ms  p(95)=13.38ms
    http_req_receiving.........: avg=410.61µs min=48.17µs  med=259.69µs max=9.51ms  p(90)=1.03ms   p(95)=1.37ms
    http_req_sending...........: avg=70.88µs  min=29.56µs  med=58.9µs   max=2.6ms   p(90)=90.1µs   p(95)=112.27µs
    http_req_tls_handshaking...: avg=0s       min=0s       med=0s       max=0s      p(90)=0s       p(95)=0s
    http_req_waiting...........: avg=8.41ms   min=2.56ms   med=7.56ms   max=79.2ms  p(90)=10.93ms  p(95)=12.89ms
    http_reqs..................: 2000    531.769624/s
    iteration_duration.........: avg=9.37ms   min=4.49ms   med=8.47ms   max=83.05ms p(90)=12.04ms  p(95)=14.1ms
    iterations.................: 2000    531.769624/s
    vus........................: 5       min=5  max=5
    vus_max....................: 5       min=5  max=5
```

Congratulations - you've now successfully executed some lightweight service-level performance tests against your microservice. You can do all sorts of cool things with this such as only deploy if a certain number of requests meet a given threshold, or a % difference between runs or set a hard limit, such as 100ms per response. It's up to you and your Ops team.

## Running With Docker
TODO
  
