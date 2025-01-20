import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import mysql.connector
import pandas as pd
from tkinter import filedialog


class SearchBar(tk.Entry):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.bind("<KeyRelease>", self.on_key_release)
        self.place(width=350)  
        self.configure(width=20, relief="flat", font=("Arial", 12))  
        self.focus()
        

    def on_key_release(self, event):
        search_text = self.get().strip().lower()


def get_all_depots():
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT DISTINCT depo FROM products")
    depots = cursor.fetchall()
    cursor.close()
    db.close()

    depot_list = ["Tümü"]
    for depot in depots:
        depot_list.append(depot[0])
    return depot_list

def get_all_units():
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT DISTINCT birim FROM products")
    units = cursor.fetchall()
    cursor.close()
    db.close()

    unit_list = ["Tümü"]
    for unit in units:
        unit_list.append(unit[0])
    return unit_list

def fetch_filtered_products():
    search_term = search_entry.get().strip()
    selected_depo = depo_combobox.get()
    selected_birim = birim_combobox.get()

    db = get_db_connection()
    cursor = db.cursor()

    query = """
    SELECT id, urun_kodu, urun_ismi, stok, birim, depo
    FROM products
    WHERE (urun_kodu LIKE %s OR urun_ismi LIKE %s)
    """

    if selected_depo != "Tümü":
        query += " AND depo = %s"
    if selected_birim != "Tümü":
        query += " AND birim = %s"

    params = ['%' + search_term + '%', '%' + search_term + '%']

    if selected_depo != "Tümü":
        params.append(selected_depo)
    if selected_birim != "Tümü":
        params.append(selected_birim)

    cursor.execute(query, tuple(params))

    rows = cursor.fetchall()
    cursor.close()
    db.close()

    for item in product_tree.get_children():
        product_tree.delete(item)

    for row in rows:
        if row[3] < 20:
            product_tree.insert("", tk.END, values=row, tags=("low_stock",))
        else:
            product_tree.insert("", tk.END, values=row)

def fetch_all_products():
    search_term = search_entry.get().strip()
    db = get_db_connection()
    cursor = db.cursor()

    if search_term:
        query = """
        SELECT id, urun_kodu, urun_ismi, stok, birim, depo
        FROM products
        WHERE urun_kodu LIKE %s OR urun_ismi LIKE %s
        """
        cursor.execute(query, ('%' + search_term + '%', '%' + search_term + '%'))
    else:
        query = "SELECT id, urun_kodu, urun_ismi, stok, birim, depo FROM products"
        cursor.execute(query)

    rows = cursor.fetchall()
    cursor.close()
    db.close()

    for item in product_tree.get_children():
        product_tree.delete(item)

    for row in rows:
        if row[3] < 20:
            product_tree.insert("", tk.END, values=row, tags=("low_stock",))
        else:
            product_tree.insert("", tk.END, values=row)
def on_enter(event):
    fetch_filtered_products()

def on_right_click(event):
    selected_item = product_tree.selection()
    if not selected_item:
        return

    urun_id = product_tree.item(selected_item)['values'][0]
    stock_menu.urun_id = urun_id 
    stock_menu.post(event.x_root, event.y_root)

def increase_stock():
    urun_id = stock_menu.urun_id
    amount = simpledialog.askinteger("Stok Artır", "Kaç adet artırmak istersiniz?", minvalue=1)
    if amount is None:  
        return

    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT urun_ismi, urun_kodu, stok, birim, depo FROM products WHERE id = %s", (urun_id,))
    product = cursor.fetchone()
    cursor.close()
    db.close()

    product_name, product_code, stock, unit, depot = product

    update_stock('increase', urun_id, amount)

    add_to_db_history("Stok Artırma", product_name, product_code, stock + amount, unit, depot, f"Miktar: {amount}")



