# -*- coding: utf-8 -*-
"""
Created on Mon Oct 07 11:38:45 2013

@author: user

http://habrahabr.ru/post/148782/
http://software-carpentry.org/blog/2012/05/an-exercise-with-matplotlib-and-numpy.html
"""

FILES = ['2013-10-29.txt']

import numpy as np
import numpy.ma as ma
import matplotlib.pyplot as plt

conv = lambda s: float(s.replace(',','.'))

for F in FILES:
    d = np.genfromtxt(F, delimiter=';', names=True, converters = {'area':conv},
                      dtype=[('id', 'int'),
                             ('price', 'float'),
                             ('rooms', 'int'),
                             ('area', 'float'),
                             ('year', 'int')])
                             
    

    mask = (d['area'] < 1)
    d = ma.masked_array(d, mask)
    mask = (d['area'] > 200)
    d = ma.masked_array(d, mask)
    mask = (d['price'] < 30000)
    d = ma.masked_array(d, mask)
    mask = (d['price'] > 300000)
    d = ma.masked_array(d, mask)
    
    dpm = d['price'] / d['area']
    
#    area = np.sort(d, order = 'area')
    
    area = d['area'].compressed()
    price = d['price'].compressed()
    
    

#np.ma.anomalies
    
    fig = plt.figure()
    fig.canvas.set_window_title(F) 
    
    plt.scatter(area, price)
    
    k, c = np.polyfit(area, price, 1)
    simple = np.arange(0, 100)
    plt.plot(simple, c + (k * simple), 'r')
     
    plt.annotate('{0:.2f} * x + {1:.2f}'.format(k, c), (0.05, 0.9), xycoords='axes fraction')
    plt.annotate('|{0:.2f}|'.format( np.average(price / area) ), (0.05, 0.8), xycoords='axes fraction')
    plt.legend(loc='lower right')    
    
    plt.show()
    
    
    
    fig = plt.figure()
    
    mask = (d['rooms'] <> 1)
    n = ma.masked_array(d, mask, keep_mask=False)
    print d[1:10]
    area = n['area'].compressed()
    price = n['price'].compressed()
    k, c = np.polyfit(area, price, 1)    
    plt.plot(simple, c + (k * simple), 'r')
    plt.scatter(area, price, 20, 'r')
    
    mask = (d['rooms'] <> 2)
    n = ma.masked_array(d, mask, keep_mask=False)
    print d[1:10]
    area = n['area'].compressed()
    price = n['price'].compressed()
    k, c = np.polyfit(area, price, 1)    
    plt.plot(simple, c + (k * simple), 'g')
    plt.scatter(area, price, 20, 'g')
    
    mask = (d['rooms'] <> 3)
    d = ma.masked_array(d, mask, keep_mask=False)
    area = d['area'].compressed()
    price = d['price'].compressed()
    k, c = np.polyfit(area, price, 1)    
    plt.plot(simple, c + (k * simple), 'b')
    plt.scatter(area, price, 20, 'b')
    
    plt.show()