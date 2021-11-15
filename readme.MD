# Redis Enterprise Cloud Prometheus by Name

## About

A reverse proxy for Redis Enteprise Cloud Prometheus cluster endpoint that substitute ID to name.

The names are looked up in Redis Enterprise Cloud API.

This ensures cluster/subscription and DB rebuilt are staying with stable names while having changing ID, which then ensures Grafana metrics stay stable.


## Doc

![architecture](doc/image001.png?raw=true)

## URL
See source
- /cloud (returns the ID / name dictionary as JSON per last refresh - can be empty)
- /refresh (will call Redis Enteprise Cloud API)
- /proxy (the substituted Prometheus scrapping endpoint)
- /8070 (for testing)


# How to run

The project provides also a Prometheus and Grafana server for local testing
(See Redis Enterprise docs)

## Locally

run app.py in VScode

http://localhost:5000/cloud
http://localhost:5000/refresh
http://localhost:5000/proxy

## As Docker compose

docker compose build
docker compose up


http://localhost:8070/8070
http://localhost:8070/cloud
http://localhost:8070/refresh
http://localhost:8070/cloud
http://localhost:8070/proxy


# Other Notes

https://api.redislabs.com/v1/swagger-ui.html#/Databases/getSubscriptionDatabasesUsingGET

(Note the need to follow redirects)
curl -X GET https://internal.c16664.eu-west1-2.gcp.cloud.rlrcp.com:8070/ -s -k -L

http://localhost:9090/graph?g0.expr=redis_evicted_keys&g0.tab=1&g0.stacked=0&g0.show_exemplars=0&g0.range_input=1h

http://localhost:3000/
admin / secret



