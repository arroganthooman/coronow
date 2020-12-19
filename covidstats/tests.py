from django.test import TestCase
from django.test.client import Client
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from django import db
from .models import KasusProvinsi, KasusUpdated
from .task import main as task_main
import threading, requests, re, datetime, json, schedule, logging

# Create your tests here.
class CovidstatsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.url = reverse('covidstats')

        cls.kasus_updated_json = requests.get("https://data.covid19.go.id/public/api/update.json").json()
        cls.list_provinsi_json = requests.get("https://data.covid19.go.id/public/api/prov_list.json").json()
        cls.jakarta_json = requests.get("https://data.covid19.go.id/public/api/prov_detail_DKI_JAKARTA.json").json()
        
        db.connections.close_all()
        task_main()
        task_thread = threading.enumerate()[1]
        while(not task_thread.__dict__.get('task_done_once', False)):
            pass
        
        cls.user_credential = {
            'username': 'test',
            'email': 'test@test.xyz',
            'password': 'test'
        }
        cls.user = User.objects.create_user(cls.user_credential['username'], cls.user_credential['email'], cls.user_credential['password'])
        logging.basicConfig(level=logging.WARNING)

    #Task Test
    def test_task_thread_exists(self):
        self.assertTrue(len(threading.enumerate()) > 1)

    def test_task_is_scheduled(self):
        self.assertEqual(schedule.jobs[0].period.seconds // 3600, 3)

    def test_task_run_successfully(self):
        self.assertEqual(KasusUpdated.objects.all().count(), 1)
        
        jumlah_provinsi = len(self.list_provinsi_json['list_data'])
        self.assertEqual(KasusProvinsi.objects.all().count(), jumlah_provinsi + 1) # +Indonesia

    def test_task_fetch_latest_data(self):
        list_provinsi_expected_date = datetime.datetime.fromtimestamp(int(self.jakarta_json['list_perkembangan'][-1]['tanggal'])//1000, datetime.timezone.utc)
        self.assertEqual(str(list_provinsi_expected_date), str(KasusProvinsi.objects.all()[0].update_terakhir))

        kasus_updated_expected_date = datetime.datetime.strptime(self.kasus_updated_json['update']['penambahan']['created'], '%Y-%m-%d %X').replace(tzinfo = datetime.timezone.utc)
        self.assertEqual(str(kasus_updated_expected_date), str(KasusUpdated.objects.all()[0].update_terakhir))

    #Models Test
    def test_models_can_create_KasusUpdated(self):
        kasus_updated_data = self.kasus_updated_json
        r = requests.get("https://covid19.disiplin.id/")

        kasus_updated = KasusUpdated.objects.create(
            nama = "kasus-updated2",
            spesimen = kasus_updated_data['data']['total_spesimen'],
            spesimen_negatif = kasus_updated_data['data']['total_spesimen_negatif'],
            kasus_terkonfirmasi_kum = kasus_updated_data['update']['total']['jumlah_positif'],
            kasus_terkonfirmasi = kasus_updated_data['update']['penambahan']['jumlah_positif'],
            kasus_meninggal_kum = kasus_updated_data['update']['total']['jumlah_meninggal'],
            kasus_meninggal = kasus_updated_data['update']['penambahan']['jumlah_meninggal'],
            kasus_sembuh_kum = kasus_updated_data['update']['total']['jumlah_sembuh'],
            kasus_sembuh = kasus_updated_data['update']['penambahan']['jumlah_sembuh'],
            kasus_dirawat_kum  = kasus_updated_data['update']['total']['jumlah_dirawat'],
            kasus_dirawat = kasus_updated_data['update']['penambahan']['jumlah_dirawat'],
            kasus_suspek = kasus_updated_data['data']['jumlah_odp'],
            kab_kota_terdampak = re.findall('(?<=<p>Kasus Suspek<\/p>\\\\t\\\\t\\\\t\\\\r\\\\n                <h4 class="text-danger">)[\d.]+', str(r.content))[0],
            transmisi_lokal = re.findall('(?<=<p>Kab Kota terdampak<\/p>\\\\r\\\\n                <h4 class="text-danger">)[\d.]+', str(r.content))[0],
            update_terakhir = datetime.datetime.strptime(kasus_updated_data['update']['penambahan']['created'], '%Y-%m-%d %X').replace(tzinfo = datetime.timezone(datetime.timedelta(hours=7))),
            str_update_terakhir = datetime.datetime.strptime(kasus_updated_data['update']['penambahan']['created'], '%Y-%m-%d %X').replace(tzinfo = datetime.timezone(datetime.timedelta(hours=7))).strftime("%d %b %y") 
        )

        kasus_updated.save()
        self.assertTrue(str(KasusUpdated.objects.filter(nama="kasus-updated2")[0]) == "kasus-updated2")
        
    def test_models_can_create_KasusProvinsi(self):
        kasus_provinsi = KasusProvinsi.objects.create(
            nama_provinsi = "provinsi_dummy",
            data_json = {"json": True},
            update_terakhir = timezone.now(),
            str_update_terakhir = timezone.now().strftime("%d %b %y") 
        )

        kasus_provinsi.save()
        self.assertTrue(str(KasusProvinsi.objects.filter(nama_provinsi="provinsi_dummy")[0]) == "provinsi_dummy")

    #URL Test
    def test_urls_covidstats_exists(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    #View Test
    def test_views_use_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'covidstats/covidstats.html')

    def test_views_contain_data(self):
        response = self.client.get(self.url)
        html = response.content.decode('utf8')

        self.assertIn(f'{KasusUpdated.objects.all()[0].kasus_terkonfirmasi_kum:,}', html)
        self.assertIn(f'{KasusUpdated.objects.all()[0].kasus_sembuh_kum:,}', html)
        self.assertIn(f'{KasusUpdated.objects.all()[0].kasus_meninggal_kum:,}', html)
    
    def test_views_pass_is_authenticated_as_context(self):
        response = self.client.get(self.url)
        self.assertEqual(response.context["is_auth"], response.wsgi_request.user.is_authenticated)

    def test_views_pass_KasusUpdated_as_context(self):
        response = self.client.get(self.url)
        self.assertEqual(response.context["kasus_updated"], KasusUpdated.objects.all()[0])
    
    def test_views_post_KasusProvinsi_return_kasus_harian_json(self):
        self.client.login(username=self.user_credential['username'], password=self.user_credential['password'])

        response = self.client.post(self.url, {
            "post_type": "POST_PROV",
            "prov": "DKI Jakarta"
        })

        html = response.content.decode('utf8')
        self.assertIn(KasusProvinsi.objects.get(nama_provinsi="DKI JAKARTA").data_json[-1], json.loads(html))

    def test_views_post_KasusProvinsi_not_found_return_json(self):
        self.client.login(username=self.user_credential['username'], password=self.user_credential['password'])

        response = self.client.post(self.url, {
            "post_type": "POST_PROV",
            "prov": "else"
        })

        html = response.content.decode('utf8')
        self.assertEqual(response.status_code, 404)
        expected_json = {
            'fail': True, 
            'reason': 'not-found', 
            'msg': 'KasusProvinsi matching query does not exist.'
        }
        self.assertEqual(expected_json, json.loads(html))
    
    def test_views_post_KasusProvinsi_not_auth_return_kasus_harian_indonesia_json(self):
        response = self.client.post(self.url, {
            "post_type": "POST_PROV",
            "prov": "else"
        })

        html = response.content.decode('utf8')
        self.assertIn(KasusProvinsi.objects.get(nama_provinsi="INDONESIA").data_json[-1], json.loads(html))