from django.test import TestCase
from django.contrib.auth.models import auth, User

# Create your tests here.

## Test URL
class TestLogin(TestCase):

	## Test URL
	def test_url_login(self):
		response = self.client.get("/login/")
		self.assertEquals(response.status_code,200)
		self.assertTemplateUsed(response, "login.html")

	def test_url_login_dengan_login(self):
		user = User.objects.create_user(
			username="fikri", password="password"
			)

		self.client.login(username="fikri", password="password")
		response = self.client.get('/login/')
		self.assertEquals(response.status_code,302)

	def test_url_register(self):
		response = self.client.get('/login/register/')
		self.assertEquals(response.status_code,200)
		self.assertTemplateUsed(response, "register.html")

	def test_url_register_dengan_login(self):
		user = User.objects.create_user(
			username="fikri", password="password"
			)

		self.client.login(username="fikri", password="password")
		response = self.client.get('/login/register/')
		self.assertEquals(response.status_code, 302)


	## test view
	def test_view_login(self):
		user = User.objects.create_user(
			username="fikri", password="password"
			)
		
		response = self.client.post('/login/', data= {
			'username': 'fikri',
			'password':'password'
			})

		self.assertEquals(response.status_code, 302)

	def test_view_register_berhasil(self):
		response = self.client.post('/login/register/', data= {
			'username': 'fikri',
			'password':'password',
			'password1':'password',
			'email': 'fikri@gmail.com'
			})
		self.assertEquals(response.status_code,302)

	def test_view_register_gagal(self):
		user = User.objects.create_user(
			username="fikri", password="password"
			)

		response = self.client.post('/login/register/', data= {
			'username': 'fikri',
			'password':'password',
			'password1':'password',
			'email': 'fikri@gmail.com'
			})

		self.assertEquals(response.status_code, 302)

	def test_logout(self):
		user = User.objects.create_user(
			username="fikri", password="password"
			)

		self.client.login(username="fikri", password="password")

		response = self.client.get('/login/logout/')
		self.assertEquals(response.status_code,302)



