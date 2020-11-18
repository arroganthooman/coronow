def main():
    import schedule, time, logging, requests, threading, re, datetime
    from .models import KasusUpdated, KasusProvinsi

    API_PROV_LIST = "https://data.covid19.go.id/public/api/prov_list.json"
    API_UPDATE = "https://data.covid19.go.id/public/api/update.json"
    API_UPDATE_PROV = "https://data.covid19.go.id/public/api/prov_detail_{}.json"

    def update_data():
        logging.info("Task Thread (Update Data) : Retrieving Covid data from API.")

        update_json = requests.get(API_UPDATE).json()
        r = requests.get("https://covid19.disiplin.id/")

        update_object = KasusUpdated()
        update_object.nama = "kasus-updated"
        update_object.spesimen = update_json['data']['total_spesimen']
        update_object.spesimen_negatif = update_json['data']['total_spesimen_negatif']
        update_object.kasus_terkonfirmasi_kum = update_json['update']['total']['jumlah_positif']
        update_object.kasus_terkonfirmasi = update_json['update']['penambahan']['jumlah_positif']
        update_object.kasus_meninggal_kum = update_json['update']['total']['jumlah_meninggal']
        update_object.kasus_meninggal = update_json['update']['penambahan']['jumlah_meninggal']
        update_object.kasus_sembuh_kum = update_json['update']['total']['jumlah_sembuh']
        update_object.kasus_sembuh = update_json['update']['penambahan']['jumlah_sembuh']
        update_object.kasus_dirawat_kum  = update_json['update']['total']['jumlah_dirawat']
        update_object.kasus_dirawat = update_json['update']['penambahan']['jumlah_dirawat']
        update_object.kasus_suspek = update_json['data']['jumlah_odp']
        update_object.kab_kota_terdampak = re.findall('(?<=<p>Kasus Suspek<\/p>\\\\t\\\\t\\\\t\\\\r\\\\n                <h4 class="text-danger">)[\d.]+', str(r.content))[0]
        update_object.transmisi_lokal = re.findall('(?<=<p>Kab Kota terdampak<\/p>\\\\r\\\\n                <h4 class="text-danger">)[\d.]+', str(r.content))[0]
        update_object.update_terakhir = datetime.datetime.strptime(update_json['update']['penambahan']['created'], '%Y-%m-%d %X').replace(tzinfo = datetime.timezone.utc)
        update_object.str_update_terakhir = update_object.update_terakhir.strftime("%d %b %y") 

        prov_list = requests.get(API_PROV_LIST).json()['list_data']
        prov_obj_list = []
        for prov in prov_list:
            prov_object = KasusProvinsi(nama_provinsi = prov['key'])
            prov_data_json = requests.get(API_UPDATE_PROV.format(prov['key'].replace(" ", "_"))).json()
            prov_object.data_json = prov_data_json['list_perkembangan']
            prov_object.update_terakhir = datetime.datetime.fromtimestamp(int(prov_data_json['list_perkembangan'][-1]['tanggal'])//1000, datetime.timezone.utc)
            prov_object.str_update_terakhir = prov_object.update_terakhir.strftime("%d %b %y") 
            prov_obj_list.append(prov_object)
        list_harian = update_json['update']['harian']
        indo_update_terakhir = datetime.datetime.strptime(update_json['update']['harian'][-1]["key_as_string"][:19], '%Y-%m-%dT%X').replace(tzinfo = datetime.timezone(datetime.timedelta(hours=7)))
        prov_obj_list.append(KasusProvinsi(
            nama_provinsi = "INDONESIA",
            data_json = [{
                    "tanggal": x["key"],
                    "KASUS": x["jumlah_positif"]["value"],
                    "MENINGGAL": x["jumlah_meninggal"]["value"],
                    "SEMBUH": x["jumlah_sembuh"]["value"],
                    "AKUMULASI_KASUS": x["jumlah_positif_kum"]["value"],
                    "AKUMULASI_MENINGGAL": x["jumlah_meninggal_kum"]["value"],
                    "AKUMULASI_SEMBUH": x["jumlah_sembuh_kum"]["value"]
                } for x in list_harian],
            update_terakhir = indo_update_terakhir,
            str_update_terakhir = indo_update_terakhir.strftime("%d %b %y") 
        ))

        KasusUpdated.objects.all().delete()
        KasusProvinsi.objects.all().delete()

        KasusProvinsi.objects.bulk_create(prov_obj_list)
        update_object.save()
        
        logging.info("Task Thread (Update Data) : Done!") 

    def thread_job():
        update_data()
        threading.current_thread().__dict__['task_done_once'] = True
        schedule.every(3).hours.do(update_data)
        logging.info("Thread : Scheduling job.")

        while True:
            schedule.run_pending()
            time.sleep(1)

    # if(testing):
    #     format = "%(asctime)s: %(message)s"
    #     logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
    #     logging.info("Main  : Starting Task without Thread")

    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
    logging.info("Main  : Starting Thread")

    thread = threading.Thread(target=thread_job, daemon=True)
    thread.name = "CovidStatsUpdater"
    thread.start()