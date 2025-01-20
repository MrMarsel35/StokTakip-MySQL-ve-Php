<?php
session_start();

// Veritabanı bağlantısı
$servername = "localhost";
$username = "root";
$password = "";
$dbname = "stoktakip2";

$conn = new mysqli($servername, $username, $password, $dbname);
if ($conn->connect_error) {
    die("Bağlantı başarısız: " . $conn->connect_error);
}

if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    $input_username = $_POST['username'];
    $input_password = $_POST['password'];

    // Kullanıcıyı veritabanından kontrol et
    $sql = "SELECT * FROM users WHERE username = ? AND is_active = 1";
    $stmt = $conn->prepare($sql);
    $stmt->bind_param("s", $input_username);
    $stmt->execute();
    $result = $stmt->get_result();

    if ($result->num_rows > 0) {
        // Kullanıcı bulundu, şifreyi kontrol et
        $user = $result->fetch_assoc();
        if ($user['password'] == $input_password) {  // Şifreyi doğrudan kontrol et
            // Başarılı giriş, session'a kullanıcı bilgisini kaydet
            $_SESSION['admin'] = $user['id'];
            header("Location: admin-dashboard.php"); // Yönetici paneline yönlendir
            exit;
        } else {
            $error = "Hatalı şifre!";
        }
    } else {
        $error = "Kullanıcı adı bulunamadı!";
    }
    $stmt->close();
}

$conn->close();
?>

<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0" >
    <title>Admin Girişi</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>

<div class="search-form">
    <h2>Admin Girişi</h2>
    <?php if (isset($error)) { echo "<p class='error'>$error</p>"; } ?>
    <form action="admin-login.php" method="post"  >
        <input type="text" class="search-select" name="username" placeholder="Kullanıcı Adı" required>
        <input type="password" class="search-select" name="password" placeholder="Şifre" required>
        <button type="submit" class="search-button">Giriş Yap</button>
    </form>
</div>

</body>
</html>
