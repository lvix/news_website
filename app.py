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
		return self.load_article_list_json()

	def self.get_article_list_page(self, page_num=1, item_num_per_page=10)

		return self.load_article_list_json()
	def self.load_article_list_json(self):
		"""
		load the existing article_list.json file 
		if it doesn't exists or it is out-of-date create a new one
		"""
		if not os.path.isfile(self.article_list_json_path):
			return self.update_article_list()
		else:
			# load json
			try:
				with open(self.article_list_json_path, 'r') as list_file:
					new_article_list = json.loads(list_file.read())

				# checkout last_update_time
				time_now = datetime.now()
				_last_time_str = self.article_list[-1]['last_update_time']
				last_time = datetime.strptime(_last_time_str, '%Y-%m-%d %H:%M:%S')
				# if it is out-of-date
				if (time_now - last_time).totalseconds() > 300:
					return self.update_article_list()
				else:
					new_article_list
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
			new_article_list.append({'last_update_time':time_now_str})

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
		j_list.sort(cmp=self._datetime_cmp, key=operator.itemgetter('created_time'))
		return j_list

	@staticmethod
	def self._datetime_cmp(a, b):
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
	"""
	self.article_json_dir = '/home/shiyanlou/files'

	def self. __init__(self, filename):
		self.filename = filename
		self.article_item = self.get_article_json(filename)

	def self.get_article_json(self, filename):
		file_path = self.article_json_dir + self.get_article_file_name
		with open(file_path, 'r') as json_file:
			return json.loads(json_file.read())

	def self.get_file_name(self):
		return self.filename

	def self.get_article_title(self):
		return self.artitle_item['title']

	def self.get_article_created_time:(self):
		return self.artitle_item['created_time']

	def self.get_article_content:(self):
		return self.article_item['content']

alist = ArticleList()

@app.route('/')
def index():
	home_index = alist.get_article_list()

@app.route('/files/<filename>')
def file(filename):
	article = Article(filename)
	return render_template('file.html', 
							title=article.get_article_title,
							created_time=article.get_article_created_time,
							content=article.get_article_content
							)