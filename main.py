from bs4 import BeautifulSoup
from urllib.request import urlopen
from datetime import date
import csv


def main():
    print("Main!")
    #url = "https://www.zagrebancija.com/"
    #getCategories("https://www.zagrebancija.com/")

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


    with open('zagrebancija-metapodaci.csv', 'w', newline='\n', encoding="utf-8") as file:

        with open('noDoubles.txt', "r", newline='\n', encoding="utf-8") as linkovi:
            writer = csv.writer(file)
            writer.writerow(["Link", "Naslov", "Podnaslov", "Autor", "Link na autora", "Datum", "Tagovi", "Kategorije", "Tekst"])
            for link in linkovi:
                a = getMetadata(link)
                print(a[-1], a[-2])
                writer.writerow([a[0], a[1], a[2], a[3], a[4], a[5], a[6], a[7], a[8]])
    file.close()
    linkovi.close()

def getMetadata(link):
    """
    autor, naslov, podnaslov, link, (br autorovih clanaka) kategorija, tagovi, datum, tekst
    """
    c = urlopen(link).read()
    soup = BeautifulSoup(c, features="lxml")
    text = soup.get_text()
    #print(text)
    head_tag = soup.head
    #print(type(head_tag))
    metas = head_tag.find_all("meta")
    mList = []
    #za author name: <div class="td-post-author-name">
    for meta in metas:
        mList.append(meta)
    mList = mList[1:]
    title = ""
    url = ""
    description = ""
    pubTime = ""

    for m in mList:

        if (m.get("property")) == "og:title":
            title = (m.get("content"))
        elif (m.get("property")) == "og:description":
            description = (m.get("content"))
        elif (m.get("property")) == "og:url":
            url = (m.get("content"))
        elif (m.get("property")) == "article:published_time":
            pubTime = (m.get("content"))
        else:
            pass




    datetime = pubTime[:10]
    dateBroken = datetime.split("-")
    pyDate = date(int(dateBroken[0]), int(dateBroken[1]), int(dateBroken[2]))
    pubTime = pyDate


    body_tag = soup.body
    #iz bodyja trebamo td_post_author_name, td_post_header (gettext) za kategorije i footer
    divs = body_tag.find_all("div")
    mydivs = soup.find("div", {"class": "td-post-author-name"})
    #print(type(mydivs), mydivs)
    author_link = mydivs.find("a")['href']
    author_name = mydivs.find("a").get_text()

    kategorije = ""
    mydivs2 = soup.find_all("li", {"class": "entry-category"})
    for li in mydivs2:
        kategorije +=  (li.get_text()) + " "

    tagovi = ""
    footFetish = body_tag.find("footer")
    tags = footFetish.find("ul", {"class": "td-tags"})
    hrefs = tags.find_all("a")
    for href in hrefs:
        tagovi += href.get_text() + " "
    tekst = body_tag.find("div",{"class": "td-post-content"})
    realText = str(tekst.get_text())
    print(realText)
    return url, title, description, author_name, author_link, pubTime, tagovi, kategorije, realText
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