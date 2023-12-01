# Extract from html


## What it does
Extracts the following from html:
- urls
- emails
- images
- tables
- structured data (schema.org)
- text
- title
- feeds


## How to use

### Using the api

#### Send a url (get)
Send the url as a query parameter 'url'.
Will retrieve the content and return extracted data.
If 'contentUrl' provided, will use the content from 'contentUrl' but use 'url' as attributes


#### Send a WebContent object (post)
The content will be extracted from either the 'text' field or it will retrieve the content from the url in 'archivedAt'.

```
{
    "@type": "webContent",
    "url": [
        "https://storage.googleapis.com/kraken-cdn/641fcdaa9664421b3ac4db2b6b494397bf0dc8d65a559e9c2238de77d09e740e.html"
    ],
    "archivedAt": [
        "https://storage.googleapis.com/kraken-cdn/641fcdaa9664421b3ac4db2b6b494397bf0dc8d65a559e9c2238de77d09e740e.html"
    ],
    "about": {
        "@type": "webPage",
        "url": "https://www.petro-canada.ca/en/business/rack-prices"
    }
}

```

### Using the library
Provided url of the page and html content, returns list of records with extractions.

`from kraken_extract_from_html import kraken_extract_from_html as k
`

`records = k.get(url, html)`