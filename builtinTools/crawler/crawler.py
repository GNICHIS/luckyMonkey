import argparse
"""
import requests
import random
from urlparse import urlparse
from urlparse import urljoin
from bs4 import BeautifulSoup
import re
import random
"""

from modules.crawl import *
from modules.payloads import *
from modules.jsparser import *



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

parser.add_argument('--screenshots',
                    help='Enable screenshots mode, so the script will store a screenshot for each visited web page, default = False',
                    #required=True,
                    default=False,
                    type=bool,
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
session = args.session


def genSession(host):
    hexchars = "abcdef0123456789"
    r = ""
    for i in range(0, 6):
        r += hexchars[random.randint(0, len(hexchars) - 1)]
    return(host.replace(".", "_") + "_" + r)

session = genSession(urlparse(startUrl).netloc) if len(args.session) == 0 else args.session



#Manual silly testing :(
#depthCrawling(startUrl, 0)
#signatures : depthCrawling(url, d, maxDepth, timeoutValue, verifySSL, allowRedirects)
#             breadhCrawling(url, d, maxDepth, timeoutValue, verifySSL, allowRedirects)
#breadhCrawling(startUrl, 0, depth, timeoutValue, verifySSL, allowRedirects)
#print(len(hittedURLs))
#print(hittedURLs)

#depthCrawling(startUrl, 0, depth, timeoutValue, verifySSL, allowRedirects)
breadhCrawling(startUrl, 0, depth, timeoutValue, verifySSL, allowRedirects)
"""
print(len(hittedURLs))

print(hittedURLs)
print("===============================")
for key in hittedURLs.keys():
    if len(hittedURLs[key]) > 0:
        print(key, hittedURLs[key])
"""


# after the crawling is finished, the hittedURLs hashTable must be saved as a database in the right location
# is not the good way to only be able to save the work 

from modules.dbblahblah import *

dbFile = "sessions/" + session + ".json"
db = blahblahDB(dbFile)
#print(hittedURLs)
print(db.saveEntireDb(hittedURLs))

