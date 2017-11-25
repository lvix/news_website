#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from flask import Flask, request, render_template
from datetime import datetime
import os, json, operator
# classes
class ArticleList(object):
	"""
	display the jason files in ~/files/
	"""
	self.article_list_json_path = '/home/shiyanlou/news/article_list.json'
	self.article_json_dir = '/home/shiyanlou/files'

	def self.__init__(self):
		self.article_list = self.update_article_list()

	def self.get_article_list(self):
		return self.article_list 

	def self.load_article_list_json(self):
		"""
		load the existing article_list.json file 
		if it doesn't exists, create a new one
		"""
		if not os.path.isfile(self.article_list_json_path):
			self.article_list = self.update_article_list()
		else:
			# load json
			try:
				with open(self.article_list_json_path, 'r') as list_file:
					self.article_list = json.loads(list_file.read())
			except IOError:
				abort(404)
				return 

	def self.update_article_list(self):
		json_list = self._get_json_file_dirlist()
		
		try:
			# read basic information in article jsons
			new_article_list = self._read_json_basic_info

			# sort
			new_article_list = self._sort_json_list_by_time(new_article_list)
			
			# add time_stamp
			time_stamp = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
			new_article_list.append({'list_update_time':time_now_str})

			# dump json to file 
			with open(self.article_list_json_path, 'r') as list_file:
				list_file.write(json.dumps(new_article_list))

			return new_article_list
		except:IOError
			return 

	def self._read_json_basic_info(self, json_list):
		article_info_list = []
		for js in json_list:
			with open('{}{}'.format(self.article_json_dir, js), 'r') as json_file:
				article = json.loads(json_file.read())
				_title = article['title']
				_created_time = 
				article_info_list.append({'title':article['title'], 
										'file_name':js, 
										'created_time':article['created_time']})
		return article_info_list

	def self._get_json_file_dirlist(self):
		try:
			file_list = os.listdir(self.article_json_dir)
			json_list = []
			for f_name in file_list:
				if f_name[-5:] == '.json':
					json_list.append(f_name)
			return json_list
		except:
			return 

	def self._sort_json_list_by_time(self, j_list):
		j_list.sort(cmp=self.datetime_cmp, key=operator.itemgetter('created_time'))
		return j_list

	@staticmethod
	def self.datetime_cmp(a, b):
		a_dt = datetime.strptime(a, '%Y-%m-%d %H:%M:%S')
		b_dt = datetime.strptime(b, '%Y-%m-%d %H:%M:%S')
		if a_dt > b_dt:
			return 1
		elif a_dt < b_dt:
			return -1 
		else:
			return 0 

class Article(object):
	"""
	

@app.route('/')
def index():
	 

@app.route('/files/<filename>')
def file(filename):
