from django.test import TestCase, Client
from django.urls import resolve
from .models import Feedback
from .views import feedback, savefeedback

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
        self.assertEquals(response.status_code, 302)

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