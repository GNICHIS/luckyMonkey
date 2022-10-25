import argparse
import requests
import random
from urlparse import urlparse
from urlparse import urljoin
from bs4 import BeautifulSoup
import re
import random


#python2

#config part : 

useragentsFile = "config/useragents"


parser = argparse.ArgumentParser(description='LuckyMonkey.')

parser.add_argument('--url',
                    help='Url entry point',
                    required=True,
                    )

parser.add_argument('--mode',
                    help='Crawling mode can be either depth or breadh',
                    #required=True,
                    choices=['depth', 'breadh',]
                    )

parser.add_argument('--depth',
                    help='Crawling depth default = 5',
                    #required=True,
                    default=5,
                    type=int,
                    )
parser.add_argument('--timeout',
                    help='Requests timeout default = 5',
                    #required=True,
                    default=2,
                    type=int,
                    )
parser.add_argument('--verifyssl',
                    help='Only accept verified SSL certificate default = True',
                    #required=True,
                    default=True,
                    type=bool,
                    )

parser.add_argument('--allowredirects',
                    help='Follow 301 and 302 url redirections default = False',
                    #required=True,
                    default=False,
                    type=bool,
                    )

parser.add_argument('--include',
                    help='A regular expression (regexp) to define the scope of the urls to follow default = All Urls tied to the parent domain',
                    #required=True,
                    default="",
                    )

parser.add_argument('--exclude',
                    help='A regular expression (regexp) to define the scope of the urls to reject default = None',
                    #required=True,
                    default="",
                    )

parser.add_argument('--session',
                    help='Define the session, default = randomly generated',
                    #required=True,
                    default="",
                    )

args = parser.parse_args()


#timeoutValue = 2
#verifySSL = False
#allowRedirects = False

timeoutValue = args.timeout
verifySSL = args.verifyssl
allowRedirects = args.allowredirects
depth = args.depth
mode = args.mode
startUrl = args.url
include = args.include
exclude = args.exclude




useragents = []
with open(useragentsFile, "r") as uas:
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


hittedURLs = []
def depthCrawling(url, d):
    global hittedURLs
    if d == depth:
        return
    crawledURLs = getURLs(url)
    for crawledURL in crawledURLs:
        if crawledURL not in hittedURLs:
            #print(crawledURL)
            hittedURLs.append(crawledURL)
            depthCrawling(crawledURL, d + 1)
    
def breadhCrawling(url, d):
    global hittedURLs
    q = [url]
    while len(q) > 0 and d < depth:
        crawledURLs = getURLs(q[-1])
        for crawledURL in crawledURLs:
            if crawledURL not in hittedURLs:
                hittedURLs.append(crawledURL)
                q.append(crawledURL)
        d += 1


#Manual silly testing :(
#depthCrawling(startUrl, 0)
breadhCrawling(startUrl, 0)
print(len(hittedURLs))
hittedURLs = []
depthCrawling(startUrl, 0)
print(len(hittedURLs))