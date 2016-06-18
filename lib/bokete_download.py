from urllib.request import urlopen
from bs4 import BeautifulSoup

def bokete(n):
    try:
        html = urlopen("http://bokete.jp/odai/" + str(n)).read()
        soup = BeautifulSoup(html, "html.parser")
        print(soup.find("h3", class_="boke-text").string)
    except:
        pass


START = 1
END   = 2000000
if __name__ == "__main__":
    for i in range(START, END):
        bokete(i)
