import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from unicodedata import normalize
import datetime
import uuid
from io import StringIO  


def get(url, html):
    
    return extract_tables(url, html)

def extract_tables(url, html):

    file = StringIO(html)
    try:
        tables = pd.read_html(file)
    except Exception as e:
        if str(e) != 'No tables found':
            print(e)
        return []
    
    
    records = []
    count = 0
    for t in tables:

        record = {
            '@type': 'table',
            '@id': str(uuid.uuid4()),
            'text': t.to_json(None,'records'),
            'dateCreated': datetime.datetime.now(),
            'url': url,
            'name': f'table_{str(count)}'
        }
        records.append(record)
        count += 1

    return records