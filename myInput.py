import os
import re
import time
import getpass

def myInput(
    title="Masukkan nilai:",
    data_type="str",            # str, int, float, option, password, multiselect, file, folder
    options=None,
    default=None,
    error_message="Input tidak valid!",
    use_default_on_error=False,
    allow_empty=False,
    validator=None,             # fungsi custom validasi
    regex=None,                 # validasi regex
    max_retry=None,             # jumlah percobaan maksimal
    timeout=None,               # detik sebelum auto default
    auto_create=False,          # buat file/folder kalau tidak ada
    confirm_create=True         # konfirmasi dulu sebelum auto-create
):
    start_time = time.time()
    attempts = 0
    
    while True:
        # Timeout check
        if timeout and (time.time() - start_time > timeout):
            print(f"\n⏰ Timeout! menggunakan default: {default}")
            return default

        # Prompt
        if data_type == "option" and options:
            print(f"\n{title}")
            for i, opt in enumerate(options, 1):
                mark = " (default)" if opt == default else ""
                print(f" {i}. {opt}{mark}")
            prompt = f"Pilih (1-{len(options)} / teks): "
        else:
            prompt = f"{title} "
            if default is not None:
                prompt += f"(Default: {default}) "

        # Input (khusus password)
        raw = getpass.getpass(prompt) if data_type == "password" else input(prompt)
        raw = raw.strip()

        # Handle kosong
        if raw == "":
            if default is not None:
                return default
            elif allow_empty:
                return None
            else:
                print(error_message)
                attempts += 1
                continue

        try:
            # Tipe data dasar
            if data_type == "int":
                val = int(raw)
            elif data_type == "float":
                val = float(raw)
            elif data_type == "option":
                if raw.isdigit() and 1 <= int(raw) <= len(options):
                    val = options[int(raw)-1]
                elif raw in options:
                    val = raw
                else:
                    raise ValueError
            elif data_type == "multiselect":
                val = []
                parts = [p.strip() for p in raw.split(",")]
                for p in parts:
                    if p.isdigit() and 1 <= int(p) <= len(options):
                        val.append(options[int(p)-1])
                    elif p in options:
                        val.append(p)
                    else:
                        raise ValueError
            elif data_type == "file":
                if os.path.isfile(raw):
                    val = raw
                else:
                    if auto_create:
                        if confirm_create:
                            jawab = input(f"📄 File '{raw}' tidak ada, buat baru? [y/n]: ").lower()
                            if jawab != "y":
                                raise ValueError("File tidak dibuat.")
                        # Buat folder induk jika perlu
                        folder = os.path.dirname(raw)
                        if folder and not os.path.exists(folder):
                            os.makedirs(folder, exist_ok=True)
                        open(raw, "w").close()
                        print(f"✅ File baru dibuat: {raw}")
                        val = raw
                    else:
                        raise ValueError("File tidak ditemukan!")
            elif data_type == "folder":
                if os.path.isdir(raw):
                    val = raw
                else:
                    if auto_create:
                        if confirm_create:
                            jawab = input(f"📂 Folder '{raw}' tidak ada, buat baru? [y/n]: ").lower()
                            if jawab != "y":
                                raise ValueError("Folder tidak dibuat.")
                        os.makedirs(raw, exist_ok=True)
                        print(f"✅ Folder baru dibuat: {raw}")
                        val = raw
                    else:
                        raise ValueError("Folder tidak ditemukan!")
            else:  # str / password
                val = str(raw)

            # Regex check
            if regex and not re.fullmatch(regex, str(val)):
                raise ValueError("Regex tidak cocok!")

            # Validator check
            if validator and not validator(val):
                raise ValueError("Validator gagal!")

            return val

        except Exception as e:
            if use_default_on_error and default is not None:
                print(f"{error_message} → menggunakan default: {default}")
                return default
            else:
                print(f"{error_message} ({e})")
                attempts += 1

        # Check max retry
        if max_retry and attempts >= max_retry:
            print("❌ Terlalu banyak percobaan. menggunakan default.")
            return default


# ==============================
# CONTOH PENGGUNAAN
# ==============================

# Input file dengan auto-create + konfirmasi
path_file = myInput(
    "Masukkan path file:", 
    data_type="file", 
    error_message="Path file tidak valid!", 
    default="example.txt",
    auto_create=True,
    confirm_create=True
)

# Input folder dengan auto-create + konfirmasi
path_folder = myInput(
    "Masukkan path folder:", 
    data_type="folder", 
    error_message="Path folder tidak valid!", 
    default="./data",
    auto_create=True,
    confirm_create=True
)

print("\nHasil Input:")
print("File   :", path_file)
print("Folder :", path_folder)
