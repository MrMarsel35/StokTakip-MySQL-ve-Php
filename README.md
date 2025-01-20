# Stok Takip Sistemi

**Stok Takip Sistemi** Python, Tkinter ve MySQL kullanılarak geliştirilmiş bir masaüstü uygulamasıdır. Bu sistem, işletmelerin stoklarını kolayca yönetmelerine, ürünleri takip etmelerine ve hızlı işlem yapmalarına olanak tanır. Ayrıca, ürünlerin depoları ve birimleri arasında filtreleme yapabilme, stok artırma/azaltma işlemleri gerçekleştirebilme gibi özellikleri de içerir.

## Özellikler

### 1. **Hızlı Arama**
- Ürün kodu veya ismiyle hızlı arama yapabilirsiniz. Arama sonuçları anında filtrelenir.

### 2. **Esnek Stok Yönetimi**
- **Stok Artırma:** Kullanıcılar, mevcut ürün stoklarını artırabilir.
- **Stok Azaltma:** Stok miktarını azaltabilirler.
- **Ürün Silme:** Ürünler veritabanından tamamen silinebilir.

### 3. **Excel ile Toplu Veri Yükleme**
- Excel dosyasından ürün bilgilerini sisteminize aktarabilirsiniz. Excel formatı, ürün kodu, ismi, stok, birim ve depo gibi bilgileri içerir.

### 4. **Filtreleme Özellikleri**
- Depo ve birim bazında filtreleme yaparak, yalnızca ihtiyacınız olan verileri görebilirsiniz.

### 5. **İşlem Geçmişi**
- Tüm stok işlemleri (artırma, azaltma, silme) kaydedilir ve işlem geçmişine erişebilirsiniz. İşlem tarihleri, kullanıcı adları ve detayları görüntülenebilir.

### 6. **Veritabanı Yönetimi**
- **Veritabanını sıfırlama:** Sistemdeki tüm ürün verilerini temizleyebilir, sıfırdan başlayabilirsiniz.

### 7. **Düşük Stok Uyarıları**
- Stok seviyesi 20'nin altına düşen ürünler, kırmızı renkte uyarı ile gösterilir.

## Kullanılan Teknolojiler

- **Python:** Tkinter, MySQL, Pandas ve diğer kütüphanelerle geliştirilmiştir.
- **Tkinter:** Kullanıcı arayüzü oluşturmak için kullanılmıştır.
- **MySQL:** Ürün bilgilerini ve işlem geçmişini depolamak için kullanılan veritabanı yönetim sistemidir.
- **Pandas:** Excel dosyasından veri yüklemek için kullanılmıştır.

## Kurulum

1. **Gerekli Paketlerin Yüklenmesi:**

   Projenin çalışabilmesi için gerekli Python kütüphanelerini yükleyin:

   ```bash
   pip install mysql-connector-python pandas


2. Veritabanı Ayarları:
Veritabanı bağlantısı için MySQL kurulumu gereklidir. MySQL sunucusu üzerinde bir veritabanı oluşturun (örneğin: stoktakip2).
products ve transaction_history gibi tabloları oluşturun.
Bağlantı bilgilerini (host, user, password, database) get_db_connection() fonksiyonunda güncelleyin.
3. Uygulamanın Çalıştırılması:
bash
Kopyala
python stok_takip.py
Bu iki kısmı gerektiği şekilde kullanabilirsiniz. Eğer başka bir yardıma ihtiyacınız olursa, yardımcı olmaktan memnuniyet duyarım!



Ürün arama çubuğu üzerinden arama yapabilir, Excel dosyasından veri yükleyebilirsiniz.
İşlem Geçmişi:

Tüm stok işlemleriniz kaydedilir. "İşlem Geçmişi" butonuyla geçmişe dair her türlü işlemi görüntüleyebilirsiniz.
Stok Yönetimi:

Sağ tıklayarak ürünleri artırabilir, azaltabilir veya silebilirsiniz.
Katkıda Bulunma
Bu projeye katkıda bulunmak isterseniz, aşağıdaki adımları izleyebilirsiniz:

Bu repoyu fork edin.
Yeni bir branch oluşturun.
Yapmak istediğiniz değişiklikleri gerçekleştirin.
Pull request açarak katkınızı sunun.
