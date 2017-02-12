import json
import os

from flask import Flask
from flask import make_response
from flask import request

from Factories.DropletParser import DropletParser
from services.DOService import DOService

app = Flask(__name__)
doService = DOService('https://api.digitalocean.com/v2', os.getenv('DO_TOKEN', "RANDOM_TOKEN"))


def get_droplets_info():
    droplets = doService.get('/droplets')
    droplets = DropletParser().parse(droplets.get('droplets'))
    k = "".join([droplet.get_info() for droplet in droplets])
    return make_response(k)


@app.route('/')
def hello_world():
    r = get_droplets_info()
    r.headers['Content-Type'] = 'application/json'
    return r


@app.route('/webhook', methods=['POST'])
def web_hook():
    req = request.get_json(silent=True, force=True)
    print json.dumps(req, indent=2)
    result = process_request(req)
    res = make_api_ai_response(result)
    res = json.dumps(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def process_request(ai_request):
    action = ai_request.get('result').get('action')
    if action == "do.status":
        parameters = ai_request.get('result').get('parameters')
        server = parameters.get('server')
        return "Hey If you are getting this message means that your " + server + " is up"
    elif action == "do:list":
        parameters = ai_request.get('result').get('parameters')
        entity = parameters.get('DOEntities')
        if entity == "droplet":
            r = get_droplets_info()
            r.headers['Content-Type'] = 'application/json'
            return r
    else:
        return "Hey sorry I am dumb, I can't understand complex words"


def make_api_ai_response(message):
    return {
        "speech": message,
        "displayText": message,
        "source": "test-app"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')
