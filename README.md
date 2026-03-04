RC4 — Rivest Cipher 4
Implementasi Stream Cipher dalam Python
==================================================================================
Pengantar Singkat
RC4 (Rivest Cipher 4) adalah algoritma kriptografi jenis stream cipher yang dirancang oleh Ron Rivest dari RSA Security pada tahun 1987. Selama lebih dari dua dekade, RC4 menjadi salah satu algoritma enkripsi paling banyak digunakan di dunia karena kesederhanaan implementasinya dan kecepatannya dalam memproses data.
Kegunaan Utama di Dunia Nyata
Teknologi	Keterangan
---------------------------------------------------------------------------------------------------------------------------------------------
SSL/TLS	Digunakan untuk mengenkripsi komunikasi HTTPS antara browser dan server web (1990–2015)
---------------------------------------------------------------------------------------------------------------------------------------------
WEP & WPA-TKIP	Menjadi inti enkripsi standar keamanan Wi-Fi pada router rumahan dan perkantoran
---------------------------------------------------------------------------------------------------------------------------------------------
Microsoft Office	Dipakai untuk enkripsi dokumen yang dilindungi password (versi sebelum Office 2007)
---------------------------------------------------------------------------------------------------------------------------------------------
Adobe PDF	Mengenkripsi file PDF yang menggunakan proteksi password
---------------------------------------------------------------------------------------------------------------------------------------------
Microsoft RDP	Mengamankan sesi remote desktop antara komputer klien dan server
---------------------------------------------------------------------------------------------------------------------------------------------
Komunikasi GSM	Digunakan pada beberapa implementasi protokol jaringan seluler generasi awal
==================================================================================
Pembangkitan Kunci (Key Generation)
RC4 tidak membangkitkan kunci baru — ia menggunakan kunci yang diberikan langsung oleh pengguna untuk menginisialisasi state internal melalui proses yang disebut KSA (Key Scheduling Algorithm).
Cara Kerja KSA
Input: Kunci berupa string teks (dikonversi ke bytes)
Output: Array permutasi S berisi 256 elemen (0–255) yang sudah teracak
1. Buat array S = [0, 1, 2, ..., 255]
2. Set j = 0
3. Untuk setiap i dari 0 hingga 255:
       j = (j + S[i] + key[i mod panjang_kunci]) mod 256
       Tukar S[i] dengan S[j]
4. Kembalikan array S
def ksa(key_bytes):
    S = list(range(256))   # Inisialisasi S = [0..255]
    j = 0
    for i in range(256):
        j = (j + S[i] + key_bytes[i % len(key_bytes)]) & 0xFF
        S[i], S[j] = S[j], S[i]   # Tukar posisi
    return S
Distribusi Kunci
RC4 menggunakan skema kunci simetris — kunci yang sama digunakan untuk enkripsi dan dekripsi. Artinya:
•	Pengirim dan penerima harus berbagi kunci yang sama sebelum komunikasi dimulai.
•	Distribusi kunci harus dilakukan melalui jalur yang aman (misalnya dikirim secara terpisah atau melalui protokol pertukaran kunci seperti Diffie-Hellman).
•	Tidak ada mekanisme kunci publik/privat seperti pada RSA — keamanan sepenuhnya bergantung pada kerahasiaan kunci tersebut.
=================================================================================
Proses Enkripsi
Enkripsi RC4 dilakukan dalam dua tahap: pembangkitan keystream menggunakan PRGA, lalu operasi XOR antara keystream dan plaintext.
Tahap 1  PRGA (Pseudo-Random Generation Algorithm)
PRGA menghasilkan aliran byte acak (keystream) dari array S hasil KSA.
1. Set i = 0, j = 0
2. Ulangi untuk setiap byte yang dibutuhkan:
       i = (i + 1) mod 256
       j = (j + S[i]) mod 256
       Tukar S[i] dengan S[j]
       output_byte = S[(S[i] + S[j]) mod 256]
       Hasilkan output_byte sebagai keystream
def prga(S):
    i = j = 0
    while True:
        i = (i + 1) & 0xFF
        j = (j + S[i]) & 0xFF
        S[i], S[j] = S[j], S[i]
        yield S[(S[i] + S[j]) & 0xFF]   # Hasilkan 1 byte keystream
Tahap 2  XOR Plaintext dengan Keystream
def rc4(key: bytes, data: bytes) -> bytes:
    stream = prga(ksa(key))
    return bytes([b ^ next(stream) for b in data])
Setiap byte plaintext di-XOR satu per satu dengan byte keystream:
Plaintext  :  H     a     l     o
(ASCII)    : 0x48  0x61  0x6C  0x6F

Keystream  : 0x3A  0x1F  0x82  0xC3   ← dihasilkan PRGA

XOR (^)    : 0x72  0x7E  0xEE  0xAC

Ciphertext : 727eeeac  (dalam format hex)
=================================================================================
Proses Dekripsi
Dekripsi RC4 identik dengan enkripsi. Tidak ada fungsi terpisah, cukup jalankan rc4() yang sama dengan kunci yang sama pada ciphertext.
Mengapa Bisa Sama?
Karena sifat matematis XOR yang simetris:
Enkripsi : Plaintext  XOR Keystream = Ciphertext
Dekripsi : Ciphertext XOR Keystream = Plaintext
===========================================================
Kelebihan & Kelemahan
Kelebihan
Aspek	Penjelasan
Kecepatan	Sangat cepat dalam enkripsi/dekripsi, cocok untuk perangkat dengan sumber daya terbatas
Implementasi Sederhana	Hanya butuh ~30 baris kode, mudah diimplementasikan di berbagai bahasa pemrograman
Ringan	Tidak membutuhkan banyak memori — hanya array 256 byte untuk state internal
Fleksibel	Dapat mengenkripsi data dengan panjang berapa pun tanpa perlu padding
Simetris	Satu fungsi untuk enkripsi dan dekripsi, menyederhanakan implementasi
Kelemahan
Aspek	Penjelasan
RC4 Biases	Byte-byte awal keystream memiliki distribusi statistik yang tidak merata, membuat pola dapat dideteksi
Rentan Serangan	Kelemahan ini dieksploitasi dalam serangan BEAST dan CRIME yang menarget SSL/TLS
WEP Mudah Dibobol	Implementasi RC4 dalam WEP dapat dipecahkan dalam hitungan menit menggunakan tools seperti Aircrack-ng
Tidak Ada Integritas Data	RC4 murni tidak memverifikasi apakah data telah dimodifikasi selama transmisi (no MAC)
Kunci Simetris	Distribusi kunci menjadi tantangan — jika kunci bocor, semua enkripsi gugur seketika
Sudah Dilarang (RFC 7465)	Sejak 2015 resmi dilarang digunakan dalam TLS/SSL oleh standar internasional
