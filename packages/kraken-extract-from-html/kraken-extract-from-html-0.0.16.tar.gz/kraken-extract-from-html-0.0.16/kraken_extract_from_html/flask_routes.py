from kraken_extract_from_html import kraken_extract_from_html as k
import os
from flask import Flask
from flask import request
from flask import Response
from flask import redirect
from flask import url_for
from flask import jsonify

from flask_cors import CORS

import datetime
import time
import uuid
import random
import json
import markdown
import requests
from kraken_thing import Thing, Things
ASSET_ID = 'f83225cf-541c-379b-a6bd-b337d1139f6e'
LOG_URL = 'https://apidata.tactik8.repl.co/logs'
LOG_URL = 'https://data.krknapi.com/logs'


# Initalize app
test_mode = False


# Initialize flask app
app = Flask(__name__,
            static_url_path='',
            static_folder='static',
            template_folder='templates')
app.secret_key = b'_5#mn"F4Q8z\n\xec]/'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
CORS(app)
LOG_URL = 'https://data.krknapi.com/logs'

    
@app.route('/', methods=['GET'])
def main_get():
    """Process get data
    """

    # Accept and process url parameter
    url = request.args.get('url')
    contentUrl = request.args.get('contentUrl')

    
    if url:
        return jsonify(k.kraken_extract_from_url(url, contentUrl))
        

    # Shows instructions
    with open('README.md') as f:
        md_content = f.read()

    html_content = markdown.markdown(md_content)

    return Response(html_content)


@app.route('/', methods=['POST'])
def main_post():
    """Process post data
    """

    input_records = request.get_json()

    result = k.kraken_extract_from_record(input_records)
    
    return jsonify(result)

@app.route('/log', methods=['GET'])
def log_get():
    """
    """
    url = LOG_URL

    t = Thing()
    t.api_url(LOG_URL)
    
    things = Things()

    things.api_get({})

    content = things.html.table()
    
    return Response(content)
    


def run_api():
    #from waitress import serve
    #serve(app, host="0.0.0.0", port=8080, threads= 20)
    app.run(host='0.0.0.0', debug=False)