def decrease_stock():
    urun_id = stock_menu.urun_id
    amount = simpledialog.askinteger("Stok Azalt", "Kaç adet azaltmak istersiniz?", minvalue=1)
    if amount is None:  
        return

    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT urun_ismi, urun_kodu, stok, birim, depo FROM products WHERE id = %s", (urun_id,))
    product = cursor.fetchone()
    cursor.close()
    db.close()

    product_name, product_code, stock, unit, depot = product

    update_stock('decrease', urun_id, amount)
    add_to_db_history("Stok Azaltma", product_name, product_code, stock - amount, unit, depot, f"Miktar: {amount}")


def update_stock(action, urun_id, amount):
    db = get_db_connection()
    cursor = db.cursor()

    if action == 'increase':
        query = "UPDATE products SET stok = stok + %s WHERE id = %s"
    elif action == 'decrease':
        query = "UPDATE products SET stok = stok - %s WHERE id = %s"

    cursor.execute(query, (amount, urun_id))
    db.commit()
    cursor.close()
    db.close()
    fetch_filtered_products()

def delete_product():
    urun_id = stock_menu.urun_id
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT urun_ismi, urun_kodu, stok, birim, depo FROM products WHERE id = %s", (urun_id,))
    product = cursor.fetchone()

    if product:
        product_name, product_code, stock, unit, depot = product        
        cursor.execute("DELETE FROM products WHERE id = %s", (urun_id,))
        db.commit()
        add_to_db_history("Ürün Silme", product_name, product_code, stock, unit, depot, f"Ürün ID: {urun_id}")
    
    cursor.close()
    db.close()
    fetch_filtered_products()

def upload_excel_file():
    file_path = filedialog.askopenfilename(
        title="Excel Dosyasını Seçin",
        filetypes=[("Excel Files", "*.xls;*.xlsx")]
    )
    if not file_path:
        messagebox.showwarning("Uyarı", "Lütfen bir dosya seçin.")
        return

    try:
        df = pd.read_excel(file_path)
        db = get_db_connection()
        cursor = db.cursor()
        
        for index, row in df.iterrows():
            urun_kodu = row['Ürün Kodu']
            urun_ismi = row['Ürün İsmi']
            stok = row['Stok']
            birim = row['Birim']
            depo = row['Depolar']

            query = """
            INSERT INTO products (urun_kodu, urun_ismi, stok, birim, depo)
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (urun_kodu, urun_ismi, stok, birim, depo))

        db.commit()
        cursor.close()
        db.close()
        fetch_filtered_products()
        messagebox.showinfo("Başarılı", "Veriler başarıyla yüklendi.")
    except Exception as e:
        messagebox.showerror("Hata", f"Bir hata oluştu: {e}")

def reset_db():
    db = get_db_connection()
    cursor = db.cursor()
    try:
        cursor.execute("DELETE FROM products")
        db.commit()
        messagebox.showinfo("Başarılı", "Veritabanı sıfırlandı.")
    except Exception as e:
        messagebox.showerror("Hata", f"Veritabanı sıfırlanırken bir hata oluştu: {e}")
    finally:
        cursor.close()
        db.close()
    fetch_filtered_products()  
    
def add_to_db_history(action, product_name, product_code, stock, unit, depot, details):    
    db = get_db_connection()
    cursor = db.cursor()
    
    query = """
    INSERT INTO transaction_history (action, product_name, product_code, stock, unit, depot, details, username)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, (action, product_name, product_code, stock, unit, depot, details, current_user))

    db.commit()
    cursor.close()
    db.close()


