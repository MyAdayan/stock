import pymysql
import urllib
import re
import urllib.request
import requests
from lxml import etree

#连接数据库
name = 'root'
password = 'root'
db = pymysql.connect('localhost', name, password, charset='gbk')
cursor = db.cursor()
sqlSentence = "use stockDataBase;"
cursor.execute(sqlSentence)

#获取html界面
def getHtml(url):
    html = ""
    try:
        html = urllib.request.urlopen(url).read()
        html = html.decode('gbk')
    except:
        print("404 error")
    return html

#获得股票分类
def getStackClassification(html):
    if html == "":
        return ""
    selector = etree.HTML(html)
    info = selector.xpath('//div[@class="aide nb"]/div/a/text()')
    #s = r'<a href="http://quote.eastmoney.com/center/list.html#\d+_\d_\d" target="_blank">(.*?)</a>'
    #pat = re.compile(s)
    #classification = pat.findall(str(info))
    print("info"+info)
    classification = info[2]
    return classification

cursor.execute('select distinct stock_code from stock_all')
results = cursor.fetchall()
codes = list(results)

sqlSentence2 = "delete from stock_classification where 1=1"
cursor.execute(sqlSentence2)
j = 0
codes = "601112"
for code in codes:
    code = ''.join(code)#将tuple转换为字符串
    url = ""
    #判断连接是否存在

    if getHtml("http://quote.eastmoney.com/sz" + code + ".html") is not "":
        url = "http://quote.eastmoney.com/sz" + code + ".html"
    elif getHtml("http://quote.eastmoney.com/sh" + code + ".html") is not "":
        url = "http://quote.eastmoney.com/sh" + code + ".html"
    else:
        continue

    if getStackClassification(getHtml(url))=="-":
        getStackClassification(getHtml(url))
        classification = "null";
    else:
        classification = getStackClassification(getHtml(url))

    print(code)
    print(classification)
    sqlSentence3 = "insert into stock_classification" + "(stock_code, classification) values ('%s','%s')" % (code,classification)
    cursor.execute(sqlSentence3)
    j = j + 1
    if j >= 100:
        j = 0
    db.commit()