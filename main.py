import json
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from randevu import HizmetRandevusu


varsayilan_hizmetler = {
    "Masaj": 600,
    "Cilt Bakimi": 450,
    "Sauna": 300,
    "Fitness": 250,
    "Yuzme": 200
}

varsayilan_maliyetler = {
    "Masaj": 250,
    "Cilt Bakimi": 180,
    "Sauna": 100,
    "Fitness": 80,
    "Yuzme": 60
}


def hizmetleri_yukle():
    try:
        with open("hizmetler.json", "r", encoding="utf-8") as dosya:
            veriler = json.load(dosya)
            return veriler["hizmetler"], veriler["maliyetler"]

    except (FileNotFoundError, json.JSONDecodeError, KeyError):
        hizmetleri_kaydet(varsayilan_hizmetler, varsayilan_maliyetler)
        return varsayilan_hizmetler.copy(), varsayilan_maliyetler.copy()


def hizmetleri_kaydet(hizmetler, maliyetler):
    with open("hizmetler.json", "w", encoding="utf-8") as dosya:
        json.dump({
            "hizmetler": hizmetler,
            "maliyetler": maliyetler
        }, dosya, ensure_ascii=False, indent=4)


def randevulari_yukle():
    try:
        with open("veriler.json", "r", encoding="utf-8") as dosya:
            veriler = json.load(dosya)

            if isinstance(veriler, list):
                return veriler

            print("Randevu dosyasinin icerigi hatali.")
            return []

    except FileNotFoundError:
        return []

    except json.JSONDecodeError:
        print("Randevu dosyasi okunamadi.")
        return []


def randevulari_kaydet(randevular):
    try:
        with open("veriler.json", "w", encoding="utf-8") as dosya:
            json.dump(randevular, dosya, ensure_ascii=False, indent=4)

    except OSError:
        print("Dosya kaydedilirken hata olustu.")


hizmetler, maliyetler = hizmetleri_yukle()
randevular = randevulari_yukle()


def hizmet_ekle():
    print("\n--- Yeni Hizmet Ekle ---")

    isim = input("Hizmet adi: ").strip()

    if isim == "":
        print("Hizmet adi bos birakilamaz.")
        return

    if isim in hizmetler:
        print("Bu hizmet zaten kayitli.")
        return

    try:
        ucret = float(input("Hizmet ucreti: "))
        maliyet = float(input("Hizmet maliyeti: "))

        if ucret <= 0 or maliyet < 0:
            print("Ucret sifirdan buyuk, maliyet sifir veya daha buyuk olmali.")
            return

        hizmetler[isim] = ucret
        maliyetler[isim] = maliyet

        hizmetleri_kaydet(hizmetler, maliyetler)

        print("Yeni hizmet basariyla eklendi.")

    except ValueError:
        print("Lutfen gecerli bir sayi giriniz.")


def randevu_ekle():
    print("\n--- Randevu Ekle ---")

    musteri_adi = input("Musteri adi: ").strip()

    if musteri_adi == "":
        print("Musteri adi bos birakilamaz.")
        return

    tarih = input("Tarih (GG.AA.YYYY): ").strip()
    saat = input("Saat (Ornek: 14:30): ").strip()

    try:
        tarih_bilgisi = datetime.strptime(tarih, "%d.%m.%Y")
        saat_bilgisi = datetime.strptime(saat, "%H:%M")

    except ValueError:
        print("Tarih veya saat formati hatali.")
        return

    yeni_baslangic = datetime.combine(
        tarih_bilgisi.date(),
        saat_bilgisi.time()
    )

    yeni_bitis = yeni_baslangic + timedelta(hours=1)

    print("\nHizmetler:")

    for hizmet, ucret in hizmetler.items():
        print(hizmet, "-", ucret, "TL")

    secim = input("Hizmet seciniz: ").strip()

    if secim not in hizmetler:
        print("Gecersiz hizmet secimi.")
        return

    for randevu in randevular:
        if randevu["durum"] == "Aktif" and randevu["tarih"] == tarih:
            eski_baslangic = datetime.combine(
                datetime.strptime(randevu["tarih"], "%d.%m.%Y").date(),
                datetime.strptime(randevu["saat"], "%H:%M").time()
            )

            eski_bitis = eski_baslangic + timedelta(hours=1)

            if yeni_baslangic < eski_bitis and eski_baslangic < yeni_bitis:
                print("Bu saat araliginda baska bir aktif randevu var.")
                return

    yeni_randevu = HizmetRandevusu(
        musteri_adi,
        tarih,
        saat,
        secim,
        hizmetler[secim]
    )

    randevular.append({
        "musteri_adi": yeni_randevu.musteri_adi,
        "tarih": yeni_randevu.tarih,
        "saat": yeni_randevu.saat,
        "hizmet": yeni_randevu.hizmet,
        "ucret": yeni_randevu.ucret,
        "durum": yeni_randevu.durum
    })

    randevulari_kaydet(randevular)
    print("Randevu basariyla eklendi.")


def randevulari_listele():
    print("\n--- Kayitli Randevular ---")

    if len(randevular) == 0:
        print("Kayitli randevu bulunamadi.")
        return

    for i, randevu in enumerate(randevular, start=1):
        print("\nRandevu No:", i)
        print("Musteri:", randevu["musteri_adi"])
        print("Tarih:", randevu["tarih"])
        print("Saat:", randevu["saat"])
        print("Hizmet:", randevu["hizmet"])
        print("Ucret:", randevu["ucret"], "TL")
        print("Durum:", randevu["durum"])


def randevu_ara():
    print("\n--- Randevu Ara ---")

    isim = input("Aranacak musteri adi: ").strip().lower()

    if isim == "":
        print("Arama alani bos birakilamaz.")
        return

    bulundu = False

    for i, randevu in enumerate(randevular, start=1):
        if isim in randevu["musteri_adi"].lower():
            print("\nRandevu No:", i)
            print("Musteri:", randevu["musteri_adi"])
            print("Tarih:", randevu["tarih"])
            print("Saat:", randevu["saat"])
            print("Hizmet:", randevu["hizmet"])
            print("Ucret:", randevu["ucret"], "TL")
            print("Durum:", randevu["durum"])
            bulundu = True

    if not bulundu:
        print("Bu isimde bir randevu bulunamadi.")


def randevu_iptal():
    randevulari_listele()

    if len(randevular) == 0:
        return

    try:
        no = int(input("\nIptal edilecek randevu numarasi: "))

        if no < 1 or no > len(randevular):
            print("Gecersiz randevu numarasi.")
            return

        randevu = randevular[no - 1]

        if randevu["durum"] != "Aktif":
            print("Bu randevu aktif degil.")
            return

        randevu["durum"] = "Iptal Edildi"

        randevulari_kaydet(randevular)

        print("Randevu iptal edildi.")

    except ValueError:
        print("Lutfen sayi giriniz.")


def randevu_tamamla():
    randevulari_listele()

    if len(randevular) == 0:
        return

    try:
        no = int(input("\nTamamlanacak randevu numarasi: "))

        if no < 1 or no > len(randevular):
            print("Gecersiz randevu numarasi.")
            return

        randevu = randevular[no - 1]

        if randevu["durum"] != "Aktif":
            print("Bu randevu aktif degil.")
            return

        randevu["durum"] = "Tamamlandi"

        randevulari_kaydet(randevular)

        print("Randevu tamamlandi.")

    except ValueError:
        print("Lutfen sayi giriniz.")


def gelir_hesapla():
    tamamlananlar = []

    for randevu in randevular:
        if randevu["durum"] == "Tamamlandi":
            tamamlananlar.append(randevu)

    if len(tamamlananlar) == 0:
        print("Henuz tamamlanan randevu yok.")
        return

    ucretler = [randevu["ucret"] for randevu in tamamlananlar]

    toplam_gelir = sum(ucretler)
    ortalama_ucret = np.mean(ucretler)

    toplam_gider = 0

    for randevu in tamamlananlar:
        toplam_gider += maliyetler[randevu["hizmet"]]

    kar = toplam_gelir - toplam_gider
    kar_yuzdesi = (kar / toplam_gelir) * 100

    print("\n--- Gelir ve Kar Raporu ---")
    print("Toplam Gelir:", toplam_gelir, "TL")
    print("Toplam Gider:", toplam_gider, "TL")
    print("Toplam Kar:", kar, "TL")
    print("Kar Yuzdesi: %", round(kar_yuzdesi, 2))
    print("Ortalama Hizmet Ucreti:", round(ortalama_ucret, 2), "TL")

    tablo = pd.DataFrame(tamamlananlar)

    sonuc = tablo.groupby("hizmet").agg(
        randevu_sayisi=("hizmet", "count"),
        toplam_gelir=("ucret", "sum")
    )

    sonuc["toplam_gider"] = [
        maliyetler[hizmet] * sayi
        for hizmet, sayi in sonuc["randevu_sayisi"].items()
    ]

    sonuc["kar"] = sonuc["toplam_gelir"] - sonuc["toplam_gider"]

    print("\n--- Hizmetlere Gore Rapor ---")
    print(sonuc)


def menu():
    while True:
        print("\n===== RANDEVU TAKIP SISTEMI =====")
        print("1- Randevu Ekle")
        print("2- Randevulari Listele")
        print("3- Randevu Ara")
        print("4- Randevu Iptal Et")
        print("5- Randevu Tamamla")
        print("6- Gelir ve Kar Hesapla")
        print("7- Yeni Hizmet Ekle")
        print("8- Cikis")

        secim = input("\nSeciminiz: ").strip()

        if secim == "1":
            randevu_ekle()

        elif secim == "2":
            randevulari_listele()

        elif secim == "3":
            randevu_ara()

        elif secim == "4":
            randevu_iptal()

        elif secim == "5":
            randevu_tamamla()

        elif secim == "6":
            gelir_hesapla()

        elif secim == "7":
            hizmet_ekle()

        elif secim == "8":
            print("Programdan cikiliyor.")
            break

        else:
            print("Hatali secim yaptiniz.")


if __name__ == "__main__":
    menu()  