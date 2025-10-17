# 📌 `universal_input` – Fungsi Utilities Input Serbaguna di Python

## ✨ Deskripsi

`universal_input` adalah fungsi Utilities Python serbaguna untuk mengambil input dari user dengan validasi otomatis sesuai tipe data yang diinginkan.
Fungsi ini mendukung berbagai jenis input, mulai dari **string**, **integer**, **float**, **option (pilihan)**, hingga **file** dan **folder** dengan pengecekan keberadaan serta opsi **auto-create**.

Fitur ini berguna untuk membuat aplikasi CLI yang lebih **user-friendly**, **aman**, dan **fleksibel**.

---

## 🚀 Fitur Utama

* Mendukung berbagai `data_type`:

  * `"string"` → teks bebas
  * `"int"` → bilangan bulat
  * `"float"` → bilangan desimal
  * `"option"` → memilih dari daftar pilihan
  * `"file"` → path file dengan pengecekan eksistensi
  * `"folder"` → path folder dengan pengecekan eksistensi
* Dukungan **default value** bila user tidak mengisi.
* Validasi otomatis dengan **error message** kustom.
* Pilihan apakah input salah akan **diulang** atau langsung gunakan **default**.
* Untuk `file` dan `folder`:

  * Bisa cek apakah path ada.
  * Jika tidak ada, bisa **auto-create** (opsional).
  * Dengan **konfirmasi [y/n]** sebelum membuat.

---

## ⚙️ Parameter Fungsi

```python
def universal_input(
    title: str,
    data_type: str = "string",
    default=None,
    error_message: str = "Input tidak valid.",
    options: list = None,
    allow_retry: bool = True,
    auto_create: bool = False,
    confirm_create: bool = True
):
```

| Parameter          | Tipe   | Deskripsi                                                                                           |
| ------------------ | ------ | --------------------------------------------------------------------------------------------------- |
| **title**          | `str`  | Pesan prompt untuk user.                                                                            |
| **data_type**      | `str`  | Jenis data input. Pilihan: `"string"`, `"int"`, `"float"`, `"option"`, `"file"`, `"folder"`.        |
| **default**        | `any`  | Nilai default bila user tidak mengisi atau input salah.                                             |
| **error_message**  | `str`  | Pesan error yang ditampilkan jika input tidak valid.                                                |
| **options**        | `list` | Hanya dipakai bila `data_type="option"`. Berisi daftar pilihan yang valid.                          |
| **allow_retry**    | `bool` | Jika `True`, user akan ditanya ulang sampai benar. Jika `False`, langsung pakai default bila salah. |
| **auto_create**    | `bool` | Untuk `file` / `folder`. Jika `True`, akan otomatis membuat jika path tidak ada.                    |
| **confirm_create** | `bool` | Jika `True`, user akan ditanya konfirmasi `[y/n]` sebelum auto-create file/folder.                  |

---

## 🔄 Return Value

* Mengembalikan **nilai input** sesuai `data_type`.
* Jika input tidak valid dan `allow_retry=False`, maka akan mengembalikan `default`.

---

## 📖 Contoh Penggunaan

### 1. Input String

```python
nama = universal_input("Masukkan nama Anda", data_type="string", default="Anonim")
print("Halo,", nama)
```

### 2. Input Integer

```python
umur = universal_input("Masukkan umur Anda", data_type="int", default=18)
print("Umur:", umur)
```

### 3. Input Float

```python
nilai = universal_input("Masukkan nilai ujian", data_type="float", default=0.0)
print("Nilai ujian:", nilai)
```

### 4. Input Option (Pilihan)

```python
warna = universal_input(
    "Pilih warna favorit",
    data_type="option",
    options=["merah", "hijau", "biru"],
    default="merah"
)
print("Warna favorit Anda:", warna)
```

### 5. Input File (dengan auto-create)

```python
file_path = universal_input(
    "Masukkan path file konfigurasi",
    data_type="file",
    default="config.json",
    auto_create=True,          # otomatis buat jika tidak ada
    confirm_create=True        # minta konfirmasi dulu
)
print("File yang dipilih:", file_path)
```

### 6. Input Folder (dengan auto-create)

```python
folder_path = universal_input(
    "Masukkan folder output",
    data_type="folder",
    default="output",
    auto_create=True,
    confirm_create=True
)
print("Folder output:", folder_path)
```

---

### 7. Input Folder (dengan Piilhan file index)

```python
# Contoh 1: Filter array dengan output nama file saja
file_python = universal_input(
    title="Silakan pilih file Python:",
    data_type="fileselect",
    file_filter=["csv", "txt"],
    scan_directory="./csv",
    output_type="filename"
)
print(file_python)  # Output: data.csv (hanya nama file)

# Contoh 2: Filter array dengan output full path
file_python = universal_input(
    title="Silakan pilih file Python:",
    data_type="fileselect", 
    file_filter=["csv", "txt"],
    scan_directory="./csv",
    output_type="fullpath"
)
print(file_python)  # Output: /home/user/project/csv/data.csv (full path)

# Contoh 3: Filter array dengan output relative path
file_python = universal_input(
    title="Silakan pilih file Python:",
    data_type="fileselect",
    file_filter=["csv", "txt"], 
    scan_directory="./csv",
    output_type="relative"
)
print(file_python)  # Output: ./csv/data.csv (relative path)

# Contoh 4: Mixed filter patterns
file_gambar = universal_input(
    title="Pilih file gambar:",
    data_type="fileselect",
    file_filter=["*.jpg", "png", ".gif"],  # Support berbagai format
    output_type="filename"
)
```


## 🛠️ Catatan

* Untuk `file`, jika `auto_create=True`, fungsi akan membuat file kosong jika belum ada.
* Untuk `folder`, jika `auto_create=True`, fungsi akan membuat folder baru jika belum ada.
* Jika `confirm_create=True`, user akan diminta konfirmasi sebelum proses pembuatan.

---

