import pymysql
import urllib
import re
import requests
import json
import random
from datetime import date, datetime
import unicodecsv as csv
import os

class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)

class DBUtil(object):
    def __init__(self, name, password):
        self.name = name
        self.password = password

    def connect(self, databaseName):
        self.db = pymysql.connect('localhost', self.name, self.password, charset='gbk')
        self.cursor = self.db.cursor()
        sqlSentence = "use " + databaseName + " ;"
        self.cursor.execute(sqlSentence)

    def query(self, statement):
        try:
            self.cursor.execute(statement)
            desc = [item[0] for item in self.cursor.description]
            result = [dict(zip(desc, item)) for item in self.cursor.fetchall()]
        except:
            print("Error: unable to fecth data")
        return result

    def execute(self, statement):
        self.cursor.execute(statement)


    def close(self):
        self.db.close()

class InputData(object):
    def input(self):
        # self.stockCode = raw_input("stockCode:")
        self.startDate = input("startDate:")
        self.endDate = input("endDate:")
        self.quantity = int(input("quantity:"))

def genereteJson(file, data):
    with open(file, 'w') as f:
        json.dump(data, f)

def getRondomCode(quantity, data):
    if quantity > len(data) or quantity < 1:
        return []
    else:
        return [[value for key,value in item.items()][0] for item in random.sample(data, quantity)]

def json2CSV(jsonFile, csvFile):
    with open(jsonFile, 'r') as f:
        jsondata = json.load(f)

    # jsonData = open(jsonFile)
    csvfile = open(csvFile, 'w',newline='')#python3下

    for line in jsondata:#获取属性列表
        for i, dic in enumerate(json.loads(line)):
            if i == 0:
                keys = dic.keys()
                writer = csv.writer(csvfile)
                writer.writerow(keys)#将属性列表写入csv中
            else:
                writer.writerow(dic.values())
    jsondata.close()
    csvfile.close()

def main():
    inputData = InputData()
    inputData.input()

    dbUtil = DBUtil('root','root')
    dbUtil.connect('stockdatabase')

    codeStatement = "select DISTINCT stock_code from stock_all;"
    rondomCodeList =  getRondomCode(inputData.quantity, dbUtil.query(codeStatement))
    result = []
    for item in rondomCodeList:

        # 清空数据表
        sqlSentence1 = "delete from stock_classification where 1=1"
        dbUtil.execute(sqlSentence1)

        #print("item:"+item)
        statement2 = "insert into my_data (select * from stock_all, stock_classification where stock_all.stock_code = '" + item +  \
                    "' and stock_all.stock_code = stock_classification.stock_code and date BETWEEN '" \
                    + inputData.startDate + "' and '" + inputData.endDate + "');"
        print(statement2)
        dbUtil.execute(statement2)
        #print("查询内容:"+str(dbUtil.query(statement)))

        my_file = 'D:/stock/stock.csv'
        if os.path.exists(my_file):
            # 删除文件，可使用以下两种方法。
            os.remove(my_file)
        else:
            print
            'no such file:%s' % my_file

        statement3 = "select * from my_data into outfile 'D:/stock/stock.csv';"
        dbUtil.execute(statement3)

    dbUtil.close()
if __name__ == '__main__':
    main()




