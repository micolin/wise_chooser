#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Usage:

 Author: MicoLin
 Create time: 2017-10-29
 Filename:page_crawler.py
"""

import os
import sys
import urllib
import urllib2
import logging
import configparser
import argparse

from page_objects import CityUListPage
from page_objects import CityUPersonPage

def get_page(url):
	logging.info('getting_page: %s' % (url))
	for retry in range(5):
		try:
			respon = urllib2.urlopen(url)
			page = respon.read()
			break
		except:
			logging.info('Get page error. Retry: %s / 5' % (retry + 1))
	return page

def download_personpage_cityu(config):
	list_base_url = config.get('CityU', 'list_url')
	save_dir = config.get('page', 'save_dir')

	filters = ['researcher', 'students']
	status = ['current', 'former']
	
	# TODO: Add auto logic here
	pagenum_dict = {'current_researcher': 1018,
					'current_students': 2000,
					'former_researcher': 109,
					'former_students': 222 
					}
	pagesize = 100

	list_url_tmp = "%s?filter=%s&affiliationStatus=%s&page=%s&pageSize=%s"
	
	for _filter in filters:
		for _status in status:
			page_num = (pagenum_dict["%s_%s" % (_status, _filter)] / pagesize ) + 1
			for page_idx in range(page_num):
				req_url = list_url_tmp % (list_base_url, _filter, _status, page_idx, pagesize)
				page = get_page(req_url)
				cityu_list_page = CityUListPage(page)
				
				out_dir = os.path.join(save_dir, 'cityu_list', _filter, _status) 
				filename = 'list_%s.page' % (page_idx)
				cityu_list_page.save_page(out_dir, filename)
	

def main():
	config = configparser.ConfigParser()
	config.read('./config/crawler_config')
	download_personpage_cityu(config)

if __name__ == "__main__":
	"""Logging config"""
	logging.basicConfig(level=logging.INFO,
						format='%(asctime)s %(levelname)s %(funcName)s %(lineno)d %(message)s', 
						filename='./log.spider', filemode='w')

	parser = argparse.ArgumentParser(description=__doc__,
									formatter_class=argparse.RawTextHelpFormatter)

	parser.add_argument('-f', '')

	main()
