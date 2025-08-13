
#Proje Tanımı

Bu proje, Python kullanılarak geliştirilecek bir RESTful API uygulamasıdır.  
API, sisteme tanımlanan "job" görevlerini çalıştıracak, sonuçlarını veritabanına kaydedecek ve kullanıcıya sunacaktır.  
Uygulama, Docker ortamında çalışacaktır.

#Özelliklerimiz
- Sistemdeki job görevlerini tetikleme ve çalıştırma
- Job çalışınca üretilen sonuçların belirlenen veritabanına kaydedilmesi
- API üzerinden job sonuçlarının listelenmesi ve detaylarının görüntülenmesi
- Başlangıçta 2 adet job tanımlı olacak:
  1. Komut Çalıştırma Jobu
     -Sistemin çalıştığı dizinde verilen işletim sistemi komutunu çalıştırır ve çıktısını döndürür.
  2. Katana Crawl Jobu
     -Katana aracı ile verilen web sitesinin adresini crawl yapar, bulunan toplam URL sayısını veritabanına kaydeder.


# Teknolojiler
- **Python** 
- **SQLite** 
- **Docker**
- **Docker Compose**
- **Katana**
- **RabbitMQ**
- **PortreSQL**

# Kullanım Senaryosu
1. API üzerinden bir job tetiklenir.
2. Job çalışır ve çıktısını üretir.
3. Üretilen çıktı veritabanına kaydedilir.
4. API üzerinden bu sonuçlar listelenebilir ve detayları görüntülenebilir.


# Katana URL Crawl Test

Bu proje, **ProjectDiscovery Katana** aracı kullanılarak  
`https://demo.testfire.net` adresinde yapılan eğitim amaçlı bir taramanın  
çıktı dosyalarını içermektedir.

# İçerik
- **urls.txt** → Katana tarafından bulunan tüm URL’lerin listesi.
- **urls.db** → Hedef site adresi ve toplam URL sayısını içeren SQLite veritabanı.

## Amaç
Bu çalışma tamamen **eğitim ve test amaçlıdır**.  
Tarama, herkese açık ve yasal olarak izinli bir test ortamı olan  
[demo.testfire.net](https://demo.testfire.net) üzerinde yapılmıştır.

