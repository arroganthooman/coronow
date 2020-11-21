from django.test import TestCase, Client
from .models import News, Comment

# Create your tests here.
class Testing(TestCase):
    def test_url_news(self):
        response = Client().get('/covidnews/')
        self.assertEquals(response.status_code, 200)
    
    def test_isi_news(self):
        response = Client().get('/covidnews/')
        html_kembalian = response.content.decode('utf8')
        self.assertIn("CovidNews", html_kembalian)

    def test_template_news(self):
        response = Client().get('/covidnews/')
        self.assertTemplateUsed(response, 'news.html','base.html')
