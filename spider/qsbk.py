#!/usr/bin/python
# -*- coding:utf-8 -*-

import re
import urllib 
from urllib import request
from email.mime.text import MIMEText
import smtplib
from email.utils import parseaddr, formataddr
from email.header import Header
import mysql.connector
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr
import poplib
import imaplib
import string
import logging
import os
import time
from datetime import datetime, timedelta
import hashlib
logging.basicConfig(level=logging.INFO)
#debug，info，warning，error

SENDEREMAIL = 'youremail@qq.com'
SENDPASSWORD = 'yourpasswd'		#QQ或163需要使用客户端密码，对于QQ来说是独立密码

AdminEMail = ['admin@qq.com']

SRVADDR = 'smtp.qq.com'
SRVPORT = 465	#465 25
POP3RECVSRCADDR = 'pop.qq.com'

UserAgent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36'
ROOTURL1 = 'http://www.qiushibaike.com/text/page/'
ROOTURL2 = 'http://www.qiushibaike.com/textnew/page/'

SQLUser = 'root'
SQLPasswd = 'yourpasswd'
SQLDataBase = 'python'

#糗百的文字段子正则表达式，如果网站改版，需要更新正则表达式
QBRegex = r'<div class="content">(.*?)<!--.*?-->.*?</div>\s*(?!.*?<div class="thumb">.*?)?<div class="stats">'
CmdRegexs = [r'.{0,3}?(add)\s*(.*?)\s*?', r'.{0,3}?(TD)\s*?', r'.{0,3}?(addme)\s*?', r'.{0,3}?(changeto)\s*(.*?)\s*?', r'.{0,3}?(sourcecode)\s*?']
HaveTwoPara = ['add', 'changeto']

AutoReplyMsg = {
'add':'	感谢您的信赖，后续每日九时许将会精彩有相关内容推送给您！',
'TD':'	退订成功！叨扰之处，请见谅！',
'addme':'	感谢您的信赖，后续每日九时许将会精彩有相关内容推送给您！',
'changeto':'	感谢您的信赖，更改邮箱操作成功',
'sourcecode':	'请至:https://github.com/nullscc/pythoncode/tree/master/spider，qsbk.py中即是主要代码'
}

Signature = '''
------------------------------
本邮件由服务器自动发送，请勿回复以下内容外的任何其他内容，如有任何建议，请发送邮件到jarves@foxmail.com
如需预定，请发送：addme
如需退订，请发送：TD
如需为您的朋友预订，请发送：add your_friend@xx.com
如需更改收取的邮件地址，请发送：changeto your_emailaddress@xx.com
如果您对python有兴趣，并想查看代码，或者在此功能上想指点以下我的，请发送：sourcecode，您会收到源代码网址
'''

class NoContentError(ValueError):
    pass

