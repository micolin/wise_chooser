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
from bs4 import BeautifulSoup

class BaseParser(object):
    
    def __init__(self, page, tags):
        self.soup = BeautifulSoup(page)
        self.page = page
        self.tags = tags

    
    def get_tag_string(self, tag):
        if tag:
            res = tag.string
            if res == None:
                res = tag.get_text()
            return res.strip()
        return None

    
    def get_tag_href(self, tag):
        if tag:
            return tag['href']
        return None

    
    def begin_parse(self):
        pass

    
    def execute(self):
        return self.begin_parse()