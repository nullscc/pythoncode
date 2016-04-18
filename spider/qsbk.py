#!/usr/bin/python
# -*- coding:utf-8 -*-
'''
时间：2016年4月18日
开发环境：Python 3.4.3 [GCC 4.8.4] on linux

功能：
	程序分为两个进程	
	主进程：每天上午九点，从糗事百科网站每天爬取不重复的5个文字版本段子，并发送到数据库中已经记录在案的邮件列表中的用户
	子进程：每隔5秒钟收取一次邮件，并处理后删除，所以不要用正常使用的邮箱运行本脚本，重要邮件删除了别怪我哦。

说明：
	本程序使用的数据库为：mySQL,数据库名：python，接收邮件列表表名为：qsbk(列名email)，段子md5存储表名为：md5(列名md5)
	收取的邮件使用的pop3协议，若使用IMAP4协议可能就不用一直删除邮件了，可惜有点复杂，没那么多时间去研究了～
注意：
	运行本脚本后，邮箱收件箱会全部被删除，所以请务必使用一个不使用的空邮箱，推荐QQ邮箱，或者自己搭建一个
	由于网易邮箱的反垃圾功能，貌似经常会发送或者接收失败
	由于主进程和子进程几乎是分开的，所以没有处理父进程，如果父进程突然挂掉，子进程会编程僵尸进程
	代码应该分成三个类的(邮件类，数据库操作类，爬虫类)，懒得再去改了
	类中的get_info函数每次会运行两次，增加了系统开销有时间再来优化
	实现可能略臃肿，后面有大把时间的时候再来看吧。
	
有任何建议或者指导可发送邮件到：jarves@foxmail.com
'''

#用的模块有点多～
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
import string
import logging
import os
import time
from datetime import datetime, timedelta
import hashlib
logging.basicConfig(level=logging.ERROR) #级别定义
#debug，info，warning，error

SENDEREMAIL = 'youremail@qq.com'	#主要发送、接收邮箱
SENDPASSWORD = 'yourpasswd'			#邮箱密码，QQ或163需要使用客户端密码，对于QQ来说是独立密码

AdminEMail = ['admin@qq.com']	#当糗事百科没有不重复的段子可爬，则发送邮件到此邮箱进行提醒

SRVADDR = 'smtp.qq.com'				#邮箱的SMTP服务器地址
SRVPORT = 465						#邮箱的SMTP端口一般为465(SSL)25(非SSL)
POP3RECVSRCADDR = 'pop.qq.com'		#邮箱的POP3服务器地址

#伪装为浏览器的header,提取自ubuntu中的chrome浏览器
UserAgent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36'

#糗事百科文字版段子网址，如果不能从ROOTURL1中爬到5个不重复的段子，那么转到ROOTURL2爬取
ROOTURL1 = 'http://www.qiushibaike.com/text/page/'
ROOTURL2 = 'http://www.qiushibaike.com/textnew/page/'

SQLUser = 'root'			#SQL用户名
SQLPasswd = 'yourpasswd'		#SQL密码
SQLDataBase = 'python'		#SQL的database名
SQLEailListTable = 'qsbk'	#SQL的邮件列表表名
SQLEailListColumn = 'email' #SQL的邮件列表表中列名
SQLContentMd5Table = 'md5'	#SQL的段子md5表名md5
SQLContentMd5Column = 'md5'	#SQL的段子的md5的表中列名

#糗百的文字段子正则表达式，如果网站改版，需要更新正则表达式，本来想去掉图片段子的，但是正则表达式匹配有问题，以下只是取每一页的所有段子内容
QBRegex = r'<div class="content">(.*?)<!--.*?-->.*?</div>\s*(?!.*?<div class="thumb">.*?)?<div class="stats">'

#服务代码正则表达式，允许用户空格等的输入错误
CmdRegexs = [r'.{0,3}?(addme)\s*?', r'.{0,3}?(TD)\s*?', r'.{0,3}?(add)\s*(.*?)\s*?', r'.{0,3}?(changeto)\s*(.*?)\s*?', r'.{0,3}?(sourcecode)\s*?']

#辅助作用，避免没有group(2)的CmdRegexs报错
HaveTwoPara = ['add', 'changeto']

