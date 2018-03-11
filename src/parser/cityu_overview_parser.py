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

class OverViewParser(BaseParser):
    def __init__(self, page, tags):
        super(OverViewParser, self).__init__(page, tags)

    # param class tag
    # return list(res, hrefs)
    def get_raw_content(self, tag):
        res = [];
        hrefs = []
        for child in tag.descendants:
            try:
                #获取原始内容
                #有子标签就获取其中的链接
                #没有子标签就是原始文本了
                contents = child.contents
                for cont in contents:
                    #获取链接
                    try:
                        #href = cont['href']
                        href = self.get_tag_href(cont)
                        hrefs.append(href)
                    except:
                        continue
            except:
                raw = child.string.strip()
                if raw:
                    res.append(raw)
        return [res,hrefs]

    #用来获取一些固定字段，名字，电话之类的
    def get_tag_text(self, class_name):
        tag = self.soup.find(class_ = class_name)
        return self.get_tag_string(tag)

    #获取职称
    def get_persontop_list(self, cur_tag):
        persontop = []
        if cur_tag == None:
            return persontop
        tags_li = cur_tag.find_all('li')
        for tag in tags_li:
            cur_jobtitle = {}
            tag_title = tag.find(class_ = 'jobtitle')
            title = self.get_tag_string(tag_title)
            if title != '':
                cur_jobtitle['title'] = title.replace(",", "")
                tag_org = tag.find(rel = 'Organisation')
                cur_jobtitle['department'] = self.get_tag_string(tag_org)
                cur_jobtitle['department_link'] = self.get_tag_href(tag_org)
                persontop.append(cur_jobtitle)

        #persontop['jobtitle'] = self.get_tag_string(cur_tag)
        #tag_organisation = cur_tag.find(rel = 'Organisation')
        #persontop['organisation'] = self.get_tag_href(tag_organisation) #['href']
        return persontop

    #获取我也不知道是啥的东西，哈哈哈
    def get_author_ids(self, cur_tag):
        res = []
        if cur_tag == None:
            return res
        tags_li = cur_tag.find_all('li')
        for tag in tags_li:
            tmp = {}
            tmp['field'] = self.get_tag_string(tag)
            tag_a = tag.find('a')
            if tag_a:
                tmp['field_link'] = tag_a['href']
            res.append(tmp)
        return res

    #每个部分都有对应的sunheader和textblock，是一一对应的
    def get_overview(self, cur_tag):
        res = []
        if cur_tag == None:
            return res
        tags_subheaders = cur_tag.find_all(class_ = 'subheader')
        tags_textblock = cur_tag.find_all(class_ = 'textblock')
        len_subs = len(tags_textblock)
        for i in range(len_subs):
            try:
                tmp = {}
                tmp['subheader'] = self.get_tag_string(tags_subheaders[i])
                #里面还有li分行展示的内容，用特殊符号分割一下，链接就不管了 太麻烦了
                tags_li = tags_textblock[i].find_all('li')
                if tags_li:
                    text_li = []
                    for li in tags_li:
                        text_li.append(self.get_tag_string(li))
                    tmp['textblock'] = "*".join(text_li)
                else:
                    tmp['textblock'] = self.get_tag_string(tags_textblock[i])
                res.append(tmp)
            except:
                print len(tags_subheaders)
        return res

    # param
    # return list(txt_list, url_list)
    def begin_parse(self):
        res = {}
        
        #获取姓名
        res['name'] = self.get_tag_text(self.tags['personname'])
        res['gender'] = -1
        res['school'] = ""
        res['category'] = ""
        res['qualifications'] = self.get_tag_text(self.tags['qualifications'])
        
        #获取persontop-list
        tag_persontop_list = self.soup.find(class_ = self.tags['persontop'])
        res['jobtitle'] = self.get_persontop_list(tag_persontop_list)

        #获取address
        tag_address = self.soup.find(class_ = self.tags['address'])
        #res['address'] = tag_address.text.strip()
        res['address'] = self.get_tag_string(tag_address)

        #获取phone
        tag_phone = self.soup.find(class_ = self.tags['phone'])
        res['phone'] = self.get_tag_string(tag_phone)

        #获取邮箱
        tag_mail = self.soup.find(class_ = self.tags['mail'])
        res['mail'] = self.get_tag_string(tag_mail)

        #解析orcid和scopus
        tag_author_ids = self.soup.find(class_ = self.tags['author_ids'])
        author_ids = self.get_author_ids(tag_author_ids)
        for row in author_ids:
            ind_Orc = row['field'].find("ORCID")
            ind_Sco = row['field'].find("Scopus")
            if ind_Orc >= 0:
                res['ORCID'] = row['field_link']
                continue
            if ind_Sco >= 0:
                res['scopus_link'] = row['field_link']
                continue

        #解析简介
        tag_overview = self.soup.find(class_ = self.tags['overview'])
        res['overview'] = self.get_overview(tag_overview)

        return res

