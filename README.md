# EXIF Yok Edici 3000

![Logo](https://img.shields.io/badge/python-3.x-blue.svg)
![Logo](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey)
![Logo](https://img.shields.io/badge/license-GPL%203.0-green.svg)

## Dizin

- [Hakkında](#hakkında)
- [Özellikler](#özellikler)
- [Gereknisimler](#gereksinimler)
- [Kurulum](#kurulum)
- [Özelleştirme](#özelleştirme)

## Hakkında
**EXIF Yok Edici 3000**, görsellerin EXIF üstverilerini hızlı ve kolay bir şekilde temizlemeyi sağlayan basit bir programcıktır. Konum, cihaz bilgisi, çekilme/hazırlama tarihi gibi gizliliği ve veri güvenliğini ihlal eden üstveri bilgilerini arındırır.

## Özellikler
- **Görsel ekleme:** JPG, JPEG, PNG, GIF, BMP ve TIFF formatındaki görseller desteklenir.
- **Çıktı klasörü seçimi:** Arındırılan görseller farklı bir klasöre kaydedilebilir. Klasör seçilmezse özgün dosyaların üzerine kayıt edilir.
- **Toplu işlem:** Birden fazla görsel birkaç salisede temizlenir.
- **İlerleme izleyici:** Yapılan işlem ilerleme çubuğuyla takip edilir. Yüksek sayıda görsel işlenirken yaşanan gecikmelerde "Çalışıyo' mu lan bu?" diye endişelenmeyi önler.
- **Temiz arayüz:** Basit ve anlaşılır tasarım ile kolay kullanım. Yarım akıllı alternatif programcıklardaki gibi bir anlık işlem için beş saniye reklam gösterme yamyamlığı yapılmamıştır.
  
## Gereksinimler
- **Python:** 3.7 veya üzeri sürüm
- **Pip:** Python paket yöneticisi

#### Gerekli kütüphaneler
- **Pillow:** 9.0 veya üzeri sürüm
- **tkinter:** 8.6 veya üzeri sürüm
  - **tkhtmlview:** 0.1 veya üzeri sürüm

## Kurulum
1. Depoyu klonla:
   ```
   git clone https://github.com/tyyaman55/exif-yok-edici-3000.git
   cd exif-yok-edici-3000
   ```
2. Klonlanan dizinde komut istemcisini açarak gerekli Python paketlerini yükle:
    ```
    pip install -r gereksinimler.txt
    ```
3. Programı çalıştır:
   ```
   python exif_yok_edici_3000.py
   ```

## Özelleştirme
1. Programcığın simgesi BASE64 verisi ile tanımlanıır. Bunun için dosya açılarak `program simgesinin BASE64 verisi` kısmına bu veri bütünü olduğu yapıştırılmalıdır. Aksi hâlde programcık çalışır ama ufak bir pencere açarak simgenin bulunamadığına dair bilgi verir.
2. Geliştirici bilgisine tanımlı olan bağlantı ve geliştirici adı kısmı da düzenlenmebilir.