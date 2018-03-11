#!/usr/bin/env python
# visit http://tool.lu/pyc/ for more information
'''
Usage:

 Author: ljt
 Create time: 2017-12-10
 Filename:page_parser.py
'''
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

class ProjectsParser(BaseParser):
    
    def __init__(self, page, tags):
        super(ProjectsParser, self).__init__(page, tags)

    
    def get_title(self, cur_tag):
        tag_title_link = cur_tag.find(class_ = 'link')
        title = self.get_tag_string(tag_title_link)
        title_link = tag_title_link['href']
        return (title, title_link)

    
    def get_persons(self, cur_tag):
        tags_person = cur_tag.find_all(class_ = 'link person')
        persons = []
        for tag in tags_person:
            each_person = { }
            each_person['name'] = self.get_tag_string(tag)
            each_person['person_link'] = tag['href']
            persons.append(each_person)
        
        return persons

    
    def get_period(self, cur_tag):
        tag_date = cur_tag.find(class_ = 'period')
        return self.get_tag_string(tag_date)

    
    def begin_parse(self):
        res = []
        for key in self.tags:
            ret = self.soup.find_all(class_ = self.tags[key])
            if ret:
                for row in ret:
                    tmp = { }
                    cur_tag = row
                    cur_title = self.get_title(cur_tag)
                    tmp['project'] = cur_title[0]
                    tmp['project_link'] = cur_title[1]
                    cur_persons = self.get_persons(cur_tag)
                    tmp['members'] = cur_persons
                    cur_period = self.get_period(cur_tag)
                    tmp['period'] = cur_period
                    logging.info('\n-------key : %s-----\n' % key)
                    res.append(tmp)
                
            logging.info('key %s class tag[%s] not found in page' % (key, self.tags[key]))
        
        return {
            'projects': res }