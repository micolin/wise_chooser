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

class OverViewParser(BaseParser):
    
    def __init__(self, page, tags):
        super(OverViewParser, self).__init__(page, tags)

    
    def get_raw_content(self, tag):
        res = []
        hrefs = []
        for child in tag.descendants:
            
            try:
                contents = child.contents
                for cont in contents:
                    
                    try:
                        href = self.get_tag_href(cont)
                        hrefs.append(href)
                    continue
                    None
                    None
                    continue
                    continue

            continue
            None
            None
            raw = child.string.strip()
            if raw:
                res.append(raw)
            

        
        return [
            res,
            hrefs]

    
    def get_tag_text(self, class_name):
        tag = self.soup.find(class_ = class_name)
        return self.get_tag_string(tag)

    
    def get_persontop_list(self, cur_tag):
        persontop = []
        if cur_tag == None:
            return persontop
        tags_li = None.find_all('li')
        for tag in tags_li:
            cur_jobtitle = { }
            tag_title = tag.find(class_ = 'jobtitle')
            title = self.get_tag_string(tag_title)
            if title != '':
                cur_jobtitle['title'] = title.replace(',', '')
                tag_org = tag.find(rel = 'Organisation')
                cur_jobtitle['department'] = self.get_tag_string(tag_org)
                cur_jobtitle['department_link'] = self.get_tag_href(tag_org)
                persontop.append(cur_jobtitle)
                continue
        return persontop

    
    def get_author_ids(self, cur_tag):
        res = []
        if cur_tag == None:
            return res
        tags_li = None.find_all('li')
        for tag in tags_li:
            tmp = { }
            tmp['field'] = self.get_tag_string(tag)
            tag_a = tag.find('a')
            if tag_a:
                tmp['field_link'] = tag_a['href']
            res.append(tmp)
        
        return res

    
    def get_overview(self, cur_tag):
        res = []
        if cur_tag == None:
            return res
        tags_subheaders = None.find_all(class_ = 'subheader')
        tags_textblock = cur_tag.find_all(class_ = 'textblock')
        len_subs = len(tags_textblock)
        for i in range(len_subs):
            
            try:
                tmp = { }
                tmp['subheader'] = self.get_tag_string(tags_subheaders[i])
                tags_li = tags_textblock[i].find_all('li')
                if tags_li:
                    text_li = []
                    for li in tags_li:
                        text_li.append(self.get_tag_string(li))
                    
                    tmp['textblock'] = '*'.join(text_li)
                else:
                    tmp['textblock'] = self.get_tag_string(tags_textblock[i])
                res.append(tmp)
            continue
            None
            None
            print len(tags_subheaders)
            continue

        
        return res

    
    def begin_parse(self):
        res = { }
        res['name'] = self.get_tag_text(self.tags['personname'])
        res['gender'] = -1
        res['school'] = ''
        res['category'] = ''
        res['qualifications'] = self.get_tag_text(self.tags['qualifications'])
        tag_persontop_list = self.soup.find(class_ = self.tags['persontop'])
        res['jobtitle'] = self.get_persontop_list(tag_persontop_list)
        tag_address = self.soup.find(class_ = self.tags['address'])
        res['address'] = self.get_tag_string(tag_address)
        tag_phone = self.soup.find(class_ = self.tags['phone'])
        res['phone'] = self.get_tag_string(tag_phone)
        tag_mail = self.soup.find(class_ = self.tags['mail'])
        res['mail'] = self.get_tag_string(tag_mail)
        tag_author_ids = self.soup.find(class_ = self.tags['author_ids'])
        author_ids = self.get_author_ids(tag_author_ids)
        for row in author_ids:
            ind_Orc = row['field'].find('ORCID')
            ind_Sco = row['field'].find('Scopus')
            if ind_Orc >= 0:
                res['ORCID'] = row['field_link']
                continue
            if ind_Sco >= 0:
                res['scopus_link'] = row['field_link']
                continue
                continue
        tag_overview = self.soup.find(class_ = self.tags['overview'])
        res['overview'] = self.get_overview(tag_overview)
        return res