#!/usr/bin/env python
#coding=utf-8

from urlparse import urljoin
import requests
import urlparse
from bs4 import BeautifulSoup

import sqlite3

from SqliteManager import SqliteManager

from utils import pretty_print

INDEX = 'https://www.ptt.cc/bbs/movie/index.html'
NOT_EXIST = BeautifulSoup('<a>本文已被刪除</a>', 'lxml').a

#db
class PictureObj:

    def __init__(self,title,url):
        self.picTitle = title
        self.picUrl = url
        self.tableName = "tb_picture"

    def getTableSql(self):
        sql = 'create table IF NOT EXISTS {0} (ID INTEGER PRIMARY KEY,picTitle text,picUrl text);'.format(
            self.tableName)
        return sql

    def getCreateIndexSql(self):
        sql = 'CREATE UNIQUE INDEX IF NOT EXISTS picUrl ON {0} (picUrl ASC);'.format(self.tableName)
        return sql

    def getInsertSql(self):
        sql = 'REPLACE INTO {0} (picTitle,picUrl) VALUES (text,text)'.format(self.tableName,self.picTitle,self.picUrl)
        print sql
        return sql

    def getSelectSql(self):
        sql = 'select * from ' + self.tableName
        return sql

    def getDeleteAll(self):
        sql = 'delete from ' + self.tableName
        return sql

manager = SqliteManager('testDB.db')
globalPhone = PictureObj('', '')
manager.createTable(globalPhone.getTableSql())
manager.createIndex(globalPhone.getCreateIndexSql())

def get_posts_on_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')

    articles = soup.find_all('div', 'r-ent')

    posts = list()
    for article in articles:
        meta = article.find('div', 'title').find('a') or NOT_EXIST
        posts.append({
            'title': meta.getText().strip(),
            'link': meta.get('href'),
            'push': article.find('div', 'nrec').getText(),
            'date': article.find('div', 'date').getText(),
            'author': article.find('div', 'author').getText(),
	 })

    next_link = soup.find('div', 'btn-group-paging').find_all('a', 'btn')[1].get('href')

    return posts, next_link


def get_pages(num):
    page_url = INDEX
    all_posts = list()
    for i in range(num):
        posts, link = get_posts_on_page(page_url)
        all_posts += posts
        page_url = urljoin(INDEX, link)
    return all_posts


if __name__ == '__main__':
    pages = 20
    for post in get_pages(pages):
	pic = PictureObj(post['title'],post['author'])
	manager.save(pic.getInsertSql())
        pretty_print(post['push'], post['title'], post['date'], post['author'])
