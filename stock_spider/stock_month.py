import requests
from bs4 import BeautifulSoup
import os
import time
import csv

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.1708.400 QQBrowser/9.5.9635.400'
}


# parameter
# shareCode/year/season : 股票代码，年份，季度

# 股票代码，年度，季度，获取每一季度数据的rows
def sharesCrawl(shareCode, year, season):
    shareCodeStr = str(shareCode)
    yearStr = str(year)
    seasonStr = str(season)
    url = 'http://quotes.money.163.com/trade/lsjysj_' + shareCodeStr + '.html?year=' + yearStr + '&season=' + seasonStr
    # 获取相应网页
    data = requests.get(url, headers=headers)
    soup = BeautifulSoup(data.text, 'lxml')

    # soup.findAll返回一个list，通过【0】取出第一个元素
    table = soup.findAll('table', {'class': 'table_bg001'})[0]
    print(table)
    rows = table.findAll('tr')
    print(rows)

    return rows[::-1]


def writeCSVWithName(shareCode, beginYear, endYear):
    shareCodeStr = str(shareCode)
#http://quotes.money.163.com/trade/lsjysj_600000.html
    url = 'http://quotes.money.163.com/trade/lsjysj_' + shareCodeStr + '.html'
    data = requests.get(url, headers=headers)
    soup = BeautifulSoup(data.text, 'lxml')

    name = soup.select('h1.name > a')[0].get_text()

    csvFile = open('d:/stock/dataWithName/' + shareCodeStr + name + '.csv', 'w+')
    writer = csv.writer(csvFile)
    writer.writerow(('日期', '开盘价', '最高价', '最低价', '收盘价', '涨跌额', '涨跌幅', '成交量', '成交金额', '振幅', '换手率'))

    #writer.writerow(("date", "Opening price", "highest price", "Lowest price", "Closing price", "Change amount", "Quote change", "Volume", "Turnover", "amplitude", "Change rate"))

    try:
        for i in range(beginYear, endYear + 1):
            print(str(i) + 'is going')
            time.sleep(4)
            # 循环获取4个季度的数据
            for j in range(1, 5):
                rows = sharesCrawl(shareCode, i, j)
                for row in rows:
                    csvRow = []
                    # cell.get_text()取td标签中的内容
                    for cell in row.findAll('td'):
                        csvRow.append(cell.get_text().replace(',', ''))
                    if csvRow != []:
                        writer.writerow(csvRow)
                time.sleep(3)
                print(str(i) + '年' + str(j) + '季度is done')
    except:
        print('----- 没进入循环-----')
    finally:
        csvFile.close()


writeCSVWithName(600022, 2017, 2017)