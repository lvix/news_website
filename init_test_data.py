#!/usr/bin/env python3

from app import db, Post, Category
from datetime import datetime
# sudo service mysql start
# sudo pip3 install flask_sqlalchemy, mysqlclient
# sudo pip3 install pymongo

# mysql -u root
# create database news;
# mongo
# use news;

# ./inti_test_data.py 

db.create_all()
# # ?? MySQL ????

java = Category('Java')
python = Category('Python')
post1 = Post('Hello Java', java, 'File Content - Java is cool!', datetime.utcnow())
post2 = Post('Hello Python', python, 'File Content - Python is cool!', datetime.utcnow())
db.session.add(java)
db.session.add(python)
db.session.add(post1)
db.session.add(post2)
db.session.commit()

# ?? MongoDB ????
# client = MongoClient('127.0.0.1', 27017)
# mdb = client.news
post1.add_tag('tech')
post1.add_tag('java')
post1.add_tag('linux')
post2.add_tag('tech')
post2.add_tag('python')
