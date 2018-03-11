#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Usage:

 Author: ljt
 Create time: 2017-12-10
 Filename:page_parser.py
"""

import os
import sys
import urllib
import urllib2
import logging
import configparser
import argparse
import re

from bs4 import BeautifulSoup

sys.path.append(os.path.dirname(os.getcwd()))

from page_crawler import get_page
from base_parser import BaseParser
import re

class ResearchParser(BaseParser):
    def __init__(self, page, tags):
        super(ResearchParser, self).__init__(page, tags)

    #获取title
    def get_title(self, cur_tag):
        tag_title_link = cur_tag.find(class_='link')
        title = self.get_tag_string(tag_title_link)
        title_link = tag_title_link['href']
        return (title, title_link)

    def get_persons(self, cur_tag):
        tags_person = cur_tag.find_all(class_ = 'link person')
        persons = []
        for tag in tags_person:
            each_person = {}
            each_person['name'] = self.get_tag_string(tag)
            each_person['person_link'] = tag['href']
            persons.append(each_person)
        return persons

    def get_date(self, cur_tag):
        tag_date = cur_tag.find(class_ = 'date')
        return self.get_tag_string(tag_date)


    def get_journal(self, cur_tag):
        journal_info = {}
        #tag_journal = cur_tag.find(class_ = "journal")
        tag_journal = cur_tag.find(rel = "Journal")
        journal_info['journal'] = self.get_tag_string(tag_journal)
        journal_info['journal_link'] = ""
        if tag_journal:
            journal_info['journal_link'] = tag_journal['href']
            #tag_journal_link = tag_journal.find(class_ = "link")
            #journal_info['journal_link'] = tag_journal_link['href']

        tag_journal_volume = cur_tag.find(class_ = 'volume')
        journal_info['journal_volume'] = self.get_tag_string(tag_journal_volume)
        tag_journal_pages = cur_tag.find(class_ = 'pages')
        journal_info['journal_pages'] = self.get_tag_string(tag_journal_pages)
        tag_journal_number = cur_tag.find(class_ = 'journalnumber')
        journal_info['journal_number'] = self.get_tag_string(tag_journal_number)
        return journal_info

    # param
    # return list(txt_list, url_list)
    def begin_parse(self):
        res = []
        #遍历每个需要解析的标签，解析出原始文本和文本中包括的链接
        for key in self.tags:
            ret = self.soup.find_all(class_ = re.compile(self.tags[key]))
            if ret:
                for row in ret:
                    tmp = {}
                    cur_tag = row
                    #获取research的title及其链接
                    cur_title = self.get_title(cur_tag)
                    tmp['title'] = cur_title[0]
                    tmp['title_link'] = cur_title[1]

                    #获取research的作者及其链接
                    cur_persons = self.get_persons(cur_tag)
                    tmp['authors'] = cur_persons

                    #获取research发表的日期
                    cur_date = self.get_date(cur_tag)
                    tmp['date'] = cur_date

                    #获取research发表的会议或者期刊
                    cur_journal = self.get_journal(cur_tag)
                    tmp['journal'] = cur_journal['journal']
                    tmp['journal_link'] = cur_journal['journal_link']
                    tmp['journal_volume'] = cur_journal['journal_volume']
                    tmp['journal_pages'] = cur_journal['journal_pages']
                    tmp['journal_number'] = cur_journal['journal_number']
                    logging.info("\n-------key : %s-----\n" % key)

                    #print tmp
                    res.append(tmp)
            else:
                logging.info("key %s class tag[%s] not found in page" % (key, self.tags[key]))
        #print len(res)
        return {"papers":res}


