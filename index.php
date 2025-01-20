<?php
// Veritabanı bağlantısı
$servername = "localhost";
$username = "root";
$password = "";
$dbname = "stoktakip2";

$conn = new mysqli($servername, $username, $password, $dbname);

if ($conn->connect_error) {
    die("Bağlantı başarısız: " . $conn->connect_error);
}

// Ürünleri ve filtreleri al
$depot_list = [];
$unit_list = [];

// Depo listesi
$sql = "SELECT DISTINCT depo FROM products";
$result = $conn->query($sql);
while ($row = $result->fetch_assoc()) {
    $depot_list[] = $row['depo'];
}

// Birim listesi
$sql = "SELECT DISTINCT birim FROM products";
$result = $conn->query($sql);
while ($row = $result->fetch_assoc()) {
    $unit_list[] = $row['birim'];
}

// Sayfalama için başlangıç değerleri
$limit = 50; // Sayfa başına ürün sayısı
$page = isset($_GET['page']) ? (int)$_GET['page'] : 1; // Şu anki sayfa
$offset = ($page - 1) * $limit; // Hangi ürünlerden başlanacağı

// Arama ve filtreleme
$search_term = isset($_GET['search']) ? '%' . $_GET['search'] . '%' : '%';
$selected_depo = isset($_GET['depo']) && $_GET['depo'] !== "Tümü" ? $_GET['depo'] : '%';
$selected_birim = isset($_GET['birim']) && $_GET['birim'] !== "Tümü" ? $_GET['birim'] : '%';

// Ürünleri almak için SQL sorgusu
$sql = "SELECT id, urun_kodu, urun_ismi, stok, birim, depo FROM products
        WHERE (urun_kodu LIKE ? OR urun_ismi LIKE ?)
        AND depo LIKE ? AND birim LIKE ?
        LIMIT ? OFFSET ?";

$stmt = $conn->prepare($sql);
$stmt->bind_param("ssssii", $search_term, $search_term, $selected_depo, $selected_birim, $limit, $offset);
$stmt->execute();
$products = $stmt->get_result()->fetch_all(MYSQLI_ASSOC);
$stmt->close();

// Ürün sayısını almak için SQL sorgusu
$sql_count = "SELECT COUNT(*) AS total FROM products
              WHERE (urun_kodu LIKE ? OR urun_ismi LIKE ?)
              AND depo LIKE ? AND birim LIKE ?";

$stmt_count = $conn->prepare($sql_count);
$stmt_count->bind_param("ssss", $search_term, $search_term, $selected_depo, $selected_birim);
$stmt_count->execute();
$total_result = $stmt_count->get_result()->fetch_assoc();
$total_products = $total_result['total'];
$stmt_count->close();

// Sayfalama hesaplamaları
$total_pages = ceil($total_products / $limit);

// Ürün silme işlemi
if (isset($_GET['delete_id'])) {
    $delete_id = $_GET['delete_id'];
    $delete_sql = "DELETE FROM products WHERE id = ?";
    $stmt = $conn->prepare($delete_sql);
    $stmt->bind_param("i", $delete_id);
    $stmt->execute();
    $stmt->close();
    header("Location: index.php");
    exit;
}
?>

<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Stok Takip Sistemi</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>

    <div class="container">
        <header>
            <h1>Stok Takip Sistemi</h1>
        </header>

        <!-- Arama ve Filtreleme Formu -->
        <div class="filter-form">
            <form action="index.php" method="get" class="search-container">
                <input type="text" name="search" placeholder="Ürün Kodu veya İsmi" value="<?php echo isset($_GET['search']) ? $_GET['search'] : ''; ?>" class="search-input">
                
                <select name="depo" class="search-select">
                    <option value="Tümü">Tüm Depolar</option>
                    <?php foreach ($depot_list as $depo) { ?>
                        <option value="<?php echo $depo; ?>" <?php echo isset($_GET['depo']) && $_GET['depo'] === $depo ? 'selected' : ''; ?>><?php echo $depo; ?></option>
                    <?php } ?>
                </select>

                <select name="birim" class="search-select">
                    <option value="Tümü">Tüm Birimler</option>
                    <?php foreach ($unit_list as $unit) { ?>
                        <option value="<?php echo $unit; ?>" <?php echo isset($_GET['birim']) && $_GET['birim'] === $unit ? 'selected' : ''; ?>><?php echo $unit; ?></option>
                    <?php } ?>
                </select>

                <button type="submit" class="search-button">Ara</button>
            </form>
        </div>

        <!-- Ürün Listesi -->
        <table class="product-table">
            <thead>
                <tr>
                    <th>Ürün Kodu</th>
                    <th>Ürün İsmi</th>
                    <th>Stok</th>
                    <th>Birim</th>
                    <th>Depo</th>
                    
                </tr>
            </thead>
            <tbody>
                <?php foreach ($products as $product) { ?>
                    <tr <?php echo $product['stok'] < 20 ? 'class="low-stock"' : ''; ?>>
                        <td><?php echo $product['urun_kodu']; ?></td>
                        <td><?php echo $product['urun_ismi']; ?></td>
                        <td><?php echo $product['stok']; ?></td>
                        <td><?php echo $product['birim']; ?></td>
                        <td><?php echo $product['depo']; ?></td>
                    </tr>
                <?php } ?>
            </tbody>
        </table>

				<!-- Sayfalama -->
		<!-- Sayfalama -->
				<div class="pagination">
					<?php if ($page > 1) { ?>
						<a href="index.php?page=1<?php echo isset($_GET['search']) ? '&search=' . $_GET['search'] : ''; ?>&depo=<?php echo $selected_depo; ?>&birim=<?php echo $selected_birim; ?>" class="page-link">1</a>
						<a href="index.php?page=<?php echo $page - 1; ?><?php echo isset($_GET['search']) ? '&search=' . $_GET['search'] : ''; ?>&depo=<?php echo $selected_depo; ?>&birim=<?php echo $selected_birim; ?>" class="page-link">Önceki</a>
					<?php } ?>

					<?php for ($i = 1; $i <= $total_pages; $i++) { ?>
						<a href="index.php?page=<?php echo $i; ?><?php echo isset($_GET['search']) ? '&search=' . $_GET['search'] : ''; ?>&depo=<?php echo $selected_depo; ?>&birim=<?php echo $selected_birim; ?>" class="page-link <?php echo $i == $page ? 'active' : ''; ?>"><?php echo $i; ?></a>
					<?php } ?>

					<?php if ($page < $total_pages) { ?>
						<a href="index.php?page=<?php echo $page + 1; ?><?php echo isset($_GET['search']) ? '&search=' . $_GET['search'] : ''; ?>&depo=<?php echo $selected_depo; ?>&birim=<?php echo $selected_birim; ?>" class="page-link">Sonraki</a>
					<?php } ?>
				</div>

    </div>

</body>
</html>

<?php $conn->close(); ?>