#自动回复的字典
AutoReplyMsg = {
'add':'	感谢您的信赖，后续每日九时许将会精彩有相关内容推送给您！',
'TD':'	退订成功！叨扰之处，请见谅！',
'addme':'	感谢您的信赖，后续每日九时许将会精彩有相关内容推送给您！',
'changeto':'	感谢您的信赖，更改邮箱操作成功',
'sourcecode':	'请至:https://github.com/nullscc/pythoncode/tree/master/spider，qsbk.py中即是主要代码'
}

#自动发送的段子或回复的签名
Signature = '''
------------------------------
本邮件由服务器自动发送，请勿回复以下内容外的任何其他内容，如有任何建议，请发送邮件到jarves@foxmail.com
如需预定，请发送：addme
如需退订，请发送：TD
如需为您的朋友预订，请发送：add your_friend@xx.com
如需更改收取的邮件地址，请发送：changeto your_emailaddress@xx.com (某些企业邮箱服务器可能会拦截)
如果您对python有兴趣，并想查看代码，或者在此功能上想指点以下我的，请发送：sourcecode，您会收到源代码网址
'''

#当糗事百科无非重复的段子可爬时，raise此错误
class NoContentError(ValueError):
    pass

class qsbk:
	def __init__(self):
		self.PAGE = 1
		self.RootURL = ROOTURL1
		self.url = self.RootURL+str(self.PAGE)
		self.email_content = ''
		self.fromcmd = ''
		self.fromcmd_email = ''
		self.fromaddr = ''
		self.stdtime = datetime.now()
		self.UseROOTURL2 = False
		logging.debug('init datetime:%s' %self.stdtime)
		self.nextsendtime = datetime(self.stdtime.year, self.stdtime.month, self.stdtime.day+1, 9, 00)
		#self.nextsendtime = self.stdtime + timedelta(seconds=10)
		self.todayjoke = 0

	def query_sql(self, sqlcmd):	#连接数据库，执行查询命令
		conn = mysql.connector.connect(user=SQLUser, password=SQLPasswd, database=SQLDataBase)
		cursor = conn.cursor()
		cursor.execute(sqlcmd)
		data = cursor.fetchall()
		cursor.close()
		conn.close()
		return data

	def isnewitem(self, content):	#判断是否是新段子
		md5 = hashlib.md5()
		md5.update(content.encode('utf-8'))
		data = self.query_sql("select %s from %s where %s = '%s'" %(SQLContentMd5Column, SQLContentMd5Table, SQLContentMd5Column, md5.hexdigest()))
		if data:
			return False
		else:
			self.excute_sql("insert into %s values('%s')" %(SQLContentMd5Table, md5.hexdigest()))
			return True

	def get_content(self):			#获取5个段子内容
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
			logging.debug("urllib.error.HTTPError occured")
			return self.get_content()
						
	def _format_addr(self,s):	#解析地址
		name, addr = parseaddr(s)
		return formataddr((Header(name, 'utf-8').encode(), addr))

	def excute_sql(self, sqlcmd):	#连接SQL服务器，执行更改操作
		conn = mysql.connector.connect(user=SQLUser, password=SQLPasswd, database=SQLDataBase)
		cursor = conn.cursor()
		logging.debug('in excute_sql cmd:%s' %sqlcmd)
		cursor.execute(sqlcmd)
		conn.commit()
		cursor.close()
		conn.close()

	def guess_charset(self,msg):	#猜测邮件内容的字符编码
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

	
	def get_info(self, msg, indent=0):	#收取邮件时获取发件人及根据CmdRegexs解析服务命令，indent用于缩进显示:
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
	def islegalemail(self, email):
		if re.match(r'([\w\d]+.)*[\w\d]+@[\w\d]+\.(com|org)', email):
			return True
		else:
			return False
	def handlecmd(self):	#处理CmdRegexs解析服务命令并回复给请求人
		logging.debug(self.fromcmd)
		emails = self.get_email_from_sql()
		ReplyEmail = ['']
		ReplyEmail.append(self.fromaddr)
		if self.fromcmd == "add":	#暂未考虑无效邮箱问题
			if self.fromcmd_email not in emails:
				if self.islegalemail(fromcmd_email):
					self.excute_sql("insert into %s values(NULL, '%s')" %(SQLEailListTable, self.fromcmd_email))
					self.send_content(ReplyEmail, AutoReplyMsg[self.fromcmd]+Signature)
				else:
					self.send_content(ReplyEmail, '	对不起，您所要预定的email地址不合法。'+Signature)
			else:
				self.send_content(ReplyEmail, '	用户早已预定推送内容，无须重复预定。'+Signature)
		elif self.fromcmd == "TD":
			if self.fromaddr in emails:
				self.excute_sql("delete from %s where %s = '%s'" %(SQLEailListTable, SQLEailListColumn, self.fromaddr))
				self.send_content(ReplyEmail, AutoReplyMsg[self.fromcmd]+Signature)
			else:
				self.send_content(ReplyEmail, '	用户还未预定或早已退订,无须退订。'+Signature)
		elif self.fromcmd == "addme":
			logging.debug('addme:%s' %self.fromaddr)
			logging.debug('emails:%s' %emails)
			if self.fromaddr not in emails:
				self.excute_sql("insert into %s values(NULL, '%s')" %(SQLEailListTable, self.fromaddr))
				self.send_content(ReplyEmail, AutoReplyMsg[self.fromcmd]+Signature)
			else:
				self.send_content(ReplyEmail, '	您早已预定推送内容，无须重复预定。'+Signature)
		elif self.fromcmd == "changeto":
			if self.fromaddr in emails:
				if self.fromcmd_email not in emails:
					if self.islegalemail(fromcmd_email):
						self.excute_sql("update %s set %s = '%s' where %s = '%s'" %(SQLEailListColumn, SQLEailListColumn, SQLEailListTable, self.fromcmd_email, self.fromaddr))
						self.send_content(ReplyEmail, AutoReplyMsg[self.fromcmd]+Signature)
					else:
						self.send_content(ReplyEmail, '	对不起，您所要改变的email地址不合法，推送内容仍将发送到原email地址'+Signature)
				else:
					self.send_content(ReplyEmail, '	您所指定的邮箱已经在地址列表中，请另指定一个邮箱。'+Signature)
			else:
				self.send_content(ReplyEmail, '	您还未预定推送，请先预定。'+Signature)
		self.fromcmd = ''

	def pop3recv_handle(self):	#使用POP3协议收取邮件
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
					server.dele(index)
			except poplib.error_proto:
				logging.error("poplib.error_proto occured")
			finally:
				time.sleep(10)
			server.quit()	
		

	def get_email_from_sql(self):	#从数据库查询用户邮件列表
		emails = ['']
		data = self.query_sql('select %s from %s' %(SQLEailListColumn, SQLEailListTable))
		for email in data:
			emails.append(email[0])
		return emails

	def send_content(self, TOADDR, content):	#发送邮件，参数为([收件人列表], "要发送的邮件内容")
		self.RootURL = ROOTURL1
		try:
			logging.debug(TOADDR)
			msg = MIMEText(content, 'plain', 'utf-8')
			msg['From'] = self._format_addr('一个快乐的小2B<%s>' % SENDEREMAIL)
			msg['To'] = self._format_addr('一群快乐的小2B<%s>' % TOADDR)
			msg['Subject'] = Header('给快乐小2B的问候', 'utf-8').encode()

			server = smtplib.SMTP_SSL(SRVADDR, SRVPORT) #不支持SSL的应该使用SMTP
			#server.set_debuglevel(1)
			server.login(SENDEREMAIL, SENDPASSWORD)
			server.sendmail(SENDEREMAIL, TOADDR, msg.as_string())
		except smtplib.SMTPDataError:
			logging.error('smtplib.SMTPDataError occur')
		finally:
			self.email_content = ''
			server.quit()

qs = qsbk()

if os.fork() == 0:  #调用fork创建子进程，如果父进程挂掉，子进程(收取邮件进程)还是会继续运行
	qs.pop3recv_handle()
else:
	try:
		while True:
				logging.debug('main process')
				sleeptime = (qs.nextsendtime - datetime.now()).total_seconds() + 1	#计算出睡眠时间
				logging.info(sleeptime)
				time.sleep(sleeptime)
				if (datetime.now() - qs.nextsendtime) >  timedelta(seconds=1):
					try:
						qs.send_content(qs.get_email_from_sql(), qs.get_content()+Signature) #发送包括段子内容的邮件
					except smtplib.SMTPException:	#收取错误，使程序继续运行
						logging.error('smtplib.SMTPException occured')
					finally:
						logging.debug('nextsendtime added~~~~~~~~~~~~')
						#qs.nextsendtime = datetime.now() + timedelta(minutes=1) #minutes
						qs.nextsendtime = qs.nextsendtime + timedelta(days=1)
	except NoContentError as e:	#当没有新段子时，采集错误并退出主进程
		logging.error(e)

