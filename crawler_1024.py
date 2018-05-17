import requests
from bs4 import BeautifulSoup
import os

# 设置requests get的proxy
proxies = {"http": "http://10.144.1.10:8080", "https": "http://10.144.1.10:8080", }
# mainpage URL to format item URL
rootURL = 'http://t66y.com/'
# DRG main URL to format page URL
drgRootURL = 'http://t66y.com/thread0806.php?fid=16&search=&page='

# picture root dir
jgpRootDir = 'C:\develop\\1024\\'

def getPageList():
    drgPageList = []
    for i in range(1, 101):
        drgPageList.append(drgRootURL + str(i))
    return drgPageList

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
        # 忽略首页公告栏部分颜色为红色和蓝色的链接
        if (fontLabel):
            # 获取font color
            fontColor = fontLabel[0]['color']
            # print(fontColor)
        # 如果font color为blue或者red，则忽略此链接
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
    inputLabels = soup.select('input')
    # print(inputs)

    pictureDir = jgpRootDir + url.replace(':', '').replace('/', '') + '\\'
    os.mkdir(pictureDir)

    num = 0
    for inputLabel in inputLabels:
        if inputLabel.has_attr('src'):
            jpgSrcLink = inputLabel['src']
            print(jpgSrcLink)
            jpgResponse = requests.get(jpgSrcLink, proxies=proxies)
            # print(jpgResponse.status_code)

            num += 1
            jpgPath = pictureDir + str(num) + '.jpg'

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
