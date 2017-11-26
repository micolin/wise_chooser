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
import logging

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


class CityUListPage(BasePage):
	def __init__(self, page):
		super(CityUListPage, self).__init__(page)


class CityUPersonPage(BasePage):
	def __init__(self, page):
		super(CityUPersonPage, self).__init__(page)

	def parse_page(self):
		pass
	
		
		
