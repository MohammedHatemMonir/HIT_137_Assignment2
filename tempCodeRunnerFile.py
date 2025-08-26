shift1 = int(input("Enter shift1: "))
shift2 = int(input("Enter shift2: "))

def rotate_letter(ch, k):
    if 'a' <= ch <= 'z':
        base = ord('a'); pos = ord(ch) - base
        return chr(base + ((pos + k) % 26))
    elif 'A' <= ch <= 'Z':
        base = ord('A'); pos = ord(ch) - base
        return chr(base + ((pos + k) % 26))
    else:
        return ch

def encrypt_char(ch, s1, s2):
    if 'a' <= ch <= 'z':
        if 'a' <= ch <= 'm':
            return rotate_letter(ch, s1 * s2)
        else:
            return rotate_letter(ch, -(s1 + s2))
    elif 'A' <= ch <= 'Z':
        if 'A' <= ch <= 'M':
            return rotate_letter(ch, -s1)
        else:
            return rotate_letter(ch, s2 * s2)
    else:
        return ch

def decrypt_char(ch, s1, s2):
    if 'a' <= ch <= 'z':
        a = rotate_letter(ch, -(s1 * s2))
        b = rotate_letter(ch,  (s1 + s2))
        return a if encrypt_char(a, s1, s2) == ch else b
    elif 'A' <= ch <= 'Z':
        a = rotate_letter(ch,  s1)
        b = rotate_letter(ch, -(s2 * s2))
        return a if encrypt_char(a, s1, s2) == ch else b
    else:
        return ch
    
def encrypt_file():
    f = open("raw_text.txt", "r")
    raw_text = f.read()
    f.close()
    encrypted = ""
    for ch in raw_text:
        encrypted += encrypt_char(ch, shift1, shift2)
    g = open("encrypted_text.txt", "w")
    g.write(encrypted)
    g.close()

def decrypt_file():
    h = open("encrypted_text.txt", "r")
    cipher = h.read()
    h.close()
    decrypted = ""
    for ch in cipher:
        decrypted += decrypt_char(ch, shift1, shift2)
    k = open("decrypted_text.txt", "w")
    k.write(decrypted)
    k.close()

def verify_files():
    f = open("raw_text.txt", "r")
    raw_text = f.read()
    f.close()
    k = open("decrypted_text.txt", "r")
    decrypted = k.read()
    k.close()
    if decrypted == raw_text:
        print("Verification: SUCCESS")
    else:
        print("Verification: FAILED")

encrypt_file()
decrypt_file()
verify_files()
