def ksa(key_bytes):
    S = list(range(256))        # buat array S berisi 0 sampai 255
    j = 0                       # pointer kedua, mulai dari 0
    for i in range(256):        # loop sebanyak 256x untuk mengacak seluruh array
        j = (j + S[i] + key_bytes[i % len(key_bytes)]) & 0xFF  # hitung posisi j baru, & 0xFF agar tetap 0-255
        S[i], S[j] = S[j], S[i]    # tukar S[i] dan S[j] untuk mengacak array
    return S                    # kembalikan array S yang sudah teracak

def prga(S):
    i = j = 0                           # dua pointer mulai dari 0
    while True:                         # infinite loop karena keystream bisa sepanjang apapun
        i = (i + 1) & 0xFF              # geser i maju 1, balik ke 0 setelah 255
        j = (j + S[i]) & 0xFF           # geser j berdasarkan nilai S[i]
        S[i], S[j] = S[j], S[i]         # tukar untuk terus mengacak array S
        yield S[(S[i] + S[j]) & 0xFF]   # keluarkan 1 byte keystream, pause sampai dipanggil lagi

def rc4(key: bytes, data: bytes) -> bytes:
    stream = prga(ksa(key))                         # acak S pakai key, lalu buat generator keystream
    return bytes([b ^ next(stream) for b in data])  # XOR tiap byte data dengan 1 byte keystream

def input_key():
    while True:
        key = input("Kunci      : ")
        if key:
            return key          # kembalikan key jika tidak kosong
        print("Kunci tidak boleh kosong!")

def enkripsi():
    key = input_key()
    while True:
        plaintext = input("Plaintext  : ")
        if plaintext:
            break
        print("Plaintext tidak boleh kosong!")
    
    ct = rc4(key.encode(), plaintext.encode())  # encode() untuk ubah string ke bytes sebelum diproses
    print(f"Ciphertext : {ct.hex()}\n")         # hex() untuk tampilkan hasil dalam format hexadecimal

def dekripsi():
    key = input_key()
    while True:
        ciphertext = input("Ciphertext : ")
        if not ciphertext:
            print("Ciphertext tidak boleh kosong!")
            continue
        try:
            bytes.fromhex(ciphertext)   # validasi apakah input berupa hex yang valid
            break
        except ValueError:
            print("Format ciphertext tidak valid!")

    pt = rc4(key.encode(), bytes.fromhex(ciphertext))          # fromhex() untuk ubah hex string ke bytes
    print(f"Plaintext  : {pt.decode('utf-8', errors='replace')}\n")  # errors='replace' agar tidak crash jika key salah

def main():
    menu = {"1": enkripsi, "2": dekripsi}   # dictionary untuk mapping pilihan ke fungsi
    while True:
        print("1. Enkripsi\n2. Dekripsi\n3. Keluar")
        pilihan = input("Pilih: ").strip()  # strip() untuk hapus spasi di awal/akhir input
        if pilihan == "3":
            break
        elif pilihan in menu:
            menu[pilihan]()                 # panggil fungsi sesuai pilihan
        else:
            print("Pilihan tidak valid\n")

if __name__ == "__main__":
    main()
