from django.test import TestCase, Client
from .models import News, Comment

# Create your tests here.
class Testing(TestCase):
    def setUp(self):
        news= News.objects.create(
            Judul="judul",
            description="deskripsi",
            Foto="foto",
            Sumber="sumber"
            )
        Comment.objects.create(
            komentar="aku seorang",
            nama="nama",
            berita=news
        )
    #Test Model
    def test_apakah_ada_model_news(self):
        hitung_banyaknya = News.objects.all().count()
        self.assertEquals(hitung_banyaknya, 1)

    def test_apakah_ada_model_comment(self):
        hitung_banyaknya = Comment.objects.all().count()
        self.assertEquals(hitung_banyaknya, 1)

    def test_str_model_news(self):
        news =News.objects.get(Judul="judul")
        self.assertEqual(str(news),news.Judul)

    def test_str_model_comment(self):
        komentar =Comment.objects.get(nama="nama")
        self.assertEqual(str(komentar),komentar.nama)

    # Test URL
    def test_url_news(self):
        response = Client().get('/covidnews/')
        self.assertEquals(response.status_code, 200)
    
    def test_url_detailnews(self):
        response = Client().get('/covidnews/news/1')
        self.assertEquals(response.status_code, 200)
    
    # Test Views
    def test_isi_news(self):
        response = Client().get('/covidnews/')
        html_kembalian = response.content.decode('utf8')
        self.assertIn("CovidNews", html_kembalian)

    def test_isi_detailnews(self):
        response = Client().get('/covidnews/news/1')
        html_kembalian = response.content.decode('utf8')
        self.assertIn("CovidNews", html_kembalian)
        self.assertIn("KOMENTAR", html_kembalian)

    def test_template_news(self):
        response = Client().get('/covidnews/')
        self.assertTemplateUsed(response, 'news.html','base.html')

    def test_template_detailnews(self):
        response = Client().get('/covidnews/news/1')
        self.assertTemplateUsed(response, 'detailNews.html','base.html')

    def test_POST_form(self):
        response = Client().post('/covidnews/news/1', data = {'komentar': 'komen','nama':
        'namabaru'})
        banyaknya = Comment.objects.filter(nama="namabaru").count()
        self.assertEquals(banyaknya, 1)    