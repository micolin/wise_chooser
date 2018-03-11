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
import json

from bs4 import BeautifulSoup

sys.path.append(os.path.dirname(os.getcwd()))

from page_crawler import get_page
from cityu_overview_parser    import OverViewParser
from cityu_research_parser    import ResearchParser 
from cityu_projects_parser    import ProjectsParser 
from cityu_supervision_parser import SupervisionParser 

# brief 加载解析配置
# param object config
# param string conf_name
# return dict parse_key : tag_class_name
def get_tag_conf(config, conf_name):
    tags = config.items(conf_name)
    res = {}
    for key,tag in tags:
        res[key] = tag
    return res

#获取待解析的html
def get_html_from_file(filename):
    fr = open(filename)
    lines = [line.strip() for line in fr.readlines()]
    return '\n'.join(lines)

#创建目录
def create_path(dirpath):
    if os.path.exists(dirpath):
        logging.info("%s already exists!" % dirpath)
    else:
        os.makedirs(dirpath)
        logging.info("mkdir %s success!" % dirpath)

def get_html_dirs(dir_html):
    dirs = os.listdir(dir_html)
    res = {}
    for each_dir in dirs:
        first_dir = each_dir
        res[first_dir] = []
        cur_dir = "%s/%s" % (dir_html, each_dir)
        next_dirs = os.listdir(cur_dir)
        for name in next_dirs:
            person = {}
            person['name'] = name
            person['html_list'] = []
            second_dir = "%s/%s" % (cur_dir, name)
            html_files = os.listdir(second_dir)
            for efile in html_files:
                person['html_list'].append("%s/%s" % (second_dir, efile))
            res[first_dir].append(person)
    return res


'''
    1. 加载各个待解析的配置
    2. 在首页解析四个待解析的tab url
    3. 遍历四个tab url，解析出各自的内容
'''
def main():
    #读配置，获取待解析的url和对应的tags列表

    config = configparser.ConfigParser()
    config.read('../../config/cityu_tags')


    #1.初始化源路径和目标路径
    cur_dirpath = os.path.dirname(os.getcwd())
    dir_html = "%s/parser/downloads" % cur_dirpath
    dir_output = "%s/parser/json" % cur_dirpath
    create_path(dir_output)

    #2.读取各个文件下对应的源文件，一一解析
    dir_html_list = get_html_dirs(dir_html)

    #3.加载四个tab各自的解析配置
    tags_overview    = get_tag_conf(config, 'overview')
    tags_research    = get_tag_conf(config, 'publications')
    tags_projects    = get_tag_conf(config, 'projects')
    tags_supervision = get_tag_conf(config, 'supervision')

    #4.不同的人有不同的tabs页，都枚举一下吧，简单粗暴
    target_tabs = ['overview.html', 'publications.html', 'projects.html', 'supervision.html', 'activities.html', 'prizes.html', 'theses.html']
    for first_dir, persons in dir_html_list.items():
        #if first_dir != 'cityu_researcher_current':
        #    continue
        cur_dir_output = "%s/%s" % (dir_output, first_dir)
        create_path(cur_dir_output)
        for person in persons:
            personname = person['name']
            person_json = {}
            for html in person['html_list']:
                str_html = get_html_from_file(html)
                tab_ind = -1
                for ind in range(len(target_tabs)):
                    if html.find(target_tabs[ind]) > -1:
                        tab_ind = ind
                        break
                #if ind > 3 :
                #    print personname
                #解析overview
                if tab_ind == 0:
                    parser = OverViewParser(str_html, tags_overview)
                    res_overview = parser.execute()
                    person_json.update(res_overview)
                    #print res_overview
                #解析overview
                if tab_ind == 1:
                    parser = ResearchParser(str_html, tags_research)
                    res_research = parser.execute()
                    person_json.update(res_research)
                    #print res_research
                #解析projects
                if tab_ind == 2:
                    parser = ProjectsParser(str_html, tags_projects)
                    res_projects = parser.execute()
                    person_json.update(res_projects)
                    #print res_projects
                #解析supervision
                if tab_ind == 3:
                    parser = SupervisionParser(str_html, tags_supervision)
                    res_supervision = parser.execute()
                    person_json.update(res_supervision)
                    #print res_supervision
            #print person_json
            print cur_dir_output, personname
            person_file = "%s/%s.json" % (cur_dir_output,personname)
            fopen = open(person_file, "w")
            fopen.write(json.dumps(person_json))
            fopen.close()
            #exit(0)
if __name__ == "__main__":
    """Logging config"""
    logging.basicConfig(level=logging.INFO,
            format='%(asctime)s %(levelname)s %(funcName)s %(lineno)d %(message)s',
            filename='./parse_cityu.log', filemode='w')
    main()
