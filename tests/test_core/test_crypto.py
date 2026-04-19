import pytest
from src.core.crypto import generate_salt, derive_kek
from cryptography.exceptions import InvalidTag
from src.core.crypto import generate_dek, encrypt_data, decrypt_data

def test_generate_salt():
    salt = generate_salt()
    assert isinstance(salt, bytes)
    assert len(salt) == 32

def test_derive_kek():
    password = "super_silne_haslo"
    salt = generate_salt()
    
    kek1 = derive_kek(password, salt)
    assert isinstance(kek1, bytes)
    assert len(kek1) == 32
    
    kek2 = derive_kek(password, salt)
    assert kek1 == kek2

def test_derive_kek_empty_password():
    salt = generate_salt()
    with pytest.raises(ValueError):
        derive_kek("", salt)
        
def test_generate_dek():
    dek = generate_dek()
    assert isinstance(dek, bytes)
    assert len(dek) == 32
    
def test_encrypt_decrypt_success():
    key = generate_dek()
    plaintext = b"Bardzo tajne dane"
    
    iv, ciphertext = encrypt_data(key, plaintext)
    
    assert len(iv) == 12 
    assert ciphertext != plaintext
    
    decrypted = decrypt_data(key, iv, ciphertext)
    assert decrypted == plaintext
    
def test_decrypt_tampered_data_fails():
    key = generate_dek()
    plaintext = b"Wrazliwe haslo bankowe"
    
    iv, ciphertext = encrypt_data(key, plaintext)
    
    tampered_ciphertext = bytearray(ciphertext)
    tampered_ciphertext[0] ^= 1 
    
    with pytest.raises(InvalidTag):
        decrypt_data(key, iv, bytes(tampered_ciphertext))