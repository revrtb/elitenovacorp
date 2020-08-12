
from passlib.hash import bcrypt
import mysql.connector
import appconfig
import os

class DB:
	connection = None

	def __init__(self):
		try:
			host=os.environ['DBHOST']
			port=int(os.environ['DBPORT'])
			user=os.environ['DBUSER']
			pswd=os.environ['DBPSWD']
			db=os.environ['DB']
			if self.connection == None:
				self.connection = mysql.connector.connect(host=host, user=user, password=pswd, database=db, port=port)
		except Exception as e:
			print("MySQLError %s" % (str(e)))

	def check_connection(func):
		def wrap_func(*args, **kwargs):
			try:
				cursor = args[0].connection.cursor()
				cursor.execute('select 1')
				cursor.fetchall()
				cursor.close() 
				self.connection.commit()
			except Exception as e:
				host=os.environ['DBHOST']
				port=int(os.environ['DBPORT'])
				user=os.environ['DBUSER']
				pswd=os.environ['DBPSWD']
				db=os.environ['DB']
				args[0].connection = mysql.connector.connect(host=host, user=user, passwd=pswd, db=db, port=port)
			return func(*args, **kwargs)
		return wrap_func

	@check_connection
	def validate_login(self, login, pswd):
		try:
			cursor = self.connection.cursor()
			nwrk = os.environ['DOMAIN']

			cursor.execute('SELECT password from cbm_users where username="%s" and network="%s"' % (login, nwrk))
			data = cursor.fetchone()
			cursor.close()
			self.connection.commit()
			if data != None:
				return bcrypt.verify(pswd, data[0])
			return False
		except Exception as e:
			return False


	@check_connection
	def get_publishers(self):
		try:
			cursor = self.connection.cursor()
			nwrk = os.environ['DOMAIN']

			cursor.execute('SELECT id, name, subid, feedid, feedauth, delay, max, period, default_url, email, short_link, date_time  from publishers where network="%s"' % (nwrk))
			columns = [i[0] for i in cursor.description]
			data = cursor.fetchall()
			cursor.close() 
			self.connection.commit()
			return columns, data
		except Exception as e:
			return {'error': str(e)}

	@check_connection
	def get_publisher_by_feedid(self, feedid):
		try:
			cursor = self.connection.cursor()
			nwrk = os.environ['DOMAIN']

			cursor.execute('SELECT * from publishers where feedid=%s and network="%s"' % (feedid, nwrk))
			data = cursor.fetchone()
			cursor.close() 
			self.connection.commit()
			return data
		except Exception as e:
			return {'error': str(e)}

	@check_connection
	def get_publisher_by_subid(self, subid):
		try:
			cursor = self.connection.cursor()
			nwrk = os.environ['DOMAIN']

			cursor.execute('SELECT * from publishers where subid=%s and network="%s"' % (subid, nwrk))
			data = cursor.fetchone()
			cursor.close() 
			self.connection.commit()
			return data
		except Exception as e:
			return {'error': str(e)}

	@check_connection
	def get_user_by_id(self, id):
		try:
			cursor = self.connection.cursor()

			cursor.execute('SELECT id, username, email, network from cbm_users where id=%s' % (id))
			data = cursor.fetchone()
			cursor.close() 
			self.connection.commit()
			return data
		except Exception as e:
			return {'error': str(e)}

	@check_connection
	def get_user_by_uname(self, uname, nwrk):
		try:
			cursor = self.connection.cursor()

			cursor.execute('SELECT id, username, email, network from cbm_users where username="%s" and network="%s"' % (uname, nwrk))
			data = cursor.fetchone()
			cursor.close() 
			self.connection.commit()
			if data:
				return data
			else:
				return {}
		except Exception as e:
			return {'error': str(e)}

	@check_connection
	def add_publisher(self, name, subid, feedid, feedauth, delay, max, period, default_url, email, short_link):
		try:
			cursor = self.connection.cursor()
			nwrk = os.environ['DOMAIN']
			sql = 'INSERT into publishers (name, subid, feedid, feedauth, delay, max, period, default_url, email, short_link, network) values ("%s", %s, %s, "%s", %s, %s, %s, "%s", "%s", "%s", "%s");' % (name, subid, feedid, feedauth, delay, max, period, default_url, email, short_link, nwrk)
			cursor.execute(sql)
			cursor.close() 
			self.connection.commit()
			return True
		except Exception as e:
			return str(e)

	@check_connection
	def update_publisher(self, id, name, subid, feedid, feedauth, delay, max, period, default_url, email, short_link):
		try:
			cursor = self.connection.cursor()
			sql = 'UPDATE publishers set name="%s", subid=%s, feedid=%s, feedauth="%s", delay=%s, max=%s, period=%s, default_url="%s", email="%s", short_link="%s" where id=%s ;' % (name, subid, feedid, feedauth, delay, max, period, default_url, email, short_link, id)
			cursor.execute(sql)
			cursor.close() 
			self.connection.commit()
			return True
		except Exception as e:
			return str(e)

	@check_connection
	def update_publisher_dt(self, ids):
		try:
			cursor = self.connection.cursor()
			nwrk = os.environ['DOMAIN']
			idss = ','.join(ids)
			sql = 'UPDATE publishers set date_time=NOW() where feedid in (%s) and network="%s";' % (idss, nwrk)
			cursor.execute(sql)
			cursor.close() 
			self.connection.commit()
			return True
		except Exception as e:
			return str(e)

	@check_connection
	def delete_publisher(self, id):
		try:
			cursor = self.connection.cursor()
			nwrk = os.environ['DOMAIN']
			sql = 'DELETE from publishers where feedid=%s and network="%s";' % (id, nwrk)
			cursor.execute(sql)
			cursor.close() 
			self.connection.commit()
			return True
		except Exception as e:
			return str(e)

