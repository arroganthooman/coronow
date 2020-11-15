from django.db import models

class KasusUpdated(models.Model):
    nama = models.CharField(max_length=50)
    spesimen = models.IntegerField()
    spesimen_negatif = models.IntegerField()
    kasus_terkonfirmasi_kum = models.IntegerField()
    kasus_terkonfirmasi = models.IntegerField()
    kasus_meninggal_kum = models.IntegerField()
    kasus_meninggal = models.IntegerField()
    kasus_sembuh_kum = models.IntegerField()
    kasus_sembuh = models.IntegerField()
    kasus_dirawat_kum = models.IntegerField()
    kasus_dirawat = models.IntegerField()
    kasus_suspek = models.IntegerField()
    kab_kota_terdampak = models.SmallIntegerField()
    transmisi_lokal = models.SmallIntegerField()
    update_terakhir = models.DateTimeField()

    def save(self, *args, **kwargs):
        self.full_clean()
        super(KasusUpdated, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.nama

class KasusProvinsi(models.Model):
    nama_provinsi = models.CharField(max_length=100, blank=False)
    data_json = models.JSONField()
    update_terakhir = models.DateTimeField()

    def __str__(self) -> str:
        return self.nama_provinsi