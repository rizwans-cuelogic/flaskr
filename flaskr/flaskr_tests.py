import os
import flaskr
import unittest
import tempfile



class FlaskrTestCase(unittest.TestCase):

	def setUp(self):
		self.db_fd, flaskr.app.config[ 'DATABASE' ] = tempfile.mkstemp()
		flaskr.app.testing = True
		self.app = flaskr.app.test_client()
		with flaskr.app.app_context():
			flaskr.init_db()
	
	def tearDown(self):
		os.close(self.db_fd)
		os.unlink(flaskr.app.config[ 'DATABASE'])

	def test_empty_db(self):
		
		rv = self.app.get('/')
		assert b'Unbelievable. No Entries' in rv.data

	def login(self, username, password):
		return self.app.post( '/login' , data=dict(
					username=username,
					password=password
			), follow_redirects=True)
	
	def logout(self):
		return self.app.get( '/logout' , follow_redirects=True)

	def test_login_logout(self):
		rv = self.login('admin' , 'admin123' )
		print "logged in :%s" %(rv.data)
		assert b'you are loggged in' in rv.data
		# rv = self.logout()
		# print "logged out :%s" %(rv.data)
		# assert b'you are logged out' in rv.data
		# rv = self.login( 'adminx' , 'admin123' )
		# print "invalid username :%s" %(rv.data)
		# assert b'Invalid Username' in rv.data
		# rv = self.login( 'admin', 'defaultx' )
		# print "invalid Password :%s" %(rv.data)
		# assert b'Invalid Password' in rv.data

	# def test_messages(self):
	# 	rv=self.app.post('/add',data=dict(
	# 		title='<h1>hello</h1>',
	# 		text='<strong>hi</strong>this is me'
	# 		),follow_redirects=True)
	# 	print 'Test_messages %s' %(rv.data)
	# 	assert b'No entries so far' not in rv.data
	# 	assert b'<strong>hi</strong>this is me' in rv.data
if __name__ == '__main__':
	unittest.main()