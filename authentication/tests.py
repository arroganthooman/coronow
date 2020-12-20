from django.http import response
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import auth, User

# Create your tests here.

## Test URL
class TestLogin(TestCase):
	@classmethod
	def setUpTestData(cls) -> None:
		cls.login_url = reverse('login')
		cls.logout_url = reverse('logout')
		cls.register_url = reverse('register')

		cls.user = User.objects.create_user(
			username="fikri", 
			password="password"
		)

	## Test URL
	def test_url_login(self):
		response = self.client.get(self.login_url)
		self.assertEquals(response.status_code,200)
		self.assertTemplateUsed(response, "login.html")

	def test_url_login_dengan_login(self):
		self.client.login(username="fikri", password="password")

		response = self.client.get(self.login_url)
		self.assertEquals(response.status_code,302)

	def test_url_register(self):
		response = self.client.get(self.register_url)
		self.assertEquals(response.status_code,200)
		self.assertTemplateUsed(response, "register.html")

	def test_url_register_dengan_login(self):
		self.client.login(username="fikri", password="password")

		response = self.client.get(self.register_url)
		self.assertEquals(response.status_code, 302)

	def test_url_logout(self):
		self.client.login(username="fikri", password="password")

		response = self.client.get(self.logout_url)
		self.assertEquals(response.status_code, 302)

	## test view
	def test_view_login(self):
		response = self.client.post(self.login_url, data={
			'username': 'fikri',
			'password':'password'
		})
		self.assertEquals(response.status_code, 302)

	def test_view_register_berhasil(self):
		response = self.client.post(self.register_url, data= {
			'username': 'fikriYangLain',
			'password':'password123',
			'password1':'password123',
			'email': 'fikriYangLain@gmail.com'
		})
		self.assertEquals(response.status_code,302)

	def test_view_register_gagal(self):
		response = self.client.post(self.register_url, data= {
			'username': 'fikri',
			'password':'password',
			'password1':'password',
			'email': 'fikri@gmail.com'
		})
		self.assertEquals(response.status_code, 302)

	def test_logout(self):
		self.client.login(username="fikri", password="password")

		response = self.client.get(self.logout_url)
		self.assertEquals(response.status_code, 302)