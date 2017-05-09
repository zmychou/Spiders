#!/usr/bin/python3

from bs4 import BeautifulSoup
from urllib.request import urlopen

import requests
import re
import time
import json
import csv

class Tieba():
    '''tieba crawling'''
    tiebaBase = 'http://tieba.baidu.com/f?ie=utf-8&kw='
    
    def __init__(self) :
        ''' Initiation '''
        self.posts = []
        self.item = []
        self.user = set()
        pass
    
    def entrance(self, tieba) :

        url = self.tiebaBase + tieba
        html = requests.get(url).content
        return BeautifulSoup(html)
    
    def getPosts(self, bsObj) :
        '''Get all post in one page'''
        hrefs = bsObj.findAll('a', {'class':'j_th_tit'})
        for href in hrefs :
            self.posts.append(href.attrs['href'])


    def hasNext(self, bsObj, pageType) :
        '''Denote whether there are any page to be crawl'''
        current = bsObj.find('span',{'class':pageType})
        try :
            nextSibling = current.next_sibling.next_sibling
            l = nextSibling.attrs['href'].split('/')
            return l[len(l) - 1]
        except AttributeError as e :
            print('Reach the last page!')
            return None

    def filtration(self, candidate) :
        '''Denote whether we have crawled that user info'''
        prev = len(self.user)
        self.user.add(candidate)
        current = len(self.user)
        return prev == current

    def specificPost(self, item_writer, user_writer, urlOffset) :
        '''Get the specific post and crawl all the user's info,including user_id,
        uset_name e.g, and all the the reply''' 
        headers = {
                'Accepti':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Encoding':'gzip, deflate, sdch',
                'Accept-Language':'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4',
                'Cache-Control':'max-age=0',
                'Connection':'keep-alive',
                'Host':'tieba.baidu.com',
                'Referer':'http://tieba.baidu.com/f?kw=%E7%87%95%E5%B1%B1%E5%A4%A7%E5%AD%A6&ie=utf-8&pn=0',
                'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36'
                
                }
        html = requests.get('http://tieba.baidu.com/' + urlOffset, headers = headers).text
        print(urlOffset)
        while True :
            bsObj = BeautifulSoup(html)
            answers = bsObj.findAll('div',{'class':'user-hide-post-position'})
            for answer in answers :
                row = []
                user = []
                data = json.loads(answer.parent.attrs['data-field'])
                user_id = data['author']['user_id']
                name_u = data['author']['name_u']
                user_sex = data['author']['user_sex']
                level_id = data['author']['level_id']
                open_id = data['content']['open_id']
                open_type = data['content']['open_type']
                user_name = data['author']['user_name']
                date = data['content']['date'].split(' ')
                row.append(user_id)
                row.append(user_sex)
                row.append(user_name)
                row.append(name_u)
                row.append(level_id)
                row.append(open_id)
                row.append(open_type)
                row.append(date[0])
                row.append(date[1])
                item_writer.writerow(row)
                print(user_name)
    
                if self.filtration(user_id) is not True :
                    user.append(name_u)
                    user.append(open_id)
                    user.append(open_type)
                    user.append(user_id)
                    user.append(user_sex)
                    user.append(user_name)
                    header = {
                            'Accept':'application/json',
                            'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36'}
                    detail = requests.get('http://tieba.baidu.com/home/get/panel?un=' + name_u).text
                    detail = json.loads(detail)
                    tb_age = detail['data']['tb_age']
                    post_num = detail['data']['post_num']
                    sex = detail['data']['sex']
                    grade = detail['data']['honor']['grade']
                    user.append(tb_age)
                    user.append(post_num)
                    user.append(sex)
                    user.append(date[0])
                    user.append(date[1])
                    if grade is not None :
                        for i in grade :
                            user.append(i)
                            user.append(grade[i]['forum_list'])
                    user_writer.writerow(user)
            exist = self.hasNext(bsObj, 'tP')
            if exist is None :
                break
            time.sleep(2)
            print(exist)
            html = requests.get('http://tieba.baidu.com/p/'+exist).text
            print('next page..........................')

    def main(self) :
        '''Main function,just call it and you just need to input the tieba name 
        such as 燕山大学,the you will get two files :user_info.csv and 
        answer_item.csv'''
        item = open('answer_itme.csv', 'w+')
        user = open('user_info.csv', 'w+')
        answer_item = csv.writer(item)
        user_info = csv.writer(user)
        tieba = input('Input the tieba you what to craw:')
        bsObj = self.entrance(tieba)
        exist = self.hasNext(bsObj, 'pagination-current pagination-item ')
        while True :

            self.getPosts(bsObj)       
            for post in self.posts :
                self.specificPost(answer_item, user_info, post)
            exist = self.hasNext(bsObj, 'pagination-current pagination-item ')
            if exist is None :
                break
            html = requests.get('http://tieba.baidu.com/'+exist).text
            bsObj = BeautifulSoup(html)
            print('***********************new page*********************')
