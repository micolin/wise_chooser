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

class SupervisionParser(BaseParser):
    def __init__(self, page, tags):
        super(SupervisionParser, self).__init__(page, tags)

    def get_organisation(self, cur_tag):
        organisation = {}
        tag_organisation = cur_tag.find(rel = 'Organisation')
        organisation['organisation'] = self.get_tag_string(tag_organisation)
        organisation['organisation_link'] = tag_organisation['href']
        return organisation

    def get_persons(self, cur_tag):
        tags_person = cur_tag.find(rel = 'Person')
        person = {}
        person['name'] = self.get_tag_string(tags_person)
        person['person_link'] = tags_person['href']
        return person

    def get_period(self, cur_tag):
        tag_date = cur_tag.find(class_ = 'period')
        return self.get_tag_string(tag_date)


    # param
    # return list(txt_list, url_list)
    def begin_parse(self):
        res = []
        #遍历每个需要解析的标签，解析出原始文本和文本中包括的链接
        for key in self.tags:
            ret = self.soup.find_all(class_ = self.tags[key])
            if ret:
                for row in ret:
                    tmp = {}
                    cur_tag = row

                    cur_organisation = self.get_organisation(cur_tag)
                    tmp['organisation'] = cur_organisation

                    #获取supervision名字和link
                    cur_persons = self.get_persons(cur_tag)
                    tmp['supervision'] = cur_persons

                    #获取在校时间
                    cur_period = self.get_period(cur_tag)
                    tmp['period'] = cur_period

                    logging.info("\n-------key : %s-----\n" % key)

                    #print tmp
                    res.append(tmp)
            else:
                logging.info("key %s class tag[%s] not found in page" % (key, self.tags[key]))
        #print len(res)
        return {"supervisions":res}


