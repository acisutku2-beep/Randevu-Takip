
class Randevu:
    def __init__(self, musteri_adi, tarih, saat):
        self.musteri_adi = musteri_adi
        self.tarih = tarih
        self.saat = saat


class HizmetRandevusu(Randevu):
    def __init__(self, musteri_adi, tarih, saat, hizmet, ucret):
        super().__init__(musteri_adi, tarih, saat)
        self.hizmet = hizmet
        self.ucret = ucret
        self.durum = "Aktif"

    def bilgileri_goster(self):
        print("Müşteri:", self.musteri_adi)
        print("Tarih:", self.tarih)
        print("Saat:", self.saat)
        print("Hizmet:", self.hizmet)
        print("Ücret:", self.ucret, "TL")
        print("Durum:", self.durum)
