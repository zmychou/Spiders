#!/usr/bin/python3

from urllib.request import urlopen
from bs4 import BeautifulSoup

from CsvReader import CsvReader

import re
import requests
import time
import csv
import threading

class WorkerThread(threading.Thread):
    '''A worker trhead which use to crawl the specific page'''

    def __init__(self, tags, existPool, threadName) :
        '''Initialization'''
        threading.Thread.__init__(self)
        self.tags = tags
        self.existPages = existPool
        self.threadName = threadName
        self.csvReader = CsvReader(threadName+'.csv')
        self.existPages = self.existPages.union(self.csvReader.getOffset())
    
    def filter(s, candidate):
        prev = len(pool)
        pool.add(candidate)
        current = len(pool)
        return prev == current
    
    
    def hasNextPage(self, obj):
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
    
    def findAllTag(self, base, offset, debug):
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
        self.tags = tags
        return tags            

    def getTags(self) :
        return self.tags
    
    def parsePage(self, writer, obj, debug):
        '''Crawling all data we want at the specific url offset'''
    
        items = obj.findAll("div",{"class":"pl2"})
        for item in items:
            try:
                url = item.a.attrs['href']
                urlContent = url.split('/')
                offset = urlContent[len(urlContent) - 2]
                threadLock.acquire()
                exists = filter(offset)
                threadLock.release()
                if exists :
                    print('Duplicace item...')
                    continue
                html = requests.get(url).content
                soup = BeautifulSoup(html)
                title = soup.find('span',{'property':'v:itemreviewed'})
                text = title.next_sibling.next_sibling.text
                title = title.text.strip()
                year = re.findall(r'[0-9]{4}', text)
                rating_num = soup.find('strong',{'property':'v:average'}).text
                votes = soup.find('span',{'property':'v:votes'}).text
                tags_body = soup.find('div',{'class':'tags-body'})
                tags = tags_body.findAll('a')
                runtime = soup.find('span',{'property':'v:runtime'})
                directories = soup.findAll('a',{'rel':'v:directedBy'})
                stars = soup.findAll('a',{'rel':'v:starring'})
                genress = soup.findAll('span',{'property':'v:genre'})
                official_site = soup.find('div',{'class':'subject clearfix'})\
                        .find('div',{'id':'info'})\
                        .findAll('a',{'rel':'nofollow'})
    
                info = []
                if len(official_site) > 1: 
                    contry = official_site[0].next_sibling.next_sibling.next_sibling.next_sibling
                    lang = contry.next_sibling.next_sibling.next_sibling.next_sibling
                    info.append(contry)
                    info.append(lang)
                else:
                    contry = genress[len(genress) - 1].next_sibling.next_sibling.next_sibling.next_sibling
    
                    lang = contry.next_sibling.next_sibling.next_sibling.next_sibling
                    info.append(contry)
                    info.append(lang)
    
                directors = []
                if len(directories) < 2:
                    for director in directories:
                        directors.append(director.text)
                    directors.append(' ')
                genres = []
                if len(genress) < 4:
                    for genre in genress:
                        genres.append(genre.text)
                    genres.append(' ')
                    genres.append(' ')
                    genres.append(' ')
                    genres.append(' ')
                vidioType = 'movie'
                if runtime is None:
                    vidioType = 'series'
                    runtime = 'unknown'
                else:
                    runtime = runtime.attrs['content']
                itm = [url, title, year[0], rating_num, votes,\
                        runtime, directors[0], directors[1], \
                        stars[0].text, stars[1].text, stars[2].text, stars[3].text, stars[4].text,\
                        genres[0], genres[1], genres[2], genres[3], \
                        info[0], info[1], vidioType]
                writer.writerow(itm)
                print(title)
                time.sleep(2)
            except AttributeError as e:
                print("Some thing wrong,but we will continue!")
            except IndexError as e:
                pass
    
    def run(self):
        '''主函数'''
        baseUrl = "https://movie.douban.com"
        offset = "/tag/"
        debug = True
    #    tags = findAllTag(baseUrl, offset, debug)            
    
        print('zmychou')
    
        csvFile = open(self.threadNmae+".csv", "a+", encoding='utf-8')
        try:
            writer = csv.writer(csvFile)
            for tag in self.tags:
    
                classifies = tag.split('/')
                classifies = classifies[2].split('?')
                classify = classifies[0]
                url = baseUrl + tag
                dom = requests.get(url).content
                obj = BeautifulSoup(dom)
                self.parsePage(writer, obj, classify)
                print(tag)
                time.sleep(3)
                nextOne = self.hasNextPage(obj)
                while  nextOne is not None:
    
                    dom = requests.get(nextOne).content
                    obj = BeautifulSoup(dom)
                    self.parsePage(writer, obj, classify)
                    time.sleep(3)
                    nextOne = self.hasNextPage(obj)
        finally:
            csvFile.close();
            pass
    
