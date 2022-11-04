from bs4 import BeautifulSoup

def getEvents(content):
    soup = BeautifulSoup(content, "html.parser")
    codes = []
    for tag in soup.find_all():
        try:
            attributes = tag.attrs
            for attribut in attributes:
                if attribut[:2].lower() == "on":
                    codes.append(tag[attribut])
        except Exception:
            pass
    return codes


