# 🔐 AES-GCM Folder Encryptor (Python)

Aplikasi Python untuk **mengenkripsi dan mendekripsi seluruh file dalam satu folder** menggunakan algoritma **AES-GCM (Authenticated Encryption)**.  
Proyek ini dirancang untuk latihan penerapan **AES mode modern (GCM)** serta sistem **batch encryption** pada banyak file sekaligus.

---

## 📂 Fitur Utama

✅ Mengenkripsi semua file dalam satu folder dengan **AES-GCM**  
✅ Menghasilkan folder baru berisi file terenkripsi (`.enc`)  
✅ Menyediakan fungsi dekripsi seluruh folder kembali ke bentuk semula  
✅ Menjamin integritas data melalui **Authentication Tag (GCM Tag)**  
✅ Menggunakan **satu password utama** untuk seluruh file  
✅ Menyimpan data dengan struktur byte aman (salt, nonce, tag, ciphertext)  
✅ Aman dari modifikasi file dan serangan brute-force  

---

## ⚙️ Teknologi & Modul yang Digunakan

- Python 3.8+
- [PyCryptodome](https://pypi.org/project/pycryptodome/)
- AES-256 (GCM mode)
- PBKDF2 (Password-Based Key Derivation Function 2)

---

## 📁 Struktur Folder

📦 aes-gcm-folder-encryptor

┣ 📂 input_folder/ # Folder sumber berisi file asli

┣ 📂 data_terenkripsi/ # Folder hasil enkripsi (.enc)

┣ 📂 data_hasil_dekripsi/ # Folder hasil dekripsi

┣ 📜 encryptor.py # Script utama

┗ 📜 README.md # Dokumentasi proyek


## 🚀 Cara Penggunaan

### 1️⃣ Instalasi
Pastikan Python dan PyCryptodome sudah terpasang:

      pip install pycryptodome


### 2️⃣ Menjalankan Program
      python encryptor.py

Anda akan diminta untuk:

Memasukkan password utama
Memilih mode:

1 = Enkripsi Folder

2 = Dekripsi Folder

### 3️⃣ Enkripsi

Semua file dalam input_folder/ akan dienkripsi ke data_terenkripsi/

Setiap file akan mendapatkan ekstensi .enc

Contoh hasil:

            input_folder/Proposal.pdf
            → data_terenkripsi/Proposal.pdf.enc

### 4️⃣ Dekripsi

Semua file ` .enc ` di ` data_terenkripsi/ ` akan didekripsi ke ` data_hasil_dekripsi/ `

File hasil dekripsi akan sama persis dengan file aslinya.



## 🔒 Keamanan

- Menggunakan AES-256 GCM, algoritma yang aman dan modern.

- Authentication Tag (GCM Tag) menjamin integritas dan keaslian data.

- Password diubah menjadi kunci kriptografi 256-bit melalui PBKDF2 dengan 100.000 iterasi dan salt acak.

- Password tidak disimpan di mana pun — diminta langsung saat runtime melalui getpass() (tidak terlihat di layar).

.

## 🧪 Contoh Output

            Masukkan password utama: ********
            --- Pilihan Mode ---
            1. Enkripsi Folder
            2. Dekripsi Folder
            Masukkan pilihan (1/2, atau 'q' untuk keluar): 1
            ----------------------------------------
            Mode: ENKRIPSI
            Folder Sumber: 'input_folder'
            Folder Tujuan: 'data_terenkripsi'
            ----------------------------------------
              [+] Berhasil mengenkripsi: file1.pdf
              [+] Berhasil mengenkripsi: file2.docx
            ----------------------------------------
            Proses selesai.


## 👨‍💻 Kontributor

Nama: (Achmad Amirul Ahad)

Institusi: ( Universitas Negeri Surabaya)

Tahun: 2023