def open_history_window():
    history_window = tk.Toplevel(window)  
    history_window.title("İşlem Geçmişi")
    history_window.geometry("800x400")

    history_tree = ttk.Treeview(history_window, columns=("username", "action", "product_name", "product_code", "stock", "unit", "depot", "details", "timestamp"), show="headings")

    history_tree.heading("username", text="Kullanıcı Adı")
    history_tree.heading("action", text="İşlem Türü")
    history_tree.heading("product_name", text="Ürün İsmi")
    history_tree.heading("product_code", text="Ürün Kodu")
    history_tree.heading("stock", text="Stok")
    history_tree.heading("unit", text="Birim")
    history_tree.heading("depot", text="Depo")
    history_tree.heading("details", text="Detaylar")
    history_tree.heading("timestamp", text="Tarih")

    columns = [
    ("username", 150),
    ("action", 200),
    ("product_name", 200),
    ("product_code", 150),
    ("stock", 100),
    ("unit", 100),
    ("depot", 100),
    ("details", 250),
    ("timestamp", 150)
    ]

    for col, width in columns:
        history_tree.column(col, anchor="center", width=width)
        
    history_tree.pack(pady=20, fill=tk.BOTH, expand=True)
    
    rows = fetch_db_history()  
    for action, product_name, product_code, stock, unit, depot, details, timestamp, username in rows:
        history_tree.insert("", tk.END, values=(username, action, product_name, product_code, stock, unit, depot, details, timestamp))
        
def fetch_db_history():
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT action, product_name, product_code, stock, unit, depot, details, timestamp, username FROM transaction_history ORDER BY timestamp DESC")
    rows = cursor.fetchall()
    cursor.close()
    db.close()
    return rows


def on_closing():
    global window

    if window is not None and window.winfo_exists():
        try:
            # Burada kapanış işlemlerini yapıyoruz
            print("Kapanıyor...")
            # Örneğin veritabanı bağlantısını kapatma işlemi
            # db.close()

            window.quit()  # Mainloop'u sonlandır
            window.destroy()  # Pencereyi yok et
        except Exception as e:
            print(f"Bir hata oluştu: {e}")
    else:
        print("Pencere zaten kapalı!")




