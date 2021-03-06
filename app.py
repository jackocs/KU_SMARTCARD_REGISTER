#! /usr/bin/env python

from flask import Flask, render_template
import csv
import time

app = Flask(__name__)

@app.route('/')
def index():
	try:
		date = time.strftime('%d%m%y%H%M%S')
		f = open('./static/cn.csv', 'r')
		with f:
			reader = csv.reader(f)
			for row in reader:
				print(row)
				#for e in row:
				#	print(e)
			return render_template('index.html', cn=row[0],en_name=row[1],datetime=date)
	except Exception as e:
		print("File no accessible")
	finally:
		f.close()
"""
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', 404)
"""
if __name__ == '__main__':
  app.debug = True
  app.run(host='0.0.0.0', port=8000)