class qsbk:
	def __init__(self):
		self.PAGE = 1
		self.RootURL = ROOTURL1
		self.url = self.RootURL+str(self.PAGE)
		self.email_content = ''
		self.emails = ['']
		self.fromcmd = ''
		self.fromcmd_email = ''
		self.fromaddr = ''
		self.stdtime = datetime.now()
		self.UseROOTURL2 = False
		logging.debug('init datetime:%s' %self.stdtime)
		#self.nextsendtime = datetime(self.stdtime.year, self.stdtime.month, self.stdtime.day+1, 9, 00)
		self.nextsendtime = self.stdtime + timedelta(seconds=1)
		self.todayjoke = 0

	def query_sql(self, sqlcmd):	#连接SQL服务器，获取email地址列表
		conn = mysql.connector.connect(user=SQLUser, password=SQLPasswd, database=SQLDataBase)
		cursor = conn.cursor()
		cursor.execute(sqlcmd)
		data = cursor.fetchall()
		cursor.close()
		conn.close()
		return data

	def isnewitem(self, content):
		md5 = hashlib.md5()
		md5.update(content.encode('utf-8'))
		#print(type(md5.hexdigest()))
		#print("select md5 from md5 where md5 = '%s'" % md5.hexdigest())
		data = self.query_sql("select md5 from md5 where md5 = '%s'" % md5.hexdigest())
		if data:
			return False
		else:
			self.excute_sql("insert into md5 values('%s')" % md5.hexdigest())
			return True

	def get_content(self):
		req = request.Request(self.url)
		req.add_header('User-Agent', UserAgent)
		try:
			with request.urlopen(req) as f:
				content = f.read().decode('utf-8')
				pattern = re.compile(QBRegex, re.S)
				items = pattern.findall(content)
				for i in range(len(items)):	#后续需要考虑下正则表达式没匹配到的情况，会导致IndexError	
					if self.isnewitem(items[i]):
						self.email_content += items[i].replace('<br/>', '')
						self.todayjoke = self.todayjoke + 1
					if self.todayjoke == 5:
						self.todayjoke = 0
						self.PAGE = 1
						return self.email_content
			
				self.PAGE = self.PAGE + 1
				if self.PAGE == 36 and self.UseROOTURL2:
					self.send_content(AdminEMail, '糗事百科段子已爬尽，主进程已退出，请至服务器处理僵尸子进程')
					raise NoContentError('qiushibaike has no new content')
				if self.PAGE == 36:
					self.UseROOTURL2 = True
					self.RootURL = ROOTURL2
					self.PAGE = 1
				self.url = self.RootURL+ str(self.PAGE)
				logging.debug(self.url)
				return self.get_content()
		except urllib.error.HTTPError:
			logging.warning("urllib.error.HTTPError occured")
			return self.get_content()
						
	def _format_addr(self,s):
		name, addr = parseaddr(s)
		return formataddr((Header(name, 'utf-8').encode(), addr))

	def excute_sql(self, sqlcmd):	#连接SQL服务器，获取email地址列表
		conn = mysql.connector.connect(user=SQLUser, password=SQLPasswd, database=SQLDataBase)
		cursor = conn.cursor()
		logging.debug('in excute_sql cmd:%s' %sqlcmd)
		cursor.execute(sqlcmd)
		conn.commit()
		cursor.close()
		conn.close()

	def guess_charset(self,msg):
		charset = msg.get_charset()
		if charset is None:
		    content_type = msg.get('Content-Type', '').lower()
		    pos = content_type.find('charset=')
		    if pos >= 0:
		        charset = content_type[pos + 8:].strip()
		return charset

	def decode_str(self, s):
		value, charset = decode_header(s)[0]
		if charset:
		    value = value.decode(charset)
		return value

	# indent用于缩进显示:
	def get_info(self, msg, indent=0):
		fromcontent = ''

		if indent == 0:
			for header in ['From', 'To', 'Subject']:
				value = msg.get(header, '')
				if value:
					if header=='From':
						hdr, addr = parseaddr(value)
						self.fromaddr = addr
				
		if (msg.is_multipart()):
		    parts = msg.get_payload()
		    for n, part in enumerate(parts):
		        logging.debug('%spart %s' % ('  ' * indent, n))
		        logging.debug('%s--------------------' % ('  ' * indent))
		        self.get_info(part, indent + 1)
		else:
			content_type = msg.get_content_type()
			if content_type=='text/plain' :
				content = msg.get_payload(decode=True)
				charset = self.guess_charset(msg)
			elif content_type=='text/html':
				content = msg.get_payload(decode=True)
				charset = self.guess_charset(msg)
			if charset:
					content = content.decode(charset)
					fromcontent = content #logging.debug('%sText: %s' % ('  ' * indent, content + '...'))
			else:
				logging.debug('%sAttachment: %s' % ('  ' * indent, content_type))
			for cmdregex in CmdRegexs:
				logging.debug('cmdregex is:%s' %cmdregex)
				logging.debug('excute for cmdregex in CmdRegexs:')
				m = re.match(cmdregex, fromcontent, re.S)
				if m:
					logging.debug('%s matched' %cmdregex)
					self.fromcmd = m.group(1)
					if self.fromcmd in HaveTwoPara:
						self.fromcmd_email = m.group(2)
					break

	def handlecmd(self):
		logging.debug(self.fromcmd)
		emails = self.get_email_from_sql()
		if self.fromcmd == "add":
			if self.fromcmd_email not in emails:
				self.excute_sql("insert into qsbk values(NULL, '%s')" %self.fromcmd_email)
		elif self.fromcmd == "TD":
			if self.fromaddr in emails:
				self.excute_sql("delete from qsbk where email = '%s'" %self.fromaddr)
		elif self.fromcmd == "addme":
			if self.fromaddr not in emails:
				self.excute_sql("insert into qsbk values(NULL, '%s')" %self.fromaddr)
		elif self.fromcmd == "changeto":
			if self.fromcmd_email not in emails:
				self.excute_sql("update qsbk set email = '%s' where email = '%s'" %(self.fromcmd_email, self.fromaddr))
		
		ReplyEmail = ['']
		ReplyEmail.append(self.fromaddr)
		logging.debug(ReplyEmail)
		self.send_content(ReplyEmail, AutoReplyMsg[self.fromcmd]+Signature)

	def pop3recv_handle(self):
		while True:		
			try:
				server = poplib.POP3(POP3RECVSRCADDR)
				# 可以打开或关闭调试信息:
				#server.set_debuglevel(1)

				server.user(SENDEREMAIL)
				server.pass_(SENDPASSWORD)
				logging.debug("normal excute")
				resp, mails, octets = server.list()
				index = len(mails)

				resp, lines, octets = server.retr(index)
				msg_content = b'\r\n'.join(lines).decode('utf-8')
				msg = Parser().parsestr(msg_content)
				self.get_info(msg)
				logging.debug('from info:%s %s %s'%(self.fromaddr, self.fromcmd, self.fromcmd_email))
				if self.fromcmd:
					self.handlecmd()
				#server.dele(index)
			except poplib.error_proto:
				logging.error("poplib.error_proto occured")
			finally:
				time.sleep(2)
			server.quit()	
		

	def get_email_from_sql(self):
		data = self.query_sql('select email from qsbk')
		for email in data:
			self.emails.append(email[0])
		return self.emails

	def send_content(self, TOADDR, content):
		self.RootURL = ROOTURL1
		try:
			logging.debug(TOADDR)
			msg = MIMEText(content, 'plain', 'utf-8')
			msg['From'] = self._format_addr('一个快乐的小2B<%s>' % SENDEREMAIL)
			msg['To'] = self._format_addr('一群快乐的小2B<%s>' % TOADDR)
			msg['Subject'] = Header('给快乐小2B的问候', 'utf-8').encode()

			smtp_server = SRVADDR
			server = smtplib.SMTP(SRVADDR, SRVPORT) #不支持SSL的应该使用SMTP
			#server.set_debuglevel(1)
			server.login(SENDEREMAIL, SENDPASSWORD)
			server.sendmail(SENDEREMAIL, TOADDR, msg.as_string())
		except smtplib.SMTPDataError:
			logging.info('smtplib.SMTPDataError occur')
		finally:
			self.email_content = ''
			server.quit()

qs = qsbk()
	
if 1:
	if os.fork() == 0:  #调用fork创建子进程，如果父进程挂掉，子进程(收取邮件进程)还是会继续运行
		qs.pop3recv_handle()
	else:
		try:
			while True:
					logging.debug('main process')
					time.sleep(1)
					if (datetime.now() - qs.nextsendtime) >  timedelta(seconds=1):
						try:
							qs.send_content(qs.get_email_from_sql(), qs.get_content()+Signature)
						except smtplib.SMTPException:
							logging.info('smtplib.SMTPException occured')
						finally:
							qs.nextsendtime = datetime.now() + timedelta(seconds=5) #minutes
							#qs.nextsendtime = qs.nextsendtime + timedelta(days=1)
		except NoContentError as e:
			logging.error(e)
