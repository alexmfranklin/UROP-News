import bs4 as bs
from bs4 import SoupStrainer
import urllib.request
import json
from datetime import date
from datetime import timedelta
import os, ssl
if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
    getattr(ssl, '_create_unverified_context', None)):
    ssl._create_default_https_context = ssl._create_unverified_context

only_tr_tags = SoupStrainer('tr')
only_td_tags = SoupStrainer('td', {'colspan': '2'})

sauce = urllib.request.urlopen('http://www.ust.hk/about-hkust/media-relations/press-releases').read()
soup = bs.BeautifulSoup(sauce, 'html.parser', parse_only=only_tr_tags)
number_of_pages = int(soup.findAll('a', {'class': 'page-numbers'})[2].get_text())

base_url = 'http://www.ust.hk/about-hkust/media-relations/press-releases/page/'

def collectData():
    data = []
    #Cycle through every page on the website
    for i in range(1, 4):
        print(i)
        sauce = urllib.request.urlopen(base_url + str(i)).read()
        soup = bs.BeautifulSoup(sauce, 'html.parser', parse_only=only_tr_tags)

        articles = soup.findAll('tr', {'style': ''})
        for article in articles:
            dataPart = {}

            link_title = article.find('a', {'class':'press-link'})
            if(link_title != None):
                #Find all the titles of the articles
                dataPart['title'] = link_title.get_text()
                #Find all the links of the articles
                dataPart['link'] = link_title.get('href')

            #Find all the dates of the articles
            date = article.find('td', {'style': ''})
            if(date != None):
                dataPart['date'] = date.get_text()

            #Find all the text of the articles
            textString = ''
            if(link_title != None):
                sauce2 = urllib.request.urlopen(dataPart['link']).read()
                soup2 = bs.BeautifulSoup(sauce2, 'html.parser', parse_only=only_td_tags)
                text = soup2.findAll('p')
                for paragraph in text:
                    textString += paragraph.get_text() + ' '
                dataPart['text'] = textString


            #Add the dataPart to the data
            if(dataPart != {} and dataPart['title'] != ''):
                data.append(dataPart)

    return data

def collectAllData():
    data = collectData()

    dependencyData = compileDepenencyData(data)
    articleData = compileArticleData(data)

    return (dependencyData, articleData)

#Arrange the data in the format of the dependency graph
def compileDepenencyData(data):
    dependencyData = {}

    #Create list of titles
    titles = []
    for d in data:
        titles.append(d['title'])

    #Create the initial dependency matrix
    matrix = []
    for row in range(0, len(titles)):
        dataRow = []
        for column in range(0, len(titles)):
            if(row == column):
                dataRow.append(1)
            else:
                dataRow.append(0)
        matrix.append(dataRow)

    dependencyData['packageNames'] = titles
    dependencyData['matrix'] = matrix

    return dependencyData

def compileArticleData(data):
    articleData = []

    for d in data:
        articleData.append(d)

    return articleData

#Write the data to a data file
def writeData(dependencyData, articleData):
    with open("dependencyData.json", "w") as f:
         json.dump(dependencyData, f, indent=1)
    with open("articleData.json", "w") as f:
         json.dump(articleData, f, indent=1)

data = collectData()
writeData(compileDepenencyData(data), compileArticleData(data))















#
