'''
Created on 5 сент. 2016 г.

@author: garet
'''

from urllib.parse import urlparse

def Programm():
    url = 'https://docs.python.org/3.5/library/urllib.parse.html?highlight=urlparse#urllib.parse.urlparse'
    data = urlparse(url)
    print(data)

if __name__ == '__main__':
    Programm()