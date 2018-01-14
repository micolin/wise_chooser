#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Usage:

 Author: MicoLin
 Create time: 2017-10-29
 Filename:objects.py
"""

import os
import sys
import json
import logging
import argparse
import configparser

from bs4 import BeautifulSoup as bs

class BasePage(object):
	def __init__(self, page):
		self.page = page
	
	def save_page(self, out_dir, filename):
		if not os.path.exists(out_dir):
			os.makedirs(out_dir)
		
		save_path = os.path.join(out_dir, filename)
		logging.info("Saving page to file path: %s" % (save_path))
		with open(save_path, 'w') as fin:
			fin.write(self.page)
	
	def load_page(self, file_path):
		self.page = ''
		for line in open(file_path, 'r'):
			self.page += line.strip()

class CityUListPage(BasePage):
	def __init__(self, page):
		super(CityUListPage, self).__init__(page)
		self.person_list = []
	
	def parse(self):
		logging.info("Parsing page info")
		_page_soup = bs(self.page, 'lxml')
		person_list = _page_soup.find_all('li', class_='portal_list_item')
		
		for _person_li in person_list:
			person_info = {}
			person_info['img'] = _person_li.a.span.img['src']
			
			info_node = _person_li.div.children
			for node in info_node:
				node_class = ' '.join(node['class'])
				if node_class == 'title':
					person_info['name'] = node.a.span.get_text()
					person_info['personal_page'] = node.a['href']
				elif node_class == 'relations email':
					try:
						person_info['email'] = node.li.a.span.get_text()
					except:
						person_info['email'] = ''
				elif node_class == 'relations organisations':
					try:
						person_info['department'] = node.li.a.span.get_text()
						person_info['department_page'] = node.li.a['href']
					except:
						person_info['department'] = ''
						person_info['department_page'] = ''
				elif node_class == 'type':
					try:
						person_info['extra_info'] = node.get_text()
					except:
						person_info['extra_info'] = ''
			self.person_list.append(person_info)
	
	def dump_to_file(self, out_dir, filename):
		logging.info("Dumping list info to file : %s" % (os.path.join(out_dir, filename)))
		if not os.path.exists(out_dir):
			logging.info('No such direction: %s. Creat it!' % (out_dir))
			os.makedirs(out_dir)

		writer = open(os.path.join(out_dir, filename), 'w')
		for info in self.person_list:
			writer.write("%s\n" % json.dumps(info))


class CityUPersonPage(BasePage):
	def __init__(self, page):
		super(CityUPersonPage, self).__init__(page)

	def parse_page(self):
		pass
	
def unittest():
	test_file = "/Users/baidu/Documents/projects/academic_ranking/pages/cityu_list/researcher/current/list_0.page"
	cityu_list_page = CityUListPage(None)
	cityu_list_page.load_page(test_file)
	cityu_list_page.parse()
	cityu_list_page.dump_to_file('./', 'test_file')

def main(args):
	file_list = os.listdir(args.page_dir)
	for _file in file_list:
		cityu_list_page = CityUListPage(None)
		cityu_list_page.load_page(os.path.join(args.page_dir, _file))
		cityu_list_page.parse()
		out_dir  = os.path.join(args.out_dir, '/'.join(args.page_dir.split('/')[-2:]))
		cityu_list_page.dump_to_file(out_dir, _file)

if __name__ == "__main__":
	"""Logging config"""
	logging.basicConfig(level=logging.INFO,
						format='%(asctime)s %(levelname)s %(funcName)s %(lineno)d %(message)s')

	parser = argparse.ArgumentParser(description=__doc__,
									formatter_class=argparse.RawTextHelpFormatter)
	parser.add_argument('-d', '--page_dir', required=True, help='Directory of pages')
	parser.add_argument('-o', '--out_dir', required=True, help='Directory of output')
	parser.add_argument('-u', '--university', required=True, help='Parsing University name')
	args = parser.parse_args()
	main(args)
