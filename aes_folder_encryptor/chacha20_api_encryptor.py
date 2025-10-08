import os
import json
from base64 import urlsafe_b64encode, urlsafe_b64decode
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.exceptions import InvalidTag # Harus diimpor secara eksplisit

# --- Konstanta ---
KEY_LENGTH = 32  # 256 bits
NONCE_LENGTH = 12 # 96 bits for ChaCha20Poly1305
SALT_LENGTH = 16

def derive_key(password: str, salt: bytes) -> bytes:
    """Menderivasi kunci dari password menggunakan PBKDF2."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=KEY_LENGTH,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return kdf.derive(password.encode('utf-8'))

def encrypt_api_payload(payload_data: dict, password: str) -> dict:
    """
    Enkripsi payload data (sisi Klien).
    Menggunakan ChaCha20-Poly1305 (AEAD).
    """
    # 1. Generate Salt dan Key
    salt = os.urandom(SALT_LENGTH)
    key = derive_key(password, salt)
    
    # 2. Inisialisasi AEAD dan Nonce
    aead = ChaCha20Poly1305(key)
    nonce = os.urandom(NONCE_LENGTH)
    
    # 3. Serialize data (misalnya JSON ke bytes)
    plaintext = json.dumps(payload_data).encode('utf-8')
    
    # 4. Enkripsi
    # Associated Data (AAD) diatur ke None untuk simplisitas
    ciphertext_with_tag = aead.encrypt(nonce, plaintext, associated_data=None)
    
    # 5. Format Output untuk pengiriman API (Base64 URL-safe)
    encrypted_payload = {
        "salt": urlsafe_b64encode(salt).decode('utf-8'),
        "nonce": urlsafe_b64encode(nonce).decode('utf-8'),
        "data": urlsafe_b64encode(ciphertext_with_tag).decode('utf-8')
    }
    
    return encrypted_payload

def decrypt_api_payload(encrypted_payload: dict, password: str) -> dict:
    """
    Dekripsi dan verifikasi payload data (sisi Server).
    """
    try:
        # 1. Decode dari Base64
        salt = urlsafe_b64decode(encrypted_payload['salt'])
        nonce = urlsafe_b64decode(encrypted_payload['nonce'])
        ciphertext_with_tag = urlsafe_b64decode(encrypted_payload['data'])
        
        # 2. Derive Key
        key = derive_key(password, salt)

        # 3. Inisialisasi AEAD
        aead = ChaCha20Poly1305(key)

        # 4. Dekripsi dan Verifikasi Tag
        # InvalidTag akan dilemparkan di sini jika tag tidak cocok
        plaintext_bytes = aead.decrypt(nonce, ciphertext_with_tag, associated_data=None)
        
        # 5. Deserialize data (bytes ke JSON)
        plaintext_data = json.loads(plaintext_bytes.decode('utf-8'))
        
        return {"status": "SUCCESS", "data": plaintext_data}

    except InvalidTag:
        # Kesalahan utama AEAD: data diubah atau password salah
        return {"status": "ERROR", "message": "Autentikasi GAGAL! Payload telah diubah atau kunci salah."}
    except Exception as e:
        return {"status": "ERROR", "message": f"Dekripsi GAGAL: {e}"}

def main_chacha20():
    print("--- Simulasi Pertukaran Data API dengan ChaCha20-Poly1305 ---")
    
    # Data Payload yang akan dikirim
    original_payload = {
        "user_id": 1001,
        "username": "user_rahasia",
        "transaksi": "transfer_dana_1000000"
    }
    
    # Gunakan password yang sama untuk simulasi kunci simetris
    api_secret = "ini_kunci_rahasia_api_2024"
    
    print("\n[CLIENT] Data Original (JSON Payload):")
    print(json.dumps(original_payload, indent=4))
    
    # --- PROSES ENKRIPSI (SISI KLIEN) ---
    print("\n[CLIENT] Memulai Enkripsi...")
    encrypted_data = encrypt_api_payload(original_payload, api_secret)
    
    print("\n[CLIENT] Data Terenkripsi (Siap Dikirim via API):")
    print(json.dumps(encrypted_data, indent=4))
    
    # --- PROSES DEKRIPSI (SISI SERVER) ---
    print("\n" + "="*50)
    print("[SERVER] Menerima dan Memulai Dekripsi...")
    
    decryption_result = decrypt_api_payload(encrypted_data, api_secret)
    
    if decryption_result["status"] == "SUCCESS":
        print("\n[SERVER] Dekripsi Berhasil dan Integritas Terverifikasi!")
        print("Data yang Diproses:")
        print(json.dumps(decryption_result['data'], indent=4))
    else:
        print("\n[SERVER] Dekripsi GAGAL!")
        print(f"Pesan: {decryption_result['message']}")
    
    # ------------------------------------
    # --- Uji Skenario Integritas (Tampering) ---
    # ------------------------------------
    print("\n" + "="*50)
    print("[UJI TAMPERING] Mengubah sedikit data terenkripsi sebelum dekripsi...")
    tampered_data = encrypted_data.copy()
    # Ubah 1 karakter pada bagian 'data' (Ciphertext + Tag)
    # Ini akan menyebabkan InvalidTag saat dekripsi, membuktikan integritas berfungsi
    tampered_data['data'] = tampered_data['data'].replace('A', 'Z', 1) 
    
    tamper_result = decrypt_api_payload(tampered_data, api_secret)
    
    if tamper_result["status"] == "SUCCESS":
        print("\n[SERVER] Deteksi Tampering GAGAL (INI SANGAT TIDAK AMAN!)")
    else:
        print("\n[SERVER] Deteksi Tampering BERHASIL. Integritas GAGAL diverifikasi!")
        print(f"Pesan: {tamper_result['message']}")

if __name__ == "__main__":
    main_chacha20()
    