def open_main_window():
    global window, product_tree, stock_menu, search_entry, depo_combobox, birim_combobox, filter_frame
   
    window = tk.Tk()
    window.title("Stok Takip Sistemi")
    window.geometry("800x600")
    window.configure(bg="#f2f2f2")

    window.protocol("WM_DELETE_WINDOW", on_closing)
    
    buttons_frame = tk.Frame(window, bg="#f2f2f2")
    buttons_frame.pack(pady=10)

    history_button = tk.Button(buttons_frame, text="İşlem Geçmişi", command=open_history_window, bg="#FFC107", fg="white", relief="flat", height=2, width=15)
    history_button.pack(side=tk.LEFT, padx=5)

    user_label = tk.Label(window, text=f"Hoşgeldiniz, {current_user}", font=("Helvetica", 12), bg="#f2f2f2")
    user_label.pack(pady=10)
    
    style = ttk.Style()
    style.configure("Treeview.Heading", font=("Arial", 12, "bold"))
    style.configure("Treeview", font=("Arial", 10), rowheight=25)
    style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])

    
    columns = ("id", "urun_kodu", "urun_ismi", "stok", "birim", "depo")
    product_tree = ttk.Treeview(window, columns=columns, show="headings", height=15)

    product_tree.heading("urun_kodu", text="Ürün Kodu")
    product_tree.heading("urun_ismi", text="Ürün İsmi")
    product_tree.heading("stok", text="Stok")
    product_tree.heading("birim", text="Birim")
    product_tree.heading("depo", text="Depo")

    product_tree.column("id", width=0, stretch=tk.NO)

    product_tree.column("urun_kodu", anchor="center", width=150)  
    product_tree.column("urun_ismi", anchor="center", width=200) 
    product_tree.column("stok", anchor="center")
    product_tree.column("birim", anchor="center")
    product_tree.column("depo", anchor="center")

    product_tree.tag_configure("low_stock", background="white", foreground="red")

    product_tree.pack(pady=20, fill=tk.BOTH, expand=True)

    search_frame = tk.Frame(window, bg="#f2f2f2")
    search_frame.pack(pady=10)

    search_label = tk.Label(search_frame, text="Ürün Kodu veya İsmi:", bg="#f2f2f2")
    search_label.pack(side=tk.LEFT, padx=5)

    search_entry = SearchBar(search_frame)
    search_entry.pack(side=tk.LEFT, padx=5)

    buttons_frame = tk.Frame(window, bg="#f2f2f2")
    buttons_frame.pack(pady=10)

    search_button = tk.Button(buttons_frame, text="Ara", command=fetch_filtered_products, bg="#4CAF50", fg="white", relief="flat", height=2, width=10)
    search_button.pack(side=tk.LEFT, padx=5)

    upload_button = tk.Button(buttons_frame, text="Excel'den Yükle", command=upload_excel_file, bg="#2196F3", fg="white", relief="flat", height=2, width=15)
    upload_button.pack(side=tk.LEFT, padx=5)

    reset_button = tk.Button(buttons_frame, text="DB'yi Sıfırla", command=reset_db, bg="#FF5722", fg="white", relief="flat", height=2, width=12)
    reset_button.pack(side=tk.LEFT, padx=5)

    filter_button = tk.Button(buttons_frame, text="Filtreleri Göster", command=lambda: toggle_filters(), bg="#FFC107", fg="white", relief="flat", height=2, width=15)
    filter_button.pack(side=tk.LEFT, padx=5)
    filter_frame = tk.Frame(window, bg="#f2f2f2")
    filter_frame.pack_forget()  

    
    center_frame = tk.Frame(filter_frame, bg="#f2f2f2")
    center_frame.pack(side=tk.TOP, pady=10)

   
    depot_list = get_all_depots()
    unit_list = get_all_units()

   
    depo_label = tk.Label(center_frame, text="Depo:", bg="#f2f2f2")
    depo_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

    depo_combobox = ttk.Combobox(center_frame, values=depot_list)
    depo_combobox.set("Tümü")  
    depo_combobox.grid(row=0, column=1, padx=5, pady=5)

    birim_label = tk.Label(center_frame, text="Birim:", bg="#f2f2f2")
    birim_label.grid(row=0, column=2, padx=5, pady=5, sticky="w")

    birim_combobox = ttk.Combobox(center_frame, values=unit_list)
    birim_combobox.set("Tümü")  
    birim_combobox.grid(row=0, column=3, padx=5, pady=5)
   
    stock_menu = tk.Menu(window, tearoff=0)
    stock_menu.add_command(label="Stok Artır", command=increase_stock)
    stock_menu.add_command(label="Stok Azalt", command=decrease_stock)
    stock_menu.add_command(label="Ürünü Sil", command=delete_product)

    product_tree.bind("<Button-3>", on_right_click) 
    search_entry.bind("<Return>", on_enter)

    fetch_all_products()


def toggle_filters():
    if filter_frame.winfo_ismapped():
        depo_combobox.set("Tümü")
        birim_combobox.set("Tümü")
        filter_frame.pack_forget()
    else:
        filter_frame.pack(fill=tk.X, padx=10, pady=5)

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="stoktakip2"
    )


def login_user():
    global login_username_entry, login_password_entry, login_window, current_user
    username = login_username_entry.get()
    password = login_password_entry.get()

    if not username or not password:
        messagebox.showwarning("Eksik Bilgi", "Lütfen tüm alanları doldurun.")
        return

    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
    user = cursor.fetchone()

    if user:        
        if user[4] == 1:  
            messagebox.showinfo("Başarılı Giriş", "Başarıyla giriş yaptınız.")
            current_user = user[1]  
            login_window.destroy()  
            open_main_window()  # Ana pencereyi açıyoruz
        else:
            messagebox.showerror("Hata", "Hesabınız aktif değil. Lütfen yöneticinizle iletişime geçin.")
    else:
        messagebox.showerror("Hata", "Kullanıcı adı veya şifre hatalı.")
    
    cursor.close()
    db.close()



