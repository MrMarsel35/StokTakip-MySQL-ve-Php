<?php
session_start();

// Admin kontrolü
if (!isset($_SESSION['admin'])) {
    header("Location: admin-login.php");
    exit;
}

// Veritabanı bağlantısı
$servername = "localhost";
$username = "root";
$password = "";
$dbname = "stoktakip2";

$conn = new mysqli($servername, $username, $password, $dbname);
if ($conn->connect_error) {
    die("Bağlantı başarısız: " . $conn->connect_error);
}

// Depoları ürünler tablosundan dinamik olarak al
$depo_sql = "SELECT DISTINCT depo FROM products"; // Benzersiz depo isimlerini al
$depo_result = $conn->query($depo_sql);
$depolar = $depo_result->fetch_all(MYSQLI_ASSOC);

// Ürün ekleme işlemi
if ($_SERVER['REQUEST_METHOD'] == 'POST' && isset($_POST['add_product'])) {
    $urun_kodu = $_POST['urun_kodu'];
    $urun_ismi = $_POST['urun_ismi'];
    $stok = $_POST['stok'];
    $birim = $_POST['birim'];
    $depo = $_POST['depo'];
    $ozel_birim = $_POST['ozel_birim'] ?? ''; // Özel birim (opsiyonel)

    $insert_sql = "INSERT INTO products (urun_kodu, urun_ismi, stok, birim, depo, ozel_birim) VALUES (?, ?, ?, ?, ?, ?)";
    $stmt = $conn->prepare($insert_sql);
    $stmt->bind_param("ssisss", $urun_kodu, $urun_ismi, $stok, $birim, $depo, $ozel_birim);
    $stmt->execute();
    $stmt->close();
    header("Location: admin-dashboard.php");
    exit;
}

// Ürün artırma/azaltma işlemi
if (isset($_POST['update_id'])) {
    $update_id = $_POST['update_id'];
    $action = $_POST['action']; // 'increase' veya 'decrease'
    $quantity = $_POST['quantity'];

    if ($action == 'increase') {
        $sql = "UPDATE products SET stok = stok + ? WHERE id = ?";
    } else if ($action == 'decrease') {
        $sql = "UPDATE products SET stok = stok - ? WHERE id = ?";
    }

    $stmt = $conn->prepare($sql);
    $stmt->bind_param("ii", $quantity, $update_id);
    $stmt->execute();
    $stmt->close();
    header("Location: admin-dashboard.php");
    exit;
}

// Ürün arama ve filtreleme
$search_term = isset($_GET['search']) ? '%' . $_GET['search'] . '%' : '%';
$selected_depo = isset($_GET['depo']) ? $_GET['depo'] : '%';

$sql = "SELECT * FROM products WHERE urun_kodu LIKE ? OR urun_ismi LIKE ?";
$stmt = $conn->prepare($sql);
$stmt->bind_param("ss", $search_term, $search_term);
$stmt->execute();
$products_result = $stmt->get_result();
$products = $products_result->fetch_all(MYSQLI_ASSOC);

// Sayfalama
$items_per_page = 50;
$total_items = $products_result->num_rows;
$total_pages = ceil($total_items / $items_per_page);
$page = isset($_GET['page']) ? $_GET['page'] : 1;
$start = ($page - 1) * $items_per_page;

$sql = "SELECT * FROM products WHERE urun_kodu LIKE ? OR urun_ismi LIKE ? LIMIT ?, ?";
$stmt = $conn->prepare($sql);
$stmt->bind_param("ssii", $search_term, $search_term, $start, $items_per_page);
$stmt->execute();
$products = $stmt->get_result()->fetch_all(MYSQLI_ASSOC);

$stmt->close();
$conn->close();
?>

<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Yönetici Paneli</title>
    <link rel="stylesheet" href="styles.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css"> <!-- Font Awesome -->
</head>
<body>

