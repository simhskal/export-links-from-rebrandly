import csv
from urllib.parse import urlencode

import requests


class MissingAPIKeyError(Exception):
    pass

class DefaultFilenameError(Exception):
    pass

def validate_api_key(api_key):
    if not api_key:
        raise MissingAPIKeyError("API key is required. Please add your API key to the configuration section.")
    return api_key

def validate_filename(filename):
    if "renamethis" in filename.lower():
        raise DefaultFilenameError("Please rename the export file by changing 'exportFileName' in the configuration")

def get_headers(api_key):
    if not api_key:
        raise MissingAPIKeyError("API key is required. Please add your API key to the configuration section.")
    return {
        "apikey": api_key,
        "Content-Type": "application/json",
    }

# Configuration
apiKey = " ".strip()
workspace = None
exportFileName = "exported_links_renamethis.csv"

if __name__ == "__main__":
    validate_filename(exportFileName)
    headers = get_headers(apiKey)  # Use these headers for your requests

fieldnames = ['id', 'createdAt', 'shortUrl', 'destination']

# CONSTRAINTS
MAX_PAGE_SIZE = 25

def downloadLinksAfter(lastLink):
    last = lastLink["id"] if lastLink else ""
    requestHeaders = {
      "Content-type": "application/json",
      "apikey": apiKey,
      "workspace": workspace
    }
    querystring = urlencode({
      "limit": MAX_PAGE_SIZE,
      "last": last,
      "orderBy": "createdAt",
      "orderDir": "desc"
    })
    endpoint = f"https://api.rebrandly.com/v1/links?{querystring}"
    r = requests.get(endpoint, headers=requestHeaders)
    if (r.status_code != requests.codes.ok):
      raise Exception(f"Could not retrieve links, response code was {r.status_code}")
    links = r.json()
    return links

def export():
    downloadedAll = False
    downloaded = None
    
    def lastOne():
        return downloaded[-1] if downloaded else None
        
    def initFile(exportCSV):
        outputFile = csv.DictWriter(exportCSV, fieldnames=fieldnames)
        outputFile.writeheader()
        
    def saveLinksToFile(links, exportCSV):
        outputFile = csv.DictWriter(exportCSV, fieldnames=fieldnames)
        def map(link):
            output = {}
            for field in fieldnames:
                output[field] = link[field] if field in link else ""
            return output
        outputFile.writerows([map(link) for link in links])

    with open(exportFileName, "w", encoding="UTF8", newline="") as exportCSV:
        initFile(exportCSV)
        while (not downloadedAll):
            downloaded = downloadLinksAfter(lastOne())
            if not any(downloaded):
                downloadedAll = True
            else:
                saveLinksToFile(downloaded, exportCSV)

export()