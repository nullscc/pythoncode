#!/usr/bin/python
# -*- coding:utf-8 -*-

import re
from urllib import request
from urllib.error import URLError
from email.mime.text import MIMEText
import smtplib
from email.utils import parseaddr, formataddr
from email.header import Header
import mysql.connector

SENDEREMAIL = 'yourmail@qq.com'
SENDPASSWORD = 'youpasswd'		#QQ或163需要使用客户端密码，对于QQ来说是独立密码


SRVADDR = 'smtp.qq.com'
SRVPORT = 465

UserAgent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36'
RootURL = 'http://www.qiushibaike.com/hot/'

SQLUser = 'root'
SQLPasswd = 'passwd'
SQLDataBase = 'python'

#糗百的文字段子正则表达式，如果网站改版，需要更新正则表达式
QBRegex = r'<div class="content">(.*?)<!--.*?-->.*?</div>\s*(?!.*?<div class="thumb">.*?)?<div class="stats">'

class qsbk:
	def __init__(self):
		self.url = RootURL
		self.email_content = ''
		self.emails = [SENDEREMAIL]

	def get_content(self):
		req = request.Request(self.url)
		req.add_header('User-Agent', UserAgent)
		with request.urlopen(req) as f:
			content = f.read().decode('utf-8')
			pattern = re.compile(QBRegex, re.S)
			items = pattern.findall(content)
			for i in range(5):	#后续需要考虑下正则表达式没匹配到的情况，会导致IndexError
				self.email_content += items[i].replace('<br/>', '')
			return self.email_content

	def _format_addr(self,s):
		name, addr = parseaddr(s)
		return formataddr((Header(name, 'utf-8').encode(), addr))

	def get_emailaddr(self):	#连接SQL服务器，获取email地址列表
		conn = mysql.connector.connect(user=SQLUser, password=SQLPasswd, database=SQLDataBase)
		cursor = conn.cursor()
		cursor.execute('select email from qsbk')
		data = cursor.fetchall()
		cursor.close()
		conn.close()
		for email in data:
			self.emails.append(email[0])
		return self.emails
		

	def send_content(self):
		TOADDR = self.get_emailaddr()
		msg = MIMEText(self.get_content(), 'plain', 'utf-8')
		msg['From'] = self._format_addr('一个快乐的小2B<%s>' % SENDEREMAIL)
		msg['To'] = self._format_addr('一群快乐的小2B<%s>' % TOADDR)
		msg['Subject'] = Header('给快乐的小2B的问候', 'utf-8').encode()
		smtp_server = SRVADDR
		server = smtplib.SMTP_SSL(SRVADDR, SRVPORT) #不支持SSL的应该使用SMTP
		server.set_debuglevel(1)
		server.login(SENDEREMAIL, SENDPASSWORD)
		server.sendmail(SENDEREMAIL, TOADDR, msg.as_string())
		server.quit()

qs = qsbk()
qs.send_content()
'''
try:
	qs.send_content()
except BaseException:
	print('error occured')
'''
