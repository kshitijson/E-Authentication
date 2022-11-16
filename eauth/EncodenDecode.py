from cryptography.fernet import Fernet

class Encrypt:
    def __init__(self, string):
        self.string = string

    def encrypt_text(self):
        key = Fernet.generate_key()
        fernet = Fernet(key)
        encmsg = fernet.encrypt(self.string.encode())
        return encmsg


class Decrypt:
    def __init__(self, enc_string):
        self.enc_string = enc_string
    
    def decrypt_text(self):
        key = Fernet.generate_key()
        fernet = Fernet(key)
        decmsg = fernet.decrypt(self.enc_string)
        return decmsg


#i = Encrypt('D:/QR')
#j = i.encrypt_text()
#print(j)

c = "b'gAAAAABibo6p6h1w6rCjyBlLCENodYyM_pC_wuCsuBnaj43CmtehCtdcFnV_rn4izZ_-kolBtNMNxQFFXqutGe6ywSXyCGzOBA=='"
f = Decrypt(c)
print(f.decrypt_text())