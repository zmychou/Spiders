
from urllib.request import urlopen
from bs4 import BeautifulSoup

import re
import requests
import time
import csv

#def filter(candidate):
#    offset = candidate % 8
#    test = ((pool[candidate] & 0x01 << offset) == 0)
#    if test:
#        pool[candidate] | 0x01 << offset
#    return test

pool = set()

def filter(candidate):
    prev = len(pool)
    pool.add(candidate)
    current = len(pool)
    return prev == current

def hasNextPage(obj):
    """Detect whether there is more pages or not ,if have any pages,return\
            the next page offset ,which looks like /tag/经典?start=60&type=T\
            at this time (2017/5/1) or return None type otherwise"""

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
    """Get all tags at the category page"""
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

def parsePage(writer, obj, debug):
    '''Crawling all data we want at the specific url offset'''
    items = obj.findAll("li",{"class":"subject-item"})
    for item in items:
        url = item.find("div", {"class":"info"}).h2.a.attrs["href"]
        urlContent = url.split('/')
        offset = urlContent[len(urlContent) - 2]
        if filter(offset) is not True:
            try:
                title = item.find("div", {"class":"info"}).h2.a.attrs["title"]
                whatType = re.findall(r'[a-z,A-Z,+,-]*',title)[0]
                subTitle = item.find("div", {"class":"info"}).span.text
                detail = item.find("div", {"class":"pub"}).text.strip()
                year = re.findall(r'[1|2][0-9]{3}',detail)[0]
#                if len(y) > 0 is True:
#                    year = y[0] 
#                else:
#                    year = 'unknown'
                price = re.findall(r'[0-9]{0,3}\.[0-9]{0,3}',detail)
                if len(price) > 0: 
                    price = price[0] 
                else:
                    price = detail.split('/')
                    price = price[len(price) - 1]
                pl = item.find("span", {"class":"pl"}).text.strip()
                pl = re.findall(r'[0-9]{1,9}',pl)[0]
#                if len(l) > 0 is True:
#                    pl = l[0] 
#                else:
#                    pl = 'unknown'
                rating_num = item.find("span", {"class":"rating_nums"}).text
                details = detail.split('/')
                if len(details) < 4:
                    for i in range(5):
                        details.append(" ")
                if len(details) == 4:
                    details.insert(1, " ")

                itm = [url, title, subTitle, year, price, rating_num,\
                        pl, debug, whatType, details[0], details[1],\
                        details[2]]
                writer.writerow(itm)
                print(title)
            except AttributeError as e:
                print("Something wrong,but we will continue!")
            except IndexError as e:
                print(title+" got an error when try to store info..")
                
        else:
            print('Duplicate item.......')

def main():
    '''Entry point of the script'''
    baseUrl = "https://book.douban.com"
    offset = "/tag/"
    debug = True
    tags = findAllTag(baseUrl, offset, debug)            
    
    csvFile = open("files/data.csv", "w+", encoding='utf-8')
    try:
        writer = csv.writer(csvFile)
        for tag in tags:

            print(tag)
            classifies = tag.split('/')
            classifies = classifies[2].split('?')
            classify = classifies[0]
            url = baseUrl + tag
            dom = requests.get(url).content
            obj = BeautifulSoup(dom)
            parsePage(writer, obj, classify)
            nextOne = hasNextPage(obj)
            while  nextOne is not None:

                classifies = nextOne.split('/')
                classifies = classifies[2].split('?')
                classify = classifies[0]
                url = baseUrl + nextOne
                dom = requests.get(url).content
                obj = BeautifulSoup(dom)
                parsePage(writer, obj, classify)
                time.sleep(3)
                nextOne = hasNextPage(obj)
    finally:
        csvFile.close();
        pass
main()
