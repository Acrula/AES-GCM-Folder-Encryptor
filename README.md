# AES-GCM-Folder-Encryptor
AES-GCM Folder Encryptor adalah sebuah suite demonstrasi kriptografi yang mengimplementasikan dua standar enkripsi simetris modern yang berbeda, yaitu AES-GCM dan ChaCha20-Poly1305, untuk memenuhi kebutuhan keamanan digital yang berbeda.

## Proyek Kriptografi Modern: Implementasi AES-GCM & ChaCha20
Proyek ini adalah implementasi praktis dari dua skema enkripsi simetris modern yang paling relevan saat ini, berfokus pada Authenticated Encryption with Associated Data (AEAD) untuk menjamin Kerahasiaan, Integritas, dan Otentikasi data.

Aplikasi ini dibagi menjadi dua modul utama:

1. AES-GCM Folder Encryptor: Untuk mengamankan data yang tersimpan (data at rest).
2. ChaCha20-Poly1305 API Security: Untuk mengamankan data yang ditransmisikan (data in transit).

## 🚀 Persiapan dan Instalasi
Pastikan Anda memiliki Python 3.x terinstal.

### 1. Instalasi Pustaka:

      pip install pycryptodome cryptography

### 2. Struktur Proyek:
Pastikan file skrip berada dalam struktur berikut:
     
      .
      ├── aes_folder_encryptor.py     # Modul 1: AES-GCM
      ├── chacha20_api_encryptor.py   # Modul 2: ChaCha20
      └── README.md

## 1. Modul AES-GCM Folder Encryptor
Modul ini adalah alat batch yang kuat untuk mengenkripsi seluruh folder file menggunakan AES-256 dalam mode GCM.

### Fitur Kriptografi Utama
- AES-256 GCM:Standar enkripsi simetris yang paling kuat dengan Authentication Tag untuk verifikasi integritas.

- PBKDF2: Menggunakan 100.000 iterasi PBKDF2-HMAC-SHA256 untuk menderivasi kunci yang sangat aman dari password pengguna.

- Dukungan Fleksibel: Mampu memproses seluruh folder atau file tunggal.

### Cara Menggunakan
Jalankan skrip ` aes_folder_encryptor.py ` dari terminal:

      python aes_folder_encryptor.py

Anda akan diminta untuk memasukkan informasi berikut:



### Hasil & Verifikasi Integritas
File terenkripsi (.enc) menyimpan Salt, Nonce, Authentication Tag, dan Ciphertext.

Jika Anda mencoba mendekripsi dengan password yang salah, atau jika konten file terenkripsi diubah, aplikasi akan secara otomatis mendeteksi kegagalan otentikasi dan menampilkan pesan GAGAL DEKRIPSI/VERIFIKASI TAG.

## 2. Modul ChaCha20-Poly1305 API Security
Modul ini adalah simulasi pertukaran data antara klien dan server, menyoroti penggunaan stream cipher modern, ChaCha20-Poly1305, yang unggul dalam kecepatan dan keamanan untuk data yang bergerak (in transit).

### Konsep Kriptografi
- Algoritma: Menggunakan kombinasi ChaCha20 (untuk kerahasiaan) dan Poly1305 (Message Authentication Code untuk integritas).

- AEAD Penuh: Implementasi ini adalah skema AEAD, menjamin data rahasia dan otentik dalam satu operasi.

- Penggunaan API: Data payload (JSON) dienkripsi, dikodekan dalam Base64 URL-safe, dan siap dikirim sebagai bagian dari permintaan API.

### Cara Menjalankan:
Jalankan skrip ` chacha20_api_encryptor.py ` dari terminal:

      python chacha20_api_encryptor.py

Skrip ini akan berjalan secara otomatis, menampilkan tiga tahap:

1. Enkripsi Sisi Klien: Mengubah payload JSON menjadi format terenkripsi (Base64).

2. Dekripsi Sisi Server: Berhasil mendekripsi dan memulihkan payload asli.

3. Uji Tampering: Mendemonstrasikan bagaimana Poly1305 segera mendeteksi kegagalan otentikasi ketika data terenkripsi diubah (walaupun hanya satu karakter).
