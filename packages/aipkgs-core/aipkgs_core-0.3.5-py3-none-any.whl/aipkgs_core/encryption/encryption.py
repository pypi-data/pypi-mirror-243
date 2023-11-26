import hashlib
import hmac
import os
import uuid


# def encrypt(txt: str, salt: str) -> bytes:
#     # hashlib.sha224(b"Nobody inspects the spammish repetition").hexdigest()
#     key = hashlib.pbkdf2_hmac(
#         'sha256',  # The hash digest algorithm for HMAC
#         txt.encode('utf-8'),  # Convert the password to bytes
#         salt.encode('utf-8'),  # Provide the salt
#         100000  # It is recommended to use at least 100,000 iterations of SHA-256
#     )
#     return key
#
#
# def encrypt_with_new_salt(txt):
#     salt: str = uuid.uuid4().hex
#     return salt, encrypt(txt, salt=salt)
#
#
# def check_key_password(hashed_password: str, txt: str, salt: str):
#     if hmac.compare_digest(encrypt(txt, salt), hashed_password.encode('utf-8')):
#         return True
#     else:
#         return False


def encrypt(txt: str) -> str:
    return hashlib.sha3_256(txt.encode('utf-8')).hexdigest()


def check_hash_password(hash: str, password: str):
    if hmac.compare_digest(encrypt(password), hash):
        return True
    else:
        return False
