from libraries import *


#python2

#config part : 

useragentsFile = "config/useragents"


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
def inscope(url):
    return True

def getURLs(url, timeoutValue, verifySSL, allowRedirects):
    URLs = []
    r = requests.get(url, headers=headers, timeout=timeoutValue, verify=verifySSL, allow_redirects=allowRedirects)
    soup = BeautifulSoup(r.content, "html.parser")
    for a in soup.find_all("a"):
        try:
            href = a["href"]
            if len(href) > 0:
                if not absoluteURL(href):
                    href = relativeToAbsolute(url, href)                
                if isCrawlable(href) and inscope(href):
                    URLs.append(href)
        except Exception:
            pass
    return URLs

hittedURLs = []
def depthCrawling(url, d, maxDepth, timeoutValue, verifySSL, allowRedirects):
    global hittedURLs
    print("call")
    if d == maxDepth:
        return
    crawledURLs = getURLs(url, timeoutValue, verifySSL, allowRedirects)
    print(crawledURLs)
    for crawledURL in crawledURLs:
        if crawledURL not in hittedURLs:
            #print(crawledURL)
            hittedURLs.append(crawledURL)
            print(crawledURL)
            depthCrawling(crawledURL, d + 1, maxDepth, timeoutValue, verifySSL, allowRedirects)
    
def breadhCrawling(url, d, maxDepth, timeoutValue, verifySSL, allowRedirects):
    global hittedURLs
    q = [url]
    while len(q) > 0 and d < maxDepth:
        crawledURLs = getURLs(q[-1], timeoutValue, verifySSL, allowRedirects)
        for crawledURL in crawledURLs:
            if crawledURL not in hittedURLs:
                hittedURLs.append(crawledURL)
                q.append(crawledURL)
        d += 1