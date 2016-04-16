#!/usr/bin/python
# -*- coding:utf-8 -*-

import re
from urllib import request
from urllib.error import URLError, HTTPError

class qsbk:
	url = 'http://www.qiushibaike.com/hot/'

	def get_content(self):
		req = request.Request(self.url)
		req.add_header('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36')
		with request.urlopen(req) as f:
			content = f.read().decode('utf-8')
			pattern = re.compile(r'<div class="content">(.*?)<!--.*?-->.*?</div>\s*(?!<div class="thumb">)<div class="stats">',re.S)
			items = pattern.findall(content)
			return items

qs = qsbk()

items = qs.get_content()
for i in range(5):
	print(items[i].replace('<br/>', ''))
	
