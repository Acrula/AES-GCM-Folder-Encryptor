# encryptor.py

import os
import sys
import getpass
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes

# ==============================================================================
# --- KONFIGURASI FOLDER ---
# !!! PENTING: Pastikan nama folder di bawah ini SAMA PERSIS dengan nama
# folder yang ada di komputer Anda.
# ==============================================================================
FOLDER_ASLI           = 'input_folder'         # Folder sumber berisi file asli
FOLDER_TERENKRIPSI    = 'data_terenkripsi'     # Folder tujuan untuk file .enc
FOLDER_HASIL_DEKRIPSI = 'data_hasil_dekripsi'  # Folder tujuan untuk file hasil dekripsi
# ==============================================================================

# --- Konstanta Kriptografi ---
KEY_LENGTH = 32      # AES-256
SALT_LENGTH = 16     # Standar industri
ITERATIONS = 100000  # Jumlah iterasi PBKDF2

def derive_key(password: str, salt: bytes) -> bytes:
    """Menderivasi kunci dari password dan salt menggunakan PBKDF2."""
    return PBKDF2(password.encode('utf-8'), salt, dkLen=KEY_LENGTH, count=ITERATIONS)

def encrypt_file(file_path: str, password: str, output_dir: str):
    """Mengenkripsi satu file menggunakan AES-GCM."""
    try:
        salt = get_random_bytes(SALT_LENGTH)
        key = derive_key(password, salt)

        cipher = AES.new(key, AES.MODE_GCM)
        nonce = cipher.nonce

        with open(file_path, 'rb') as f:
            plaintext = f.read()

        ciphertext, tag = cipher.encrypt_and_digest(plaintext)

        encrypted_filename = os.path.basename(file_path) + ".enc"
        output_path = os.path.join(output_dir, encrypted_filename)

        with open(output_path, 'wb') as f:
            # Simpan panjang setiap bagian agar dekripsi akurat
            f.write(len(salt).to_bytes(1, 'big'))
            f.write(salt)
            f.write(len(nonce).to_bytes(1, 'big'))
            f.write(nonce)
            f.write(len(tag).to_bytes(1, 'big'))
            f.write(tag)
            f.write(ciphertext)

        print(f"  [+] Berhasil mengenkripsi: {os.path.basename(file_path)}")
    except Exception as e:
        print(f"  [!] Gagal mengenkripsi {os.path.basename(file_path)}: {e}")

def decrypt_file(encrypted_file_path: str, password: str, output_dir: str):
    """Mendekripsi dan memverifikasi satu file AES-GCM."""
    try:
        with open(encrypted_file_path, 'rb') as f:
            salt_len = int.from_bytes(f.read(1), 'big')
            salt = f.read(salt_len)

            nonce_len = int.from_bytes(f.read(1), 'big')
            nonce = f.read(nonce_len)

            tag_len = int.from_bytes(f.read(1), 'big')
            tag = f.read(tag_len)

            ciphertext = f.read()

        key = derive_key(password, salt)
        cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
        plaintext = cipher.decrypt_and_verify(ciphertext, tag)

        original_filename = os.path.basename(encrypted_file_path)[:-len(".enc")]
        output_path = os.path.join(output_dir, original_filename)

        with open(output_path, 'wb') as f:
            f.write(plaintext)

        print(f"  [+] Berhasil mendekripsi: {os.path.basename(encrypted_file_path)}")
    except ValueError:
        print(f"  [!!!] GAGAL DEKRIPSI: {os.path.basename(encrypted_file_path)}. Password salah atau file korup/diubah.")
    except Exception as e:
        print(f"  [!] Gagal mendekripsi {os.path.basename(encrypted_file_path)}: {e}")

def process_folder(mode: str, input_dir: str, output_dir: str, password: str):
    """Fungsi utama untuk memproses seluruh file dalam sebuah folder."""
    if not os.path.isdir(input_dir):
        print(f"\n[ERROR] Folder sumber '{input_dir}' tidak ditemukan!")
        print("Mohon periksa kembali bagian 'KONFIGURASI FOLDER' di dalam kode.")
        return

    # Hapus folder output lama agar hasil baru bersih
    if os.path.exists(output_dir):
        for f in os.listdir(output_dir):
            os.remove(os.path.join(output_dir, f))
    else:
        os.makedirs(output_dir)

    print("-" * 40)
    print(f"Mode: {mode.upper()}")
    print(f"Folder Sumber: '{input_dir}'")
    print(f"Folder Tujuan: '{output_dir}'")
    print("-" * 40)

    files_in_dir = os.listdir(input_dir)
    if not files_in_dir:
        print("  [-] Folder sumber kosong, tidak ada file yang diproses.")

    for item in files_in_dir:
        input_path = os.path.join(input_dir, item)
        if os.path.isfile(input_path):
            if mode == 'enkripsi':
                encrypt_file(input_path, password, output_dir)
            elif mode == 'dekripsi':
                if item.endswith(".enc"):
                    decrypt_file(input_path, password, output_dir)
                else:
                    print(f"  [-] Melewatkan file non-enkripsi: {item}")

    print("-" * 40)
    print("Proses selesai.")

def main():
    """Fungsi utama untuk menjalankan program interaktif."""
    try:
        password = getpass.getpass("Masukkan password utama: ")
        if not password:
            print("\n[ERROR] Password tidak boleh kosong.")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\nProses dibatalkan.")
        sys.exit()

    while True:
        print("\n--- Pilihan Mode ---")
        print("1. Enkripsi Folder")
        print("2. Dekripsi Folder")
        choice = input("Masukkan pilihan (1/2, atau 'q' untuk keluar): ").strip().lower()

        if choice == '1':
            mode, input_folder, output_folder = 'enkripsi', FOLDER_ASLI, FOLDER_TERENKRIPSI
            break
        elif choice == '2':
            mode, input_folder, output_folder = 'dekripsi', FOLDER_TERENKRIPSI, FOLDER_HASIL_DEKRIPSI
            break
        elif choice == 'q':
            print("Program dihentikan.")
            sys.exit()
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")

    process_folder(
        mode=mode,
        input_dir=input_folder,
        output_dir=output_folder,
        password=password
    )

if __name__ == "__main__":
    main()
