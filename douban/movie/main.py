

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
    category = obj.find('a', {'name':'类型'}).next_sibling.next_sibling
    aTags = category.findAll("a", href = re.compile("^\/tag\/.*$"))
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
    items = obj.findAll("div",{"class":"pl2"})
    for item in items:
        try:
            url = item.a.attrs['href']
            titles = item.a.text.strip()
            title = titles.split('/')[0].strip()
            text = item.p.text
            upTime = re.findall(r'[0-9,-]{10}', text)
            date = []
            if len(upTime) > 0:

                date = upTime[0].split('-')
            else:
                date = ['','','']

            duration = re.findall(r'[0-9]{3}分钟', text)
            if len(duration) > 0:
                duration = duration[0].strip().split('分')
            else:
                duration.append('unknown')
            pl = item.find("span", {"class":"pl"}).text.strip()
            rating_num = item.find("span", {"class":"rating_nums"}).text

            itm = [url, title, date[0], date[1], date[2], duration[0],\
                    rating_num, pl, debug]
            writer.writerow(itm)
            print(title)
        except AttributeError as e:
            print("Something wrong,but we will continue!")
        except IndexError as e:
            pass

def main():
    '''主函数'''
    baseUrl = "https://movie.douban.com"
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
            time.sleep(7)
            nextOne = hasNextPage(obj)
            while  nextOne is not None:

                dom = requests.get(nextOne).content
                obj = BeautifulSoup(dom)
                parsePage(writer, obj, classify)
                time.sleep(6)
                nextOne = hasNextPage(obj)
    finally:
        csvFile.close();
        pass
main()
