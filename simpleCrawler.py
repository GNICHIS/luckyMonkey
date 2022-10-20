import argparse
import requests
import random
from urlparse import urlparse
from urljoin import urljoin
from bs4 import BeautifulSoup

#python2

parser = argparse.ArgumentParser(description='LuckyMonkey.')
"""
parser.add_argument('--sum', dest='accumulate', action='store_const',
                    const=sum, default=max,
                    help='sum the integers (default: find the max)')
"""

timeoutValue = 2
verifySSL = False
allowRedirects = False


useragents = []
with open("data/useragents", "r") as uas:
    for ua in uas:
        useragents.append(ua.strip())

#Randomly pick a useragent from the useragents list

useragent = useragents[random.randint(0, len(useragents) - 1)]

#create an initial simple header

headers = {
    "User-Agent": useragent
}

def absoluteURL(url):
    return (len(urlparse(url).scheme) != 0)
def isCrawlable(url):
    return (urlparse(url).scheme.lower() != "javascript" and urlparse(url).scheme.lower() != "data")
def relativeToAbsolute(parentUrl, url):
    return urljoin(parentUrl, url)

def getURLs(url):
    URLs = []
    r = requests.get(url, headers=headers, timeout=timeoutValue, verify=verifySSL, allow_redirects=allowRedirects)
    soup = BeautifulSoup(r.content, "html.parser")
    for a in soup.find_all("a"):
        try:
            href = a["href"]
            if len(href) > 0:
                if not absoluteURL(href):
                    href = relativeToAbsolute(url, href)
                
                if isCrawlable(href):
                    URLs.append(href)
        except Exception:
            pass


    return URLs


def depthCrawling(URLs):
    return 0
def breadhCrawling(URLs):
    return 0