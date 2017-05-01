

from urllib.request import urlopen
from bs4 import BeautifulSoup

import re
import requests
import time
import csv

def hasNextPage(obj):

    try:
        target = obj.find("span",{"class":"thispage"}).next_sibling.next_sibling
        if target is not None:
            href = target.attrs["href"]
            print(href)
            return href 
    except AttributeError as e:
        print("AttributeError:'NavigableString' object has no attribute 'attrs'")
        return None
    except KeyError as e:
        pass

def findAllTag(base, offset, debug):
    url = base+offset

    dom = requests.get(url).content
    obj = BeautifulSoup(dom)
    aTags = obj.findAll("a", href = re.compile("^\/tag\/.*$"))
    tags = []
    for tag in aTags:
        href = tag.attrs["href"]
        tags.append(href)
        if debug:
            print(href)
    return tags            

#def saveData(fileName, itme):
    


def parsePage(writer, obj, debug):
    '''Crawling all data we want at the specific url offset'''
    items = obj.findAll("li",{"class":"subject-item"})
    for item in items:
        try:
            title = item.find("div", {"class":"info"}).h2.a.attrs["title"]
            subTitle = item.find("div", {"class":"info"}).span.text
            detail = item.find("div", {"class":"pub"}).text.strip()
            pl = item.find("span", {"class":"pl"}).text.strip()
            rating_num = item.find("span", {"class":"rating_nums"}).text
            details = detail.split('/')
            if len(details) < 4:
                for i in range(5):
                    details.append(" ")
            if len(details) == 4:
                details.insert(1, " ")

            itm = [title, subTitle, details[0], details[1], details[2], \
                    details[3], details[4], rating_num, pl, debug]
            writer.writerow(itm)
            print(title)
        except AttributeError as e:
            print("Something wrong,but we will continue!")

def main():
    '''主函数'''
    baseUrl = "https://book.douban.com"
    offset = "/tag/"
    debug = True
    tags = findAllTag(baseUrl, offset, debug)            
    
    csvFile = open("files/test.csv", "w+", encoding='utf-8')
    try:
        writer = csv.writer(csvFile)
        for tag in tags:

            classifies = tag.split('/')
            classifies = classifies[2].split('?')
            classify = classifies[0]
            url = baseUrl + tag
            dom = requests.get(url).content
            obj = BeautifulSoup(dom)
            parsePage(writer, obj, classify)
            print(tag)
            time.sleep(4)
            nextOne = hasNextPage(obj)
            while  nextOne is not None:

                classifies = nextOne.split('/')
                classifies = classifies[2].split('?')
                classify = classifies[0]
                url = baseUrl + nextOne
                dom = requests.get(url).content
                obj = BeautifulSoup(dom)
                parsePage(writer, obj, classify)
                time.sleep(4)
                nextOne = hasNextPage(obj)
    finally:
        csvFile.close();
        pass
main()
