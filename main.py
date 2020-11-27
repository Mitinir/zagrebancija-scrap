from bs4 import BeautifulSoup
from urllib.request import urlopen
from datetime import date
import sys


"""

ZAGREBANCIJA SCRAPOTRONIC 3000

ej bando,

Dio koji dosad radi:
das funkciji downloadUrlsFromPage link na neku specificnu kategoriju i on ce poskidat linkove na clanke
ako ti clanci nisu stariji od 2020, to pali pomocu dateChecka. Potom sam isao poskidati linkove na sve kategorije
kroz getCategories pa sam u mainu njega stavio prije nek to poskida, i onda za svaku kategoriju iz tog fajla nek se 
izvrti downloadUrlsFromPage-- to je barem ideja. 

TODO:
--stavit u petlju koja će ić stranicu po stranicu u kategoriji i skidat članke do početka 2020,
najbolje doslovno iteratorom jer to izgleda kao /crna-kronika/page/2/, /page/3/ itd a skripta ionako stane 
kad je starije od 2020

--promijenit implementaciju tog dateChecka tako da ne exita odmah cijeli program nego da nastavi sa iducom kategorijom,
ovo sa sys exitom sam na brzinu napravio samo kao boilerplate

--onako testno iz liste linkova na same clanke izvuc metapodatke beautifulsoupom i igrat se sa slaganjem u csv


U mainu zakomentiravajte i odkomentiravajte po potrebi kad cete testirat stvari, da vam program ne radi requestove
non stop i da vam se konzola ne popunjava glupostima. Za pocetak predlazem odkomentirat downloadUrlsFromPage
i u argument pasteat prvu stranicu neke kategorije.

Lp, 
Uprava
"""
def main():
    print("Main!")
    url = "https://www.zagrebancija.com/"
    #getCategories("https://www.zagrebancija.com/")
    #downloadUrlsFromPage("https://www.zagrebancija.com/kategorija/aktualnosti/crna-kronika/page/2")
    """
    Imamo txt sa linkovima na kategorije, sad za svaku kategoriju zelimo provest funkciju koja ce poskidati
    linkove na clanke koji su izasli u 2020.
    """

    """
    fajl = open("categoryLinks.txt", "r")
    for link in fajl:
        link = link.rstrip() #jer smo ih zapisivali u fajl sa newline znakom
        downloadUrlsFromPage(link)
    """


#ideja je dobit listu linkova na kategorije
def getCategories(url):
    c = urlopen(url).read()
    soup = BeautifulSoup(c, features="lxml")
    body_tag = soup.body
    foo = body_tag.contents
    uls = body_tag.find_all("ul")[:7]
    categoryList = []
    #print(type(uls))
    for litag in uls[1:6]: #liTag je jos uvijek bs4 element tag
        #print(litag)
        list = litag.find_all("a")
        for li in list: #li je jos uvijek bs4 tag
            print(li["href"])
            categoryList.append(li["href"])
    fajl = open("categoryLinks.txt", "w")
    for category in categoryList:
        fajl.write(category + "\n")
    fajl.close()

def downloadUrlsFromPage(url):
    c = urlopen(url).read()
    soup = BeautifulSoup(c, features="lxml")
    if dateCheck(soup) == False:
        print("Prestaro!")
        sys.exit()
    h3s = []
    aTags = []
    urls = []
    divs = soup.find_all('div')
    for div in divs:
        if div.find('h3') != None:
            h3s.append(div.find('h3'))
            #a href tagovi su i u h3 tagovima i u thumbnail tagovima, mogli smo birat ijedno

    for h3 in h3s:
        aTags.append(h3.find('a'))

    for aTag in aTags:
        urls.append(aTag.get('href'))

    sortedUrls = list(set(urls)) #micemo duplikate

    fajl = open("linkovi.txt", "a")
    for sortedUrl in sortedUrls:
        print(sortedUrl)
        fajl.write(sortedUrl + "\n")
    fajl.close()

def dateCheck(soup):
    timetags = soup.find_all("time")
    datetimes = []
    is2020 = True
    for time in timetags:
        datetime = time["datetime"][:10]
        dateBroken = datetime.split("-")
        pyDate = date(int(dateBroken[0]), int(dateBroken[1]), int(dateBroken[2]))
        datetimes.append(pyDate)
    foos = [] #sigh. objasnim
    for ddate in datetimes:
        strdate = str(ddate)
        print(strdate[:4])
        if strdate[:4] != "2020":
            foos.append(strdate)
    if len(foos) >= 10:
        print("Prestaro!")
        is2020 = False
    return is2020

if __name__ == "__main__":
    main()