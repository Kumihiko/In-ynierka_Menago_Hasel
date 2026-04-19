import pytest
from src.core.memory import SecureString

def test_secure_string_clears_memory():
    secret = "tajnehaslo123"
    secure_str = SecureString(secret)
    
    assert secure_str.get_bytes() == b"tajnehaslo123"
    secure_str.destroy()
    
    assert secure_str.get_bytes() == b"\x00" * len(secret) 