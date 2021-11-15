from flask.helpers import make_response
import requests
import json
from flask import Flask
from flask import render_template
from addict import Dict
import re

app = Flask(__name__)

# TODO could be configurable thru env vars
API_KEY="TODO...YOUR...KEY...kazxn"
API_SECRET_KEY="TODO...YOUR...SECRET..hqumn"

base_url = 'https://api.redislabs.com/v1/'
headers = {"x-api-key": API_KEY, "x-api-secret-key": API_SECRET_KEY,
           'Content-type':'application/json', 'Accept':'application/json'}

CLOUD = Dict()

# for testing purpose
# simulates an answer from the Redis Enterprise Cloud prometheus endpoint (port 8070 on internal cluster adress)
@app.route('/8070')
def prometheus():
    resp = make_response(render_template('prometheus8070.txt'))
    resp.headers['Content-type'] = 'text/plain'
    return resp

# get cloud subscription/db names from Redis Enterprise Cloud API using the API key
def dbname():
    print("Caling Redis Cloud API")

    cloud = Dict()

    response = requests.get(base_url + 'subscriptions', headers=headers)
    if (response.status_code != 200):
        print(f"ERROR Redis Cloud API code {response.status_code}")
        print(response.content)
        return cloud # empty {}

    subdict = json.loads(response.content.decode())

    #cloud.subscription.ID = subscriptionName
    #cloud.db.ID = subscriptionName/DBName
    #cloud.cluster.clusterHostName = subscriptionName

    for thissub in subdict['subscriptions']:
        print("account: {}".format(subdict['accountId']))
        print("subscription id: {}  name: {}".format(thissub['id'], thissub['name']))
        cloud.subscription[thissub['id']] = thissub['name']

    for subsid in cloud.subscription.keys():
        response = requests.get(base_url + f"subscriptions/{subsid}/databases", headers=headers)
        dbs = json.loads(response.content.decode())
        for db in dbs['subscription'][0]['databases']:
            cluster = re.search(".*\.internal\.(.*):[0-9]+", db['privateEndpoint']).group(1)
            print(f"subscription id: {subsid} database {db['databaseId']} name {db['name']} cluster {cluster}")
            cloud.db[db['databaseId']] = db['name']
            cloud.dbl[db['databaseId']] = cloud.subscription[subsid] + "/" + db['name']
            cloud.cluster[cluster] = cloud.subscription[subsid]

    return cloud

# refresh cloud subscription/db names
@app.route('/refresh')
def refresh():
    global CLOUD
    CLOUD = dbname()
    return CLOUD

# read cloud subscription/db names as JSON for diagnostic
@app.route('/cloud')
def cloud():
    return CLOUD

# main endpoint to use that reverse proxy the destination cluster prometheus endpoint
# and substitute ids with names
@app.route("/proxy")
def proxy():
    response = requests.get("http://localhost:5000/8070") ## TODO change or make configurable (eg from URI /proxy/<clusterDNSinternalname> )
    data  = response.content.decode()
    for dbid in CLOUD.dbl.keys():
        data = data.replace(f"bdb=\"{dbid}\"", f"bdb=\"{CLOUD.dbl[dbid]}\"")
        data = data.replace(f"endpoint=\"{dbid}:", f"endpoint=\"{CLOUD.dbl[dbid]}:")
        data = data.replace(f"proxy=\"{dbid}:", f"proxy=\"{CLOUD.dbl[dbid]}:")
    for cluster in CLOUD.cluster.keys():
        data = data.replace(f"cluster=\"{cluster}\"", f"cluster=\"{CLOUD.cluster[cluster]}\"")

    resp = make_response(data)
    resp.headers['Content-type'] = 'text/plain'
    return resp


# curl -X GET https://internal.c16664.eu-west1-2.gcp.cloud.rlrcp.com:8070/ -s -k -L
if __name__ == '__main__':
    CLOUD = dbname()
    app.run(debug=True, threaded=True) #TODO remove debug=True

