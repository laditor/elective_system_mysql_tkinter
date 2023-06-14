import pymysql

def connect():
    db = pymysql.connect(host='localhost', user='root', password='admin', database='courseselection', charset='utf8')
    return db