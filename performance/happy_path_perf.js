import { check, group, sleep } from "k6";
import http from "k6/http";

export let options = {
    vus: 5,
    iterations: 2000
};

// Scenarios
export default function() {

    group ("single_api_call", function() {
        let res = http.get("http://localhost:1200/animal/dog");
        check(res, {
        "is status 200": (r) => r.status === 200,
        "response time is < 100ms": (r) => r.timings.duration < 100
        });
    });
}