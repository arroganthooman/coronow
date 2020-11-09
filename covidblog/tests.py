from django.test import TestCase

# Create your tests here.

from django.test import TestCase, Client
from .models import Blog, Comment
from django.contrib.auth.models import User
from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
import mock

from datetime import *
	


# Create your tests here.

# Blog tests
class TestBlog(TestCase):
	def setUp(self):
		user = User.objects.create_user('fikri', password="heheoke")
		user.is_superuser=True
		user.save()

		testtime = datetime.now() - timedelta(days=60)
		image = SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg')

		with mock.patch('django.utils.timezone.now') as mock_now:
			mock_now.return_value = testtime
			self.blog = Blog.objects.create(
				author = user,
				title = "ngetest blog",
				image = image,
				body = "cuman ngetest",
				snippet = "cuman ngetest",
				id=1
			)

			self.comment = Comment.objects.create(
				komentar = "ngetest komentar",
				nama = "fikri",
				blog = self.blog,
			)


	## Test Model

	def test_model_blog(self):
		self.assertEquals(Blog.objects.count(),1)
		Blog.objects.get(id=1).image.delete(save=True)
		Blog.objects.all().delete()

	def test_model_komentar(self):
		self.assertEquals(Comment.objects.count(),1)
		self.assertEquals(str(Comment.objects.get(blog=self.blog)), "fikri")
		self.blog.delete()


	## Test URL

	def test_url_list_blog(self):
		client = Client()
		url = reverse("covidBlog")
		response = client.get(url)
		self.assertEquals(response.status_code, 200)
		Blog.objects.get(id=1).image.delete(save=True)

	def test_url_per_blog(self):
		client = Client()
		response = client.get(reverse('blog', args=[self.blog.id]))
		self.assertEquals(response.status_code, 200)
		Blog.objects.get(id=1).image.delete(save=True)


	## Test View

	def test_view_covidBlog(self):
		url = reverse('covidBlog')
		response = Client().get(url)

		self.assertTemplateUsed(response, 'base.html')
		self.assertTemplateUsed(response, 'covidBlog.html')
		Blog.objects.get(id=1).image.delete(save=True)

	def test_view_isiBlog(self):
		url = reverse('blog', args=[self.blog.id])
		response = Client().get(url)

		self.assertTemplateUsed(response, 'base.html')
		self.assertTemplateUsed(response, 'isiBlog.html')
		Blog.objects.get(id=1).image.delete(save=True)


		## test form comment
		response =  self.client.post(url, data= {
			'komentar' : "ngetest",
			'nama' : 'fikri',
			'blog' : self.blog
		})

		self.assertEquals(Comment.objects.count(),2)
		Blog.objects.get(id=1).image.delete(save=True)


	def test_admin_change_image(self):
		url = f'admin/covidblog/blog/1/change'
		image = SimpleUploadedFile(name='testing_image.jpg', content=b'', content_type='image/jpeg')
		self.blog.image = image
		self.blog.save(update_fields=['image'])
		self.blog.delete()
