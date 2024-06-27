# Performance testing the Sri Lanka implementation

## Setup details

The performance runnner makes use of K6 with a custom extensions for fake data generation

To include additional extensions, make use of the below resources to build your desired binary

Create a new Binary with addition extensions support
* https://k6.io/docs/extensions/guides/build-a-k6-binary-using-docker/
* https://k6.io/docs/extensions/
* Faker:
    * https://github.com/szkiba/xk6-faker
    * https://ivan.szkiba.hu/xk6-faker/index.html

Example:
```
docker run --rm -u "$(id -u):$(id -g)" -v "${PWD}:/xk6" grafana/xk6 build --with github.com/szkiba/xk6-faker
```

## Run a specific performance test

Various types of performance testing can be implemented to verify different aspects of the system. An example guide can be found [here](https://grafana.com/docs/k6/latest/testing-guides/test-types/)

#### Volume test

Ensure the systems are all connected and responding as intended

```
./k6 run scripts/smoke.js
```

#### Volume test

Run a set amount of interations under a set amount of VUs as fast as possible

```
./k6 run scripts/volume.js
```

#### Load test

Run the sytem under load by ramping up the amount of VUs and keeping this load for a given period before ramping down

```
./k6 run scripts/load.js
```
