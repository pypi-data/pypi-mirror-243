from bs4 import BeautifulSoup

from kraken_extract_from_html.extractors.extract_feeds import extract_feeds
from kraken_extract_from_html.extractors.extract_images import extract_images
from kraken_extract_from_html.extractors.extract_links import extract_links
from kraken_extract_from_html.extractors.extract_schemas import extract_schemas
from kraken_extract_from_html.extractors.extract_src import extract_src
from kraken_extract_from_html.extractors.extract_text import extract_text
from kraken_extract_from_html.extractors.extract_title import extract_title

from kraken_extract_from_html.extractors.extract_title import extract_title
from kraken_extract_from_html.extractors.extract_tables import extract_tables
import requests
import datetime
import copy

from kraken_thing import Thing, Things

ASSET_ID = 'f83225cf-541c-379b-a6bd-b337d1139f6e'
LOG_URL = 'https://apidata.tactik8.repl.co/logs'
LOG_URL = 'https://data.krknapi.com/logs'


def get(url, html):
    return process_extraction(url, html)


def kraken_extract_from_url(url, contentUrl=None):

    contentUrl = contentUrl if contentUrl else url
    
    try:
        r = requests.get(contentUrl)
        html = r.text
    except Exception as e:
        print(e)
        return {}
    
    return process_extraction(url, html)


def kraken_extract_from_html(url, html):
    return process_extraction(url, html)

def kraken_extract_from_record(input_records):

    if not isinstance(input_records, list):
        input_records = [input_records]

    records = []

    for r in input_records:

        about = r.get('about', {})
        if isinstance(about, list) and len(about) > 0: 
            about = about[0]

        aboutUrl = r.get('url', None)
        if isinstance(aboutUrl, list) and len(aboutUrl) > 0: 
            aboutUrl = aboutUrl[0]
        htmls = r.get('text', None)
        archivedAt = r.get('archivedAt', None)

        if not htmls:
            htmls = []
            archivedAt = r.get('archivedAt', [])
            archivedAt = archivedAt if isinstance(archivedAt, list) else [archivedAt]
            for i in archivedAt:
                r = requests.get(i)
                html = r.text
                htmls.append(html)

        if not htmls:
            htmls = []
            urls = r.get('url', [])
            urls = urls if isinstance(urls, list) else [urls]
            for i in urls:
                r = requests.get(i)
                html = r.text
                htmls.append(html)


        for html in htmls:
            if aboutUrl and html:
                record = process_extraction(aboutUrl, html)
                records.append(record)


    return records



def process_extraction(url, html, image_urls = None):

    records = []

    
    text = extract_text(url, html)
    records+=text
    
    soup = _get_soup(html)


    links = extract_links(url, soup)
    records+=links


    images = extract_images(url, soup)
    records += images


    feeds = extract_feeds(url, soup)
    records += feeds

    try:
        schemas = extract_schemas(url, html)
        records += schemas
    except Exception as e:
        print('Error', e)
        a=1

    src = extract_src(url, soup)
    records += src

    texts = extract_text(url, html)
    records += texts

    titles = extract_title(url, soup)
    records += titles


    
    tables = extract_tables(url, html)
    records += tables

    action_record = get_action_record(url, records)

    log_action(action_record)
    
    return action_record




def _get_soup(html):

    soup = BeautifulSoup(html, 'html.parser')

    return soup



def get_action_record(url, records):
    ''' returns action record
    '''
    record = {
        '@type': 'Action',
        'name': 'api extract from html',
        'instrument': {
            "@id": ASSET_ID,
            "@type": "WebApplication"
        },
        'object': {
            '@type': 'WebPage',
            'url': url
        },
        'result': records,
        'actionStatus': 'completedActionStatus',
        'startTime': datetime.datetime.now().isoformat(),
        'endTime': datetime.datetime.now().isoformat()
    }

    return record


def log_action(input_record):
    """Log action to db
    """

    t = Thing()
    t.api_url(LOG_URL)
    
    record = copy.deepcopy(input_record)
    record['result'] = len(record.get('result', []))

    t.load(record)
    t.api_post()
    return
                           
       
