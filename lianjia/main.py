
from urllib.request import urlopen
from bs4 import BeautifulSoup

from package.NumBloom import filtration

import re
import time


def main():
    html = urlopen('http://sz.lianjia.com/zufang/pg6') 
    bsObj = BeautifulSoup(html)
    item = bsObj.find('div',{'class':'page-box house-lst-page-box'})
    print(item.attrs['page-data'])

main()
