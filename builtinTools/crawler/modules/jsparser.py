from bs4 import BeautifulSoup
def copypage(url, content):
    soup = BeautifulSoup(content, "html.parser")
    