<div class="container">
    <header>
        <h1>Yönetici Paneli</h1>
        <a href="admin-login.php?logout=true">Çıkış Yap</a>
    </header>

	<!-- Ürün Arama Formu -->
	<div class="search-form">
		<form action="admin-dashboard.php" method="get" class="search-container">
			<input type="text" name="search" placeholder="Ürün Kodu veya İsmi" value="<?php echo isset($_GET['search']) ? $_GET['search'] : ''; ?>" class="search-input">
			<select name="depo" class="search-select">
				<option value="%">Tüm Depolar</option>
				<?php foreach ($depolar as $depo) { ?>
					<option value="<?php echo $depo['depo']; ?>" <?php echo isset($_GET['depo']) && $_GET['depo'] === $depo['depo'] ? 'selected' : ''; ?>><?php echo $depo['depo']; ?></option>
				<?php } ?>
			</select>
			<button type="submit" class="search-button">Ara</button>
		</form>
	</div>

	<!-- Yeni Ürün Ekle Butonu -->
	<div class="add-product-buttonq">
		<button class="search-button" onclick="toggleForm()">
			<i class="fas fa-plus"></i> Yeni Ürün Ekle
		</button>
	</div>

	<!-- Ürün Ekleme Formu (Başlangıçta gizli olacak) -->
	<div id="addProductForm" class="add-product-form" style="display: none;">
		<h2>Yeni Ürün Ekle</h2>
		<form action="admin-dashboard.php" method="post">
			<input type="text" name="urun_kodu" placeholder="Ürün Kodu" required>
			<input type="text" name="urun_ismi" placeholder="Ürün İsmi" required>
			<input type="number" name="stok" placeholder="Stok Miktarı" required>
			<select name="birim" id="birim" required>
				<option value="adet">Adet</option>
				<option value="kg">Kilogram</option>
				<option value="litre">Litre</option>
				<option value="ozel">Özel Birim</option>
			</select>
			<select name="depo" required>
				<?php foreach ($depolar as $depo) { ?>
					<option value="<?php echo $depo['depo']; ?>"><?php echo $depo['depo']; ?></option>
				<?php } ?>
			</select>
			<!-- Özel birim alanı sadece "Özel Birim" seçildiğinde görünsün -->
			<div id="ozel-birim-container" style="display: none;">
				<input type="text" name="ozel_birim" placeholder="Özel Birim Girin">
			</div>
			<button type="submit" name="add_product">Ekle</button>
		</form>
	</div>


    <!-- Ürün Listesi ve Stok Güncelleme -->
    <table class="product-table">
        <thead>
            <tr>
                <th>Ürün Kodu</th>
                <th>Ürün İsmi</th>
                <th>Stok</th>
                <th>Birim</th>
                <th>Depo</th>
                <th>İşlemler</th>
            </tr>
        </thead>
        <tbody>
            <?php foreach ($products as $product) { ?>
                <tr>
                    <td><?php echo $product['urun_kodu']; ?></td>
                    <td><?php echo $product['urun_ismi']; ?></td>
                    <td><?php echo $product['stok']; ?></td>
                    <td><?php echo $product['birim']; ?></td>
                    <td><?php echo $product['depo']; ?></td>
                    <td>
                        <form action="admin-dashboard.php" method="post">
                            <input type="hidden" name="update_id" value="<?php echo $product['id']; ?>">
                            <div class="stock-buttons">
                                <input type="number" name="quantity" placeholder="Miktar" min="1" required>
                                <button type="submit" name="action" value="increase">Stok Artır</button>
                                <button type="submit" name="action" value="decrease">Stok Azalt</button>
                            </div>
                        </form>
                    </td>
                </tr>
            <?php } ?>
        </tbody>
    </table>

    <!-- Sayfalama -->
    <div class="pagination">
        <?php if ($page > 1) { ?>
            <a href="admin-dashboard.php?page=1<?php echo isset($_GET['search']) ? '&search=' . $_GET['search'] : ''; ?>&depo=<?php echo $selected_depo; ?>" class="page-link">1</a>
            <a href="admin-dashboard.php?page=<?php echo $page - 1; ?><?php echo isset($_GET['search']) ? '&search=' . $_GET['search'] : ''; ?>&depo=<?php echo $selected_depo; ?>" class="page-link">Önceki</a>
        <?php } ?>

        <?php for ($i = 1; $i <= $total_pages; $i++) { ?>
            <a href="admin-dashboard.php?page=<?php echo $i; ?><?php echo isset($_GET['search']) ? '&search=' . $_GET['search'] : ''; ?>&depo=<?php echo $selected_depo; ?>" class="page-link <?php echo $i == $page ? 'active' : ''; ?>"><?php echo $i; ?></a>
        <?php } ?>

        <?php if ($page < $total_pages) { ?>
            <a href="admin-dashboard.php?page=<?php echo $page + 1; ?><?php echo isset($_GET['search']) ? '&search=' . $_GET['search'] : ''; ?>&depo=<?php echo $selected_depo; ?>" class="page-link">Sonraki</a>
        <?php } ?>
    </div>
</div>

<script>
    // Özel birim alanının görünürlüğünü kontrol eden JavaScript kodu
    document.getElementById('birim').addEventListener('change', function () {
        var ozelBirimContainer = document.getElementById('ozel-birim-container');
        if (this.value === 'ozel') {
            ozelBirimContainer.style.display = 'block';
        } else {
            ozelBirimContainer.style.display = 'none';
        }
    });
</script>

<script>
    // Yeni ürün ekleme formunu açıp kapatan fonksiyon
    function toggleForm() {
        var form = document.getElementById('addProductForm');
        // Eğer form gizli ise, göster
        if (form.style.display === "none" || form.style.display === "") {
            form.style.display = "block";
        } else {
            form.style.display = "none";
        }
    }
</script>


</body>
</html>
