import hashlib
from Cryptodome.Cipher import AES
from Cryptodome.Util import Padding

class Protocol:
    def __init__(self):
        pass

    # Encrypting messages
    def EncryptAndProtectMessage(self, plain_text, R, secret):
        h = hashlib.sha3_256()
        h.update(bytes(secret,encoding='utf-8'))
        key = h.digest()

        cipher = AES.new(key, AES.MODE_EAX, nonce=R)
        cipher_text, tag = cipher.encrypt_and_digest(Padding.pad(plain_text,16))
        encrypted = cipher_text + tag
        return encrypted

    # Decrypting and verifying messages
    def DecryptAndVerifyMessage(self, cipher_text, R, secret):
        h = hashlib.sha3_256()
        h.update(bytes(secret,encoding='utf-8'))
        key = h.digest()

        try:
            cipher = AES.new(key, AES.MODE_EAX, nonce=R)
            tag = cipher_text[-16:]
            withoutTag = cipher_text[:-16]
            plaintext = Padding.unpad(cipher.decrypt_and_verify(withoutTag, tag),16)
            print("File Verified")
            return plaintext
        except ValueError:
            print("File Integrity Error")
        pass