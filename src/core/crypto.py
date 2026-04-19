import os
from argon2.low_level import hash_secret_raw, Type
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


TIME_COST = 2
MEMORY_COST = 65536
PARALLELISM = 2
HASH_LEN = 32

def generate_salt() -> bytes:
    return os.urandom(32)

def derive_kek(password: str, salt: bytes) -> bytes:
    if not password:
        raise ValueError("Haslo nie moze byc puste")
    
    return hash_secret_raw(
        secret=password.encode('utf-8'),
        salt=salt,
        time_cost=TIME_COST,
        memory_cost=MEMORY_COST,
        parallelism=PARALLELISM,
        hash_len=HASH_LEN,
        type=Type.ID
    )
    
def generate_dek() -> bytes:
    return AESGCM.generate_key(bit_length=256)

def encrypt_data(key: bytes, plaintext: bytes) -> tuple[bytes, bytes]:
    aesgcm = AESGCM(key)
    iv = os.urandom(12)
    ciphertext = aesgcm.encrypt(nonce=iv, data=plaintext, associated_data=None)
    return iv, ciphertext

def decrypt_data(key: bytes, iv: bytes, ciphertext: bytes) -> bytes:
    aesgcm = AESGCM(key)
    return aesgcm.decrypt(nonce=iv, data=ciphertext, associated_data=None)