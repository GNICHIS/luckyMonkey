from urlparse import urlparse
from urlparse import urljoin
import sys
import requests
from bs4 import BeautifulSoup
import base64
from tld import get_tld

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0"
}

depth = 5

URLs = []
startUrl = sys.argv[1]

scope = str(get_tld(startUrl, as_object=True).fld)

URLs.append(startUrl)
#setup session for persist cookies and headers
s = requests.Session()
rStart = s.get(startUrl, headers=headers, verify=False, timeout=5)

def absolute(parentUrl, url):
    if urlparse(url).scheme == 0:
        return urljoin(parentUrl, url)
    else:
        if urlparse(url).scheme.lower() == "http" or urlparse(url).scheme.lower() == "https":
            return url
def inScope(url):
    currentScope = str(get_tld(url, as_object=True).fld)
    return(currentScope == scope)

def getURLs(content, parentUrl):
    urls = []
    soup = BeautifulSoup(content, "html.parser")
    for a in soup.find_all("a"):
        try:
            href = a["href"]
            #print(href)
            #print(href)
            if len(href) > 0 and len(absolute(parentUrl, href)) > 0:
                urls.append(absolute(parentUrl, href))
        except Exception:
            pass
    return list(set(urls))
def log(a):
    #show the result and write it to a file
    print(a)
    with open(urlparse(startUrl).netloc.replace(".", "_") + ".txt", "a") as loggingFile:
        loggingFile.write(a + "\n")

crawledURLs = []

def crawl(urls, lvl = 1):
    global crawledURLs
    isThereNewUrls = False
    for url in urls:
        if url not in crawledURLs and inScope(url) == True:
            isThereNewUrls = True
            break
    if lvl <= depth and isThereNewUrls:
        globalChildUrls = []
        for url in urls:
            try:
                r = s.get(url, headers=headers, verify=False, timeout=5)
                if url not in crawledURLs and inScope(url):
                    crawledURLs.append(url)
                    log(url)
                    childUrls = getURLs(r.content, url)
                    globalChildUrls.extend(childUrls)
            except Exception:
                pass
        globalChildUrls = list(set(globalChildUrls))
        lvl += 1
        crawl(globalChildUrls, lvl)

crawl(URLs)