def sign_up_user():
    username = signup_username_entry.get()
    password = signup_password_entry.get()
    email = signup_email_entry.get()

    if not username or not password or not email:
        messagebox.showwarning("Eksik Bilgi", "Lütfen tüm alanları doldurun.")
        return

    db = get_db_connection()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM users WHERE username = %s OR email = %s", (username, email))
    existing_user = cursor.fetchone()

    if existing_user:
        messagebox.showerror("Hata", "Bu kullanıcı adı veya e-posta adresi zaten kayıtlı.")
    else:
        cursor.execute("INSERT INTO users (username, password, email) VALUES (%s, %s, %s)", (username, password, email))
        db.commit()
        messagebox.showinfo("Başarılı Kayıt", "Kayıt başarılı! Giriş yapabilirsiniz.")
    
    cursor.close()
    db.close()


def open_signup_window():
    signup_window = tk.Toplevel()  # Kayıt penceresini açıyoruz
    signup_window.title("Kayıt Ol")
    signup_window.geometry("400x350")
    signup_window.configure(bg="#f0f0f0")

    signup_label = tk.Label(signup_window, text="Kayıt Ol", font=("Helvetica", 18, "bold"), fg="#2C3E50", bg="#f0f0f0")
    signup_label.pack(pady=20)

    tk.Label(signup_window, text="Kullanıcı Adı:", font=("Helvetica", 12), bg="#f0f0f0", fg="#34495E").pack(pady=5)
    signup_username_entry = tk.Entry(signup_window, font=("Helvetica", 12), relief="solid", bd=1, width=30)
    signup_username_entry.pack(pady=10)

    tk.Label(signup_window, text="Şifre:", font=("Helvetica", 12), bg="#f0f0f0", fg="#34495E").pack(pady=5)
    signup_password_entry = tk.Entry(signup_window, show="*", font=("Helvetica", 12), relief="solid", bd=1, width=30)
    signup_password_entry.pack(pady=10)

    signup_button = tk.Button(signup_window, text="Kayıt Ol", font=("Helvetica", 12), bg="#2980B9", fg="white", relief="flat", width=30)
    signup_button.pack(pady=10)


def open_login_window():
    global login_username_entry, login_password_entry, login_window
    
    login_window = tk.Toplevel()  # Yeni login penceresi oluşturuyoruz
    login_window.title("Giriş Yap")
    login_window.geometry("400x350")
    login_window.configure(bg="#f0f0f0")

    login_label = tk.Label(login_window, text="Kullanıcı Girişi", font=("Helvetica", 18, "bold"), fg="#2C3E50", bg="#f0f0f0")
    login_label.pack(pady=20)

    tk.Label(login_window, text="Kullanıcı Adı:", font=("Helvetica", 12), bg="#f0f0f0", fg="#34495E").pack(pady=5)
    login_username_entry = tk.Entry(login_window, font=("Helvetica", 12), relief="solid", bd=1, width=30)
    login_username_entry.pack(pady=10)
    

    tk.Label(login_window, text="Şifre:", font=("Helvetica", 12), bg="#f0f0f0", fg="#34495E").pack(pady=5)
    login_password_entry = tk.Entry(login_window, show="*", font=("Helvetica", 12), relief="solid", bd=1, width=30)
    login_password_entry.pack(pady=10)

    login_button = tk.Button(login_window, text="Giriş Yap", font=("Helvetica", 12), bg="#2980B9", fg="white", relief="flat", width=30, command=login_user)
    login_button.pack(pady=10)

    signup_button = tk.Button(login_window, text="Kayıt Ol", font=("Helvetica", 12), bg="#27AE60", fg="white", relief="flat", width=30, command=open_signup_window)  # Kayıt ol butonuna işlev ekliyoruz
    signup_button.pack(pady=10)



if __name__ == "__main__":
    root = tk.Tk()  # Ana pencereyi başlatıyoruz
    root.withdraw()  # Ana pencereyi gizliyoruz
    open_login_window()  # login pencersini açıyoruz
    root.mainloop()
      
