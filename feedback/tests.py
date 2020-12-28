from django.test import TestCase, Client
from django.urls import resolve
from .models import Feedback
from .views import feedback, savefeedback, listfeedback
from django.contrib.auth.models import User

# Create your tests here.

##Test Feedback
class TestFeedback(TestCase):
    def setUp(self):
        Feedback.objects.create(
            nama="Vanessa",
            email="vanessa.emily@ui.ac.id",
            isi="hola halo hula"
        )

    ## Test Model

    def test_apakah_ada_model_Feedback(self):
        hitung_banyaknya = Feedback.objects.all().count()
        self.assertEquals(hitung_banyaknya, 1)

    ## Test URL

    def test_urlnya_ada(self):
        response = Client().get('/feedback/')
        self.assertEquals(response.status_code, 200)

    def test_url_savefeedback_ada(self):
        response = Client().get('/feedback/savefeedback/')
        self.assertEquals(response.status_code, 200)

    def test_url_listfeedback_belum_login(self):
        response = Client().get('/feedback/listfeedback/')
        self.assertEquals(response.status_code, 302)

    def test_url_listfeedback_setelah_login(self):
        user = User.objects.create_user(username='test',password='password')
        self.client.login(username='test', password='password')
        response = self.client.get('/feedback/listfeedback/')
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'listfeedback.html')

    ## Test Views

    def test_template_feedback(self):
        response = Client().get('/feedback/')
        self.assertTemplateUsed(response, 'feedback.html')
        self.assertTemplateUsed(response, 'base.html')

    def test_views_feedback(self):
        found = resolve('/feedback/')
        self.assertEquals(found.func, feedback)

    def test_views_savefeedback(self):
        found = resolve('/feedback/savefeedback/')
        self.assertEquals(found.func, savefeedback)

    def test_views_listfeedback_ada(self):
        found = resolve('/feedback/listfeedback/')
        self.assertEquals(found.func, listfeedback)

    def test_POST_form(self):
        response = Client().post('/feedback/savefeedback/', data = {'nama': 'Spongebob','email':
        'spongebob@gmail.com','isi': 'halo'})
        banyaknya = Feedback.objects.filter(nama="Spongebob").count()
        html = response.content.decode('utf-8')
        self.assertIn("nama", html)
        self.assertIn("email", html)
        self.assertIn("isi", html)
        self.assertEquals(banyaknya, 1)