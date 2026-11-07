# Randevu Takip Sistemi

## Proje Hakkında

Bu projeyi Python programlama dili ile İleri Yazılım Teknikleri dersi için hazırladım. Amacım sağlıklı yaşam merkezlerinde kullanılan randevu işlemlerini daha kolay takip edebilen basit bir program oluşturmaktı.

Program üzerinden müşterilerin randevularını ekleyebiliyor, kayıtlı randevuları görebiliyor, müşteri adına göre arama yapabiliyor ve gerektiğinde randevuları iptal edebiliyorum. Tamamlanan randevular üzerinden de gelir ve kâr hesabı yapabiliyorum.

## Programda Neler Var?

- Müşteri adına göre randevu ekleme
- Randevuları listeleme ve arama
- Randevu iptal etme
- Randevuyu tamamlandı olarak işaretleme
- Yeni hizmet ve fiyat ekleme
- Gelir ve gider hesaplama
- Hizmetlere göre kazanç raporu oluşturma
- Aynı saat aralığına başka bir randevu eklenmesini engelleme

## Kullanılan Teknolojiler

Projeyi hazırlarken Python kullandım. Ayrıca bazı işlemler için şu kütüphanelerden yararlandım:

- NumPy: Tamamlanan hizmetlerin ortalama ücretini hesaplamak için
- Pandas: Hizmet türlerine göre rapor oluşturmak için
- JSON: Randevu ve hizmet bilgilerini kaydetmek için

## Projeyi Çalıştırma

Öncelikle gerekli kütüphanelerin yüklenmesi gerekiyor.

```bash
py -m pip install numpy pandas
```

Daha sonra proje klasöründe terminal açıp şu komutu çalıştırmak yeterli:

```bash
py main.py
```

## Dosyalar

- `main.py`: Programın ana işlemlerinin bulunduğu dosya
- `randevu.py`: Randevu sınıflarının bulunduğu dosya
- `veriler.json`: Müşteri randevularının kaydedildiği dosya
- `hizmetler.json`: Hizmet ücretleri ve maliyetlerinin tutulduğu dosya

## Geliştirici

**Utku Açış**

Bilgisayar Programcılığı