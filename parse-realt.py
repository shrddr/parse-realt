# -*- coding: utf-8 -*-
"""
Created on Mon Oct 07 11:38:45 2013

@author: user

http://www.nb.by/realty/proposal/housing-stock/flat/
"""

import urllib2
from bs4 import BeautifulSoup
import time

query = "http://irr.by/realestate/sale-flats/search/geo_city=%D0%9C%D0%B8%D0%BD%D1%81%D0%BA/currency=USD"
terms = ['Цена', u'Количество комнат', u'Общая площадь', u'Год постройки']
filterprice = 10000000
out_file = 'out.txt'


def parsepage(s, d):
    p = BeautifulSoup(s)
    table = p.find("table", {"class": "adListTable"})       
    for row in table.find_all("tr", {"class": "advertRow"}):
        price = row.find("div", {"class": "priceUSD"})
        price = price.string
        price = price.replace('$', '')
        price = "".join(price.split())
        if price.isdecimal(): 
#            print(int(price))        
            i = row.find("a")['href']
            i = i.replace(u'/realestate/sale-flats/', u'')
            i = i.replace(u'/', u'')
            i = int(i)
            if (int(price) < filterprice):
                d[i] = [int(price), 0, 0, 1900]

def parseflat(i, s, d):
    
    p = BeautifulSoup(s)
    
    table = p.find("table", {"id": "mainParams"})
    for row in table.find_all("tr"):                  
        k = row.find("th")
        if (k != None):
            v = k.find_next_sibling("td")
            if ((v != None) and (v.div != None)):
#                print(k.string)
#                print(v.div.string)
                if (k.string in terms):
                    d[i][terms.index(k.string)] = v.div.string


d = {}

for i in range(1, 11):

#    try:
#        url = 'page{}.htm'.format(i)
#        s = open(url, 'r').read()
#    except IOError:
#        print("{} IOError".format(url))
#        continue

    try:
        url = query + "/page_len100/page{}/".format(i)
        s = urllib2.urlopen(url).read()
        open('2013-10-16/page{}.htm'.format(i), 'w').write(s)
        print("{} ok".format(url))
    except urllib2.URLError:
        print("{} URLError".format(url))
        continue   
    time.sleep(1)

    parsepage(s, d)
    
print("{} id's fetched".format(len(d)))





    

f = open(out_file, 'w')
f.write("id;price;rooms;area;year\n")


for i in d:
    
#    try:
#        url = 'test{}.htm'.format(i)
#        s = open(url, 'r').read()
#    except IOError:
#        print("id{} IOError".format(url))
#        continue
    
    try:
        url = "http://irr.by/realestate/sale-flats/{}/".format(i)
        s = urllib2.urlopen(url).read()
        open('2013-10-16/id{}.htm'.format(i), 'w').write(s)
        print("{} ok".format(url))
    except urllib2.URLError:
        print("{} URLError".format(url))
        continue   
    time.sleep(1)
    
    parseflat(i, s, d)
    f.write("{i};{d[0]};{d[1]};{d[2]};{d[3]}".format(i=i, d=d[i]))
    f.write("\n")
    f.flush()
   
            
f.close()
    
print(d)