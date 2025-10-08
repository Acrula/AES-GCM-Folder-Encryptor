import os
import getpass
import json
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes
from Crypto.Util import Counter

# --- Konstanta ---
KEY_LENGTH = 32  # 256 bits for AES-256
SALT_LENGTH = 16 # 16 bytes for salt
NONCE_LENGTH = 12 # 96 bits for AES-GCM Nonce
ITERATIONS = 100000

def derive_key(password: str, salt: bytes) -> bytes:
    """Menderivasi kunci dari password dan salt menggunakan PBKDF2."""
    return PBKDF2(password.encode('utf-8'), salt, dkLen=KEY_LENGTH, count=ITERATIONS)

def encrypt_file(file_path: str, password: str, output_dir: str):
    """Mengenkeskripsi file tunggal menggunakan AES-GCM."""
    try:
        # 1. Generate Salt dan Key
        salt = get_random_bytes(SALT_LENGTH)
        key = derive_key(password, salt)
        
        # 2. Inisialisasi Cipher (akan menghasilkan Nonce secara otomatis)
        cipher = AES.new(key, AES.MODE_GCM)
        nonce = cipher.nonce # Ambil Nonce yang dibuat

        # 3. Baca konten file
        with open(file_path, 'rb') as f:
            plaintext = f.read()

        # 4. Enkripsi dan buat Authentication Tag
        ciphertext, tag = cipher.encrypt_and_digest(plaintext)

        # 5. Tulis output ke file baru
        encrypted_filename = os.path.basename(file_path) + ".enc"
        output_path = os.path.join(output_dir, encrypted_filename)

        # Format file: Salt + Nonce + Tag + Ciphertext
        with open(output_path, 'wb') as f:
            f.write(salt)
            f.write(nonce)
            f.write(tag)
            f.write(ciphertext)
        
        print(f"  [+] Berhasil mengenkripsi: {file_path} -> {output_path}")

    except Exception as e:
        print(f"  [!] Gagal mengenkripsi {file_path}: {e}")

def decrypt_file(encrypted_file_path: str, password: str, output_dir: str):
    """Mendekripsi file tunggal yang terenkripsi dengan AES-GCM."""
    try:
        # 1. Baca data terenkripsi (Salt, Nonce, Tag, Ciphertext)
        with open(encrypted_file_path, 'rb') as f:
            # Pastikan urutan dan panjang data sesuai saat enkripsi
            salt = f.read(SALT_LENGTH)
            nonce = f.read(NONCE_LENGTH)
            tag = f.read(16) # AES-GCM Tag length is typically 16 bytes
            ciphertext = f.read()

        # 2. Derive Key
        key = derive_key(password, salt)

        # 3. Inisialisasi Cipher
        cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)

        # 4. Dekripsi dan Verifikasi Tag
        plaintext = cipher.decrypt_and_verify(ciphertext, tag)

        # 5. Tulis output ke file baru
        original_filename = os.path.basename(encrypted_file_path)[:-len(".enc")]
        output_path = os.path.join(output_dir, original_filename)
        
        with open(output_path, 'wb') as f:
            f.write(plaintext)
        
        print(f"  [+] Berhasil mendekripsi: {encrypted_file_path} -> {output_path}")

    except ValueError:
        print(f"  [!!!] GAGAL DEKRIPSI/VERIFIKASI TAG untuk: {encrypted_file_path}. Password salah atau file telah diubah.")
    except Exception as e:
        print(f"  [!] Gagal mendekripsi {encrypted_file_path}: {e}")


# BARIS ~100
def process_folder(action: str, input_dir: str, output_dir: str, password: str):
    """Fungsi utama untuk memproses seluruh folder ATAU file tunggal."""
    
    # Periksa apakah input adalah FILE tunggal
    if os.path.isfile(input_dir):
        # Jika itu file, panggil fungsi enkripsi/dekripsi file secara langsung
        os.makedirs(output_dir, exist_ok=True) # Pastikan output folder ada
        
        print(f"\nMode: {action.capitalize()} File Tunggal")
        print(f"Input File: {input_dir}")
        print(f"Output Folder: {output_dir}")
        print("-" * 30)

        if action == 'enkripsi':
            encrypt_file(input_dir, password, output_dir)
        elif action == 'dekripsi' and input_dir.endswith(".enc"):
            decrypt_file(input_dir, password, output_dir)
        elif action == 'dekripsi':
             print(f"  [-] Melewatkan file non-enkripsi: {input_dir} (Harus berakhiran .enc untuk dekripsi)")
        return # Keluar dari fungsi setelah memproses file tunggal

    # Jika input adalah FOLDER (Logika Awal)
    if not os.path.exists(input_dir):
        print(f"Error: Folder input '{input_dir}' tidak ditemukan.")
        return

    # Buat folder output jika belum ada
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"\nMode: {action.capitalize()} Folder")
    print(f"Input: {input_dir}")
    print(f"Output: {output_dir}")
    print("-" * 30)

    for item in os.listdir(input_dir):
        input_path = os.path.join(input_dir, item)
        if os.path.isfile(input_path):
            if action == 'enkripsi': # Ubah dari 'encrypt'
                encrypt_file(input_path, password, output_dir)
            elif action == 'dekripsi' and item.endswith(".enc"): # Ubah dari 'decrypt'
                decrypt_file(input_path, password, output_dir)
            elif action == 'dekripsi' and not item.endswith(".enc"):
                print(f"  [-] Melewatkan file non-enkripsi: {input_path}")


def main_aes_gcm():
    print("--- Aplikasi Enkripsi/Dekripsi Folder AES-GCM ---")
    
    while True:
        mode = input("Pilih mode (enkripsi/dekripsi): ").lower()
        if mode in ['enkripsi', 'dekripsi']:
            break
        print("Pilihan tidak valid. Silakan masukkan 'enkripsi' atau 'dekripsi'.")

    input_folder_name = input("Masukkan nama folder sumber (misalnya: input_folder): ")
    output_folder_name = input(f"Masukkan nama folder tujuan (misalnya: {'encrypted_folder' if mode == 'enkripsi' else 'decrypted_folder'}): ")
    
    password = getpass.getpass("Masukkan password utama: ")
    
    process_folder(mode, input_folder_name, output_folder_name, password)
    print("\nProses selesai.")

if __name__ == "__main__":
    main_aes_gcm()