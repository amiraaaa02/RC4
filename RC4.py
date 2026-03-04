def ksa(key_bytes):
    S = list(range(256))
    j = 0
    for i in range(256):
        j = (j + S[i] + key_bytes[i % len(key_bytes)]) & 0xFF
        S[i], S[j] = S[j], S[i]
    return S

def prga(S):
    i = j = 0
    while True:
        i = (i + 1) & 0xFF
        j = (j + S[i]) & 0xFF
        S[i], S[j] = S[j], S[i]
        yield S[(S[i] + S[j]) & 0xFF]

def rc4(key: bytes, data: bytes) -> bytes:
    stream = prga(ksa(key))
    return bytes([b ^ next(stream) for b in data])

def input_key():
    while True:
        key = input("Kunci      : ")
        if key:
            return key
        print("Kunci tidak boleh kosong!")

def enkripsi():
    key = input_key()
    while True:
        plaintext = input("Plaintext  : ")
        if plaintext:
            break
        print("Plaintext tidak boleh kosong!")
    
    ct = rc4(key.encode(), plaintext.encode())
    print(f"Ciphertext : {ct.hex()}\n")

def dekripsi():
    key = input_key()
    while True:
        ciphertext = input("Ciphertext : ")
        if not ciphertext:
            print("Ciphertext tidak boleh kosong!")
            continue
        try:
            bytes.fromhex(ciphertext)
            break
        except ValueError:
            print("Format ciphertext tidak valid!")

    pt = rc4(key.encode(), bytes.fromhex(ciphertext))
    print(f"Plaintext  : {pt.decode('utf-8', errors='replace')}\n")

def main():
    menu = {"1": enkripsi, "2": dekripsi}
    while True:
        print("1. Enkripsi\n2. Dekripsi\n3. Keluar")
        pilihan = input("Pilih: ").strip()
        if pilihan == "3":
            break
        elif pilihan in menu:
            menu[pilihan]()
        else:
            print("Pilihan tidak valid\n")

if __name__ == "__main__":
    main()