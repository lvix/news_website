#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from flask import Flask, request, render_template, abort
from flask_sqlalchemy import SQLAlchemy 
from pymongo import MongoClient
from datetime import datetime
import os, json, operator
# MySQL
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/news'
db = SQLAlchemy(app)
# MongoDB
client = MongoClient('127.0.0.1', 27017)
mdb = client.news

class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(80))
	created_time = db.Column(db.DateTime)
	category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
	content = db.Column(db.Text)

	category = db.relationship('Category', backref=db.backref('posts', lazy='dynamic'))

	def __init__(self, title, category, content, created_time=None):
		self.title = title
		self.category = category
		if not created_time:
			self.created_time = datetime.utcnow()
		else:
			self.created_time = created_time
		self.content = content

	def __repr__(self):
		return '<Post %r>' % self.title 

	# add tag to a post
	def add_tag(self, tag_name):
		# add a Tag called tag_name to current Post in MongoDB
		try:
			tags = self.tags
			# print('tags:', tags )
			if tag_name not in tags:
				tags.append(tag_name)
				print(tags)
				mdb.news.update({'id':self.id}, {'$set':{'tags':tags}})
		except:
			print('cannot add tag')
			return

	# remove tag from a post
	def remove_tag(self, tag_name):
		# remove a Tag called tag_name from current Post in MongoDB
		try:
			tags = self.tags
			if tag_name in tags:
				tags.remove(tag_name)
				mdb.news.update({'id':self.id}, {'$set':{'tags':tags}})
		except:
			return

	# return current Post's  tags
	@property 
	def tags(self):
		try:
			m_post = mdb.news.find_one({'id':self.id})
			if m_post == None:
				new_tags = []
				new_post = {'id':self.id, 'tags':new_tags}
				mdb.news.insert_one(new_post)
				# print('insert one ', new_post)
				return new_tags
			else:
				# print('check exising tags', m_post)
				return m_post['tags']
		except:
			print('get tags error')
			return []


class Category(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80))

	def __init__(self, name):
		self.name = name

	def __repr__(self):
		return '<Category %r>' % self.name 


def get_post_items_from_db():
	plist = db.session.query(Post).all()
	nlist = []
	for po in plist:
		_ctime = datetime.strftime(po.created_time, '%Y-%m-%d %H:%M:%S')
		p_item = {'file_name':po.id, 'title':po.title, 'created_time':_ctime, 'tags':po.tags}
		nlist.append(p_item)
	return nlist 


@app.errorhandler(404)
def not_found(error):
	return render_template('404.html'), 404

@app.route('/')
def index():
	try:
		posts = get_post_items_from_db()
	except:
		abort(404)
	return	render_template('index.html', items=posts)

@app.route('/files/<filename>')
def file(filename):
	try:
		post = db.session.query(Post).filter(Post.id==str(filename)).first()
	except:
		abort(404)
	if not post:
		abort(404)

	# set variables
	title = post.title
	created_time = datetime.strftime(post.created_time, '%Y-%m-%d %H:%M:%S')
	content = post.content
	# tags = post.tags
	return render_template('file.html', title=title, created_time=created_time, content=content)