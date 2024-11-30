import csv
from urllib.parse import urlencode

import requests

# CONFIGURATION - Rename this file as needed
exportFileName = "exported_links_renamethis.csv"
# Add API key here
apiKey = " "
workspace = None
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