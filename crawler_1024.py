import requests
from bs4 import BeautifulSoup
import os
import re

# proxy setting
proxies = {"http": "http://10.144.1.10:8080", "https": "http://10.144.1.10:8080",}

# Mainpage URL to format item URL
rootURL = 'http://t66y.com/'

# DRG main URL to format page URL
drgRootURL = 'http://t66y.com/thread0806.php?fid=16&search=&page='

# Picture storage root dir
jgpRootDir = "C:\\develop\\1024\\"

# Replace forbidden charactors with "" in Windows' directory name
def filterForbiddenChar(dirName):
    legalDir = re.sub('[\/:*?"<>|]', '', dirName)
    return legalDir

# Generate page link list
def getPageList():
    drgPageList = []
    for i in range(1, 101):
        drgPageList.append(drgRootURL + str(i))
    return drgPageList

# Get item link list from page link
def getItemList(pageLink):
    itemLinks = []
    res = requests.get(pageLink, proxies=proxies)
    res.encoding = 'gbk'
    # print(res.text)
    soup = BeautifulSoup(res.text, 'html.parser')
    header3s = soup.select('h3')
    # print(header3s)
    for header3 in header3s:
        aLabel = header3.select('a')
        fontLabel = header3.select('font')
        fontColor = ''
        # print(fontLabel)
        if (fontLabel):
            fontColor = fontLabel[0]['color']
            # print(fontColor)
        if ((fontColor != 'blue') and (fontColor != 'red')):
            ahref = aLabel[0]['href']
            if (ahref.endswith('html')):
                # print(rootURL + ahref)
                itemLinks.append(rootURL + ahref)
    return itemLinks

def downloadPictureFromURL(url):
    res = requests.get(url, proxies=proxies)
    res.encoding = 'gbk'
    # print(res.text)

    soup = BeautifulSoup(res.text, 'html.parser')
    # Get the Chinese headers to use as the directory name
    headerName = soup.select('h4')[0].text
    pictureDir = jgpRootDir + filterForbiddenChar(headerName)
    if os.path.exists(pictureDir):
        print("Directory is existed: " + pictureDir)
        return
    os.mkdir(pictureDir)

    num = 0
    inputLabels = soup.select('input')
    # print(inputs)
    for inputLabel in inputLabels:
        if inputLabel.has_attr('src'):
            jpgSrcLink = inputLabel['src']
            print("Downloading picture: " + jpgSrcLink)
            jpgResponse = requests.get(jpgSrcLink, proxies=proxies)
            # print(jpgResponse.status_code)

            num += 1
            jpgPath = pictureDir + '\\' + str(num) + '.jpg'

            with open(jpgPath, 'wb') as f:
                f.write(jpgResponse.content)
        elif inputLabel.has_attr('data-src'):
            jpgSrcLink = inputLabel['data-src']
            print("Downloading picture: " + jpgSrcLink)
            jpgResponse = requests.get(jpgSrcLink, proxies=proxies)
            # print(jpgResponse.status_code)

            num += 1
            jpgPath = pictureDir + '\\' + str(num) + '.jpg'

            with open(jpgPath, 'wb') as f:
                f.write(jpgResponse.content)

if __name__ == '__main__':
    pageList = getPageList()
    for page in pageList:
        print("Current page link is: " + page)
        itemList = getItemList(page)
        for item in itemList:
            print("Current item link is: " + item)
            downloadPictureFromURL(item)
