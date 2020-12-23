from django.contrib import messages
from django.test import TestCase
from django.test.utils import tag
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from requests.api import request

# Create your tests here.

## Test URL
class TestLogin(TestCase):
	@classmethod
	def setUpTestData(cls) -> None:
		cls.login_url = reverse('login')
		cls.logout_url = reverse('logout')
		cls.register_url = reverse('register')
		cls.index_url = reverse('index')

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
		self.assertEquals(response.url, self.index_url)

	def test_url_register(self):
		response = self.client.get(self.register_url)
		self.assertEquals(response.status_code,200)
		self.assertTemplateUsed(response, "register.html")

	def test_url_register_dengan_login(self):
		self.client.login(username="fikri", password="password")

		response = self.client.get(self.register_url)
		self.assertEquals(response.status_code, 302)
		self.assertEquals(response.url, self.index_url)

	def test_url_logout(self):
		self.client.login(username="fikri", password="password")

		response = self.client.get(self.logout_url)
		self.assertEquals(response.status_code, 302)
		self.assertEquals(response.url, self.index_url)

	## test view
	def test_view_login(self):
		response = self.client.post(self.login_url, data={
			'username': 'fikri',
			'password':'password'
		})
		self.assertEquals(response.status_code, 302)
		self.assertEquals(response.url, self.index_url)

	def test_view_login_username_atau_password_salah(self):
		response = self.client.post(self.login_url, data={
			'username': 'fikriYangLain',
			'password':'password'
		})
		msgs = [msg for msg in get_messages(response.wsgi_request)]
		self.assertEquals(msgs[0].message, "Wrong username or password!")
		self.assertEquals(msgs[0].tags, "warning")

		response = self.client.post(self.login_url, data={
			'username': 'fikri',
			'password':'password123'
		})
		msgs = [msg for msg in get_messages(response.wsgi_request)]
		self.assertEquals(msgs[0].message, "Wrong username or password!")
		self.assertEquals(msgs[0].tags, "warning")

	def test_view_register_berhasil(self):
		response = self.client.post(self.register_url, data = {
			'username': 'fikriYangLain',
			'password':'password123',
			'password1':'password123',
			'email': 'fikriYangLain@gmail.com'
		})
		self.assertEquals(response.status_code, 302)
		self.assertEquals(response.url, self.index_url)

	def test_view_register_gagal(self):
		response = self.client.post(self.register_url, data = {
			'username': 'fikri',
			'password':'password',
			'password1':'password2',
			'email': 'fikri@gmail.com'
		})
		msgs = [msg.message for msg in get_messages(response.wsgi_request)]
		tags = [msg.tags for msg in get_messages(response.wsgi_request)]
		self.assertIn("Username already exists!", msgs)
		self.assertIn("Password mismatch!", msgs)
		self.assertEquals(["warning", "warning"], tags)

	def test_view_logout(self):
		self.client.login(username="fikri", password="password")

		response = self.client.get(self.logout_url)
		self.assertEquals(response.status_code, 302)
		self.assertEquals(response.url, self.index_url)