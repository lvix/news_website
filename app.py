#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from flask import Flask, request, render_template, abort
from datetime import datetime
import os, json, operator
# classes
class ArticleList(object):
	"""
	display the jason files in ~/files/
	"""
	article_list_json_path = '/home/shiyanlou/news/article_list.json'
	article_json_dir = '/home/shiyanlou/files'

	def __init__(self):
		# print('start!')
		self.article_list = self.update_article_list()
		# print(self.get_article_list())

	def get_article_list(self):
		art_list = self.load_article_list_json()
		return art_list[:-1]

	def load_article_list_json(self):
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
				if (time_now - last_time).total_seconds() > 300:
					return self.update_article_list()
				else:
					return new_article_list
			except IOError:
				# abort(404)
				return 

	def update_article_list(self):
		json_file_list = self._get_json_file_dirlist()
		# print(json_file_list)
		try:
			# read basic information in article jsons
			new_article_list = self._read_json_basic_info(json_file_list)
			# sort
			new_article_list = self._sort_json_list_by_time(new_article_list)
			
			# add time_stamp
			time_stamp = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
			new_article_list.append({'last_update_time':time_stamp})

			# dump json to file 
			# print('dump:')
			# print(self.article_list_json_path)
			with open(self.article_list_json_path, 'w') as list_file:
				list_file.write(json.dumps(new_article_list))

			return new_article_list
		except IOError:
			return 

	def _read_json_basic_info(self, json_file_list):
		article_info_list = []
		try:
			for js in json_file_list:
				json_path = '{}/{}.json'.format(self.article_json_dir, js)
				# print(json_path)
				with open(json_path, 'r') as json_file:
					article = json.loads(json_file.read())
					article_info_list.append({'title':article['title'], 
											'file_name':js, 
											'created_time':article['created_time']})
			return article_info_list
		except:
			# print('cannot read jsons')
			return 
	def _get_json_file_dirlist(self):
		try:
			file_list = os.listdir(self.article_json_dir)
			json_list = []
			for f_name in file_list:
				if f_name[-5:] == '.json':
					json_list.append(f_name[:-5])
			return json_list
		except:
			return 

	def _sort_json_list_by_time(self, j_list):
		j_list.sort(key=operator.itemgetter('created_time'))
		return j_list

	@staticmethod
	def _datetime_cmp(a, b):
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
	article_json_dir = '/home/shiyanlou/files/'

	def __init__(self, filename):
		self.filename = filename
		self.article_item = self.read_article_json()

	def read_article_json(self):
		file_path = self.article_json_dir + self.get_file_name() + '.json'
		# print(file_path)
		with open(file_path, 'r') as json_file:
			return json.loads(json_file.read())

	def get_file_name(self):
		return self.filename

	def get_article_title(self):
		return self.article_item['title']

	def get_article_created_time(self):
		return self.article_item['created_time']

	def get_article_content(self):
		content_ori = self.article_item['content']
		# print(content_ori)
		content = []
		if r'\\n' in content_ori:
			content = content_ori.split(r'\\n')
		elif r'\n' in content_ori:
			content = content_ori.split(r'\n')
		return content

alist = ArticleList()

app = Flask(__name__)

@app.errorhandler(404)
def not_found(error):
	return render_template('404.html'), 404

@app.route('/')
def index():
	try:
		items = alist.get_article_list()
	except:
		abort(404)
	# print(items)
	return	render_template('index.html', items=items)

@app.route('/files/<filename>')
def file(filename):
	try:
		article = Article(filename)
	except:
		abort(404)
	title = article.get_article_title()
	created_time = article.get_article_created_time()
	content = article.get_article_content()
	# print(content)
	return render_template('file.html', title=title, created_time=created_time, content=content)