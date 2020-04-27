import requests
import string
import re
from bs4 import BeautifulSoup
from .proxy import *

def getsoup(url):
    req=requests.get(url,headers={'User-Agents':"Mozilla/5.0"})
    soup=BeautifulSoup(req.content,"lxml")
    return soup

def getdata(soup):
    d=soup.findAll("div",{"class":"ZINbbc xpd O9g5cc uUPGi"})
    dic=[]
    for i in d:
        temp=i.find("div",{"class":"BNeawe vvjwJb AP7Wnd"})
        li=[]
        if temp is not None:
            title=temp.get_text() 
            ta=i.find("div",{"class":"kCrYT"}).find("a")
            if ta is None:
                continue
            else:
                ta=ta['href']
            link=re.findall("q=(.*)&sa",ta)[0]
            desc=i.find("div",{"class":"BNeawe s3v9rd AP7Wnd"}).get_text()
            if desc is None:
                continue
            li.append(title)
            li.append(link)
            li.append(desc)
        dic.append(li)
    return dic        

# soup=getsoup("https://www.google.com/search?q=user+accaounts")
# print(getdata(soup))