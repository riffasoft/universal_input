import os
import re
import time
import getpass
import glob

def universal_input(
    title="Masukkan nilai:",
    data_type="str",            # str, int, float, option, password, multiselect, file, folder, fileselect
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
    confirm_create=True,        # konfirmasi dulu sebelum auto-create
    file_filter="*",           # filter file untuk fileselect (string atau list)
    scan_directory=".",         # direktori untuk scan file
    output_type="fullpath"     # "fullpath", "relative", "filename" untuk fileselect
):
    
    """
    Fungsi input interaktif dengan validasi otomatis.

    Parameters
    ----------
    title : str
        Pesan prompt.
    data_type : str
        Jenis data input. Pilihan:
        - "str"
        - "int"
        - "float"
        - "option"
        - "password"
        - "multiselect"
        - "file"
        - "folder"
        - "fileselect"
    options : list, optional
        Opsi pilihan jika data_type="option" atau "multiselect".
    default : Any, optional
        Nilai default jika input kosong / gagal.
    error_message : str
        Pesan jika validasi gagal.
    use_default_on_error : bool
        Gunakan default jika input gagal divalidasi.
    allow_empty : bool
        Boleh kosong.
    validator : Callable, optional
        Fungsi validasi custom.
    regex : str, optional
        Regex untuk validasi tambahan.
    max_retry : int, optional
        Jumlah percobaan maksimal.
    timeout : int, optional
        Timeout dalam detik.
    auto_create : bool
        Buat file/folder jika tidak ada.
    confirm_create : bool
        Konfirmasi sebelum auto-create.
    file_filter : str atau list
        Filter file untuk fileselect (contoh: "*.py", ["csv", "txt"], ["*.jpg", "*.png"]).
    scan_directory : str
        Direktori untuk scan file.
    output_type : str
        Tipe output untuk fileselect: "fullpath", "relative", "filename".

    Returns
    -------
    Any
        Nilai input sesuai data_type.
    """
    
    start_time = time.time()
    attempts = 0
    
    while True:
        # Timeout check
        if timeout and (time.time() - start_time > timeout):
            print(f"\n⏰ Timeout! menggunakan default: {default}")
            return default

        # Prompt khusus untuk fileselect
        if data_type == "fileselect":
            # Process file filter (support both string and list)
            if isinstance(file_filter, list):
                patterns = []
                for filter_item in file_filter:
                    if filter_item.startswith('*.'):
                        # Already a wildcard pattern like "*.txt"
                        patterns.append(os.path.join(scan_directory, filter_item))
                    elif filter_item.startswith('.'):
                        # Extension like ".txt" -> convert to "*.txt"
                        patterns.append(os.path.join(scan_directory, f"*{filter_item}"))
                    else:
                        # Extension without dot like "txt" -> convert to "*.txt"
                        patterns.append(os.path.join(scan_directory, f"*.{filter_item}"))
            else:
                # Single string filter
                if file_filter.startswith('*.'):
                    patterns = [os.path.join(scan_directory, file_filter)]
                elif file_filter.startswith('.'):
                    patterns = [os.path.join(scan_directory, f"*{file_filter}")]
                else:
                    patterns = [os.path.join(scan_directory, f"*.{file_filter}")]
            
            # Scan files based on patterns
            files = []
            for pattern in patterns:
                matched_files = sorted([f for f in glob.glob(pattern) if os.path.isfile(f)])
                files.extend(matched_files)
            
            # Remove duplicates and sort
            files = sorted(list(set(files)))
            
            if not files:
                filter_desc = file_filter if isinstance(file_filter, str) else ", ".join(file_filter)
                print(f"❌ Tidak ditemukan file dengan filter '{filter_desc}' di direktori '{scan_directory}'")
                if use_default_on_error and default is not None:
                    print(f"→ menggunakan default: {default}")
                    return default
                elif max_retry and attempts >= max_retry:
                    print("❌ Terlalu banyak percobaan. menggunakan default.")
                    return default
                else:
                    attempts += 1
                    continue
            
            print(f"\n{title}")
            print("Daftar file yang tersedia:")
            
            # Prepare files for display and output
            display_files = []
            output_files = []
            
            for file in files:
                # Determine what to display and return based on output_type
                if output_type == "filename":
                    display_name = os.path.basename(file)
                    return_value = os.path.basename(file)
                elif output_type == "relative":
                    display_name = os.path.relpath(file)
                    return_value = os.path.relpath(file)
                else:  # fullpath (default)
                    display_name = os.path.abspath(file)
                    return_value = os.path.abspath(file)
                
                display_files.append((file, display_name))
                output_files.append(return_value)
            
            # Display files with numbering
            for i, (original_path, display_name) in enumerate(display_files, 1):
                file_size = os.path.getsize(original_path)
                file_mtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(os.path.getmtime(original_path)))
                
                # Check if this file is the default
                is_default = False
                if default is not None:
                    if output_type == "filename" and os.path.basename(original_path) == default:
                        is_default = True
                    elif output_type == "relative" and os.path.relpath(original_path) == default:
                        is_default = True
                    elif output_type == "fullpath" and os.path.abspath(original_path) == default:
                        is_default = True
                
                mark = " (default)" if is_default else ""
                print(f" {i:2d}. {display_name} [{file_size} bytes, modified: {file_mtime}]{mark}")
            
            prompt = f"Pilih file (1-{len(files)})"
            if output_type == "filename":
                prompt += " [output: nama file]"
            elif output_type == "relative":
                prompt += " [output: relative path]"
            else:
                prompt += " [output: full path]"
            prompt += ": "
            
            raw = input(prompt).strip()
            
            # Handle input kosong
            if raw == "":
                if default is not None:
                    print(f"✅ Menggunakan default: {default}")
                    return default
                elif allow_empty:
                    return None
                else:
                    print(error_message)
                    attempts += 1
                    continue
            
            # Validasi pilihan
            if raw.isdigit():
                choice = int(raw)
                if 1 <= choice <= len(files):
                    selected_file = output_files[choice - 1]
                    print(f"✅ File dipilih: {selected_file}")
                    return selected_file
                else:
                    print(f"{error_message} (Pilihan harus antara 1-{len(files)})")
            else:
                # Jika user input nama file langsung, try to match
                matched_files = []
                for i, (original_path, display_name) in enumerate(display_files):
                    if raw == display_name or raw == os.path.basename(original_path):
                        matched_files.append((i, output_files[i]))
                
                if len(matched_files) == 1:
                    selected_file = matched_files[0][1]
                    print(f"✅ File dipilih: {selected_file}")
                    return selected_file
                elif len(matched_files) > 1:
                    print(f"❌ Multiple files match '{raw}'. Please use number selection:")
                    for idx, (orig_idx, file_out) in enumerate(matched_files, 1):
                        print(f"     {idx}. {file_out}")
                else:
                    print(f"{error_message} (File '{raw}' tidak ditemukan dalam daftar)")
            
            attempts += 1
            
            # Check max retry
            if max_retry and attempts >= max_retry:
                print("❌ Terlalu banyak percobaan. menggunakan default.")
                return default
            
            continue

        # Prompt untuk tipe data lainnya (kode asli) - tetap sama seperti sebelumnya
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
