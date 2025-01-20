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


Bu proje, bir stok takip sistemi için hazırlanmış bir yönetici paneli ve kullanıcı arayüzüne sahip bir PHP ve MySQL tabanlı web uygulamasıdır. Sistem, ürünlerin stok miktarlarını izler ve admin paneli aracılığıyla ürün ekleme, güncelleme ve arama gibi işlemleri yapmanıza olanak sağlar.

Özellikler
Ürün ekleme, güncelleme, silme
Depo, ürün kodu ve isimle arama
Sayfalama
Depo bazında ürün filtreleme
Stok artırma/azaltma
Admin giriş kontrolü
Kullanım
1. Proje Dosyalarını İndirme
Bu projeyi kullanmaya başlamak için aşağıdaki adımları takip edin:

Bu proje dosyalarını bilgisayarınıza indirin.
index.php ve admin-dashboard.php gibi dosyalar, web sunucusuna (örneğin Apache) yüklenmelidir.
PHP ve MySQL sunucusunun çalışır durumda olduğundan emin olun.
2. Veritabanı Kurulumu
Veritabanını oluşturun ve gerekli tabloları ekleyin. stoktakip2 adlı bir veritabanı oluşturun ve aşağıdaki SQL sorgularını kullanarak tablonuzu oluşturun.

sql
Kopyala
CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    urun_kodu VARCHAR(50) NOT NULL,
    urun_ismi VARCHAR(100) NOT NULL,
    stok INT DEFAULT 0,
    birim VARCHAR(50) NOT NULL,
    depo VARCHAR(50) NOT NULL,
    ozel_birim VARCHAR(50) DEFAULT NULL
);
3. PHP Veritabanı Bağlantı Ayarları
Veritabanı bağlantısını aşağıdaki gibi yapılandırabilirsiniz:

Sunucu: localhost
Kullanıcı adı: root
Şifre: (şifreniz)
Veritabanı adı: dbadi
Bu ayarları admin-dashboard.php ve index.php dosyalarındaki veritabanı bağlantı kısımlarında güncelleyin.

4. Admin Paneli (Yönetici Girişi)
Yönetici paneline erişim için admin-login.php dosyasına giriş yapmanız gerekir. Eğer giriş yapmadıysanız, sistem otomatik olarak giriş sayfasına yönlendirilecektir.

5. Admin Paneli Kullanımı
Ürün Ekleme: Yönetici panelinde "Yeni Ürün Ekle" butonuna tıklayarak yeni ürün ekleyebilirsiniz.
Stok Güncelleme: Var olan ürünlerin stok miktarını artırmak veya azaltmak için "Stok Artır" veya "Stok Azalt" butonlarını kullanabilirsiniz.
Arama ve Filtreleme: Ürünleri, ürün kodu veya ismi ile arayabilir ve depoları ile filtreleyebilirsiniz.
6. Frontend ve Admin Panel Tasarımı
Admin Paneli: admin-dashboard.php
php
Kopyala
<?php
session_start();
if (!isset($_SESSION['admin'])) {
    header("Location: admin-login.php");
    exit;
}

// Veritabanı bağlantısı
$servername = "localhost";
$username = "root";
$password = "";
$dbname = "dbadi";

$conn = new mysqli($servername, $username, $password, $dbname);
if ($conn->connect_error) {
    die("Bağlantı başarısız: " . $conn->connect_error);
}

// Ürün Ekleme, Stok Güncelleme ve Filtreleme işlemleri burada yapılmaktadır
?>
Yönetici panelinde, ürün ekleme, arama ve stok artırma/azaltma işlemleri yapılır. Veritabanı bağlantı ayarları ve admin kontrolü burada yönetilir.

Kullanıcı Arayüzü: index.php
php
Kopyala
<?php
// Ürün listeleme, filtreleme ve sayfalama işlemleri yapılmaktadır
$conn = new mysqli("localhost", "root", "", "stoktakip2");

$sql = "SELECT * FROM products WHERE urun_kodu LIKE ? OR urun_ismi LIKE ? LIMIT ?, ?";
$stmt = $conn->prepare($sql);
$stmt->bind_param("ssii", $search_term, $search_term, $start, $items_per_page);
$stmt->execute();
$products = $stmt->get_result()->fetch_all(MYSQLI_ASSOC);

// Ürün listesi burada gösterilmektedir
?>
Ana sayfada ürünlerin listesi, arama ve filtreleme işlemleri yapılmaktadır. Kullanıcılar ürünleri sorgulayarak stok bilgilerini görüntüleyebilir.

7. PHP Sayfalama
Sayfalama özelliği ile, ürünler çok fazla olduğunda sayfalama yapılır. Sayfalama için gereken PHP kodu şu şekildedir:

php
Kopyala
$total_items = $products_result->num_rows;
$total_pages = ceil($total_items / $items_per_page);
$page = isset($_GET['page']) ? $_GET['page'] : 1;
$start = ($page - 1) * $items_per_page;
8. Admin Giriş Kontrolü
Admin paneline erişim için giriş yapılması gereklidir. admin-login.php sayfasında admin kullanıcı adı ve şifresi ile giriş yapılabilir. Giriş yapmadığınız takdirde admin-dashboard.php sayfasına yönlendirilirsiniz.

php
Kopyala
<?php
session_start();
if (!isset($_SESSION['admin'])) {
    header("Location: admin-login.php");
    exit;
}
?>
9. JavaScript İşlevleri
Yönetici panelindeki form açma ve özel birim seçme işlevlerini JavaScript ile kontrol ederiz:

javascript
Kopyala
function toggleForm() {
    var form = document.getElementById('addProductForm');
    if (form.style.display === "none" || form.style.display === "") {
        form.style.display = "block";
    } else {
        form.style.display = "none";
    }
}

document.getElementById('birim').addEventListener('change', function () {
    var ozelBirimContainer = document.getElementById('ozel-birim-container');
    if (this.value === 'ozel') {
        ozelBirimContainer.style.display = 'block';
    } else {
        ozelBirimContainer.style.display = 'none';
    }
});
10. Geliştirme ve Katkı
Bu projeye katkıda bulunmak istiyorsanız, lütfen aşağıdaki adımları takip edin:

Repo'yu fork edin.
Geliştirmelerinizi yapın ve pull request oluşturun.
Lisans
Bu proje MIT Lisansı ile lisanslanmıştır.
