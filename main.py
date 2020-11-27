from bs4 import BeautifulSoup
from urllib.request import urlopen
from datetime import date
import sys


"""
TODO:
--eeeeh mozda najbolje u kategorijama maknut podkategorije jer su sve stare.

--stavit u petlju koja će ić stranicu po stranicu u kategoriji i skidat članke do početka 2020,
najbolje doslovno iteratorom jer to izgleda kao /crna-kronika/page/2/, /page/3/ itd a skripta ionako stane 
kad je starije od 2020
--promijenit implementaciju tog dateChecka tako da ne exita odmah cijeli program nego da nastavi sa iducom kategorijom,
ovo sa sys exitom sam na brzinu napravio samo kao boilerplate
--onako testno iz liste linkova na same clanke izvuc metapodatke beautifulsoupom i igrat se sa slaganjem u csv
"""
def main():
    print("Main!")

    url = "https://www.zagrebancija.com/"
    #getCategories("https://www.zagrebancija.com/")
    #downloadUrlsFromPage("https://www.zagrebancija.com/kategorija/aktualnosti/crna-kronika/page/2")
    fajl = open("categoryLinks.txt", "r")
    unsorted = []
    ext = 0
    for categLink in fajl:
        categLink= categLink.rstrip()
        downloadUrlsFromPage(categLink, ext)
        ext +=1
    fajl.close()

    fajl_w_doubles = open("linkovi.txt", "r")
    fajl_wo_doubles = open("noDoubles.txt", "a")
    for link in fajl_w_doubles:
        unsorted.append(link)
    fajl_w_doubles.close()
    noDubz = removeDoubles(unsorted)
    for link in noDubz:
        fajl_wo_doubles.write(link)
    fajl_wo_doubles.close()
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

def downloadUrlsFromPage(url, pageNum):
    c = urlopen(url).read()
    soup = BeautifulSoup(c, features="lxml")
    url = url + "page/"+str(pageNum)
    if dateCheck(soup) == False:
        print(url + " Prestaro!")
        return
    print(url + " Nije prestar ") #makni kasnije

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
def removeDoubles(unsortedList):
    sortedList = list(set(unsortedList))
    return sortedList
if __name__ == "__main__":
    main()