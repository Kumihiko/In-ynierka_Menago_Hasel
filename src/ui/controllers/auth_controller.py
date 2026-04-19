from cryptography.exceptions import InvalidTag
from src.core.memory import SecureString
from src.core.crypto import generate_salt, derive_kek, generate_dek, encrypt_data, decrypt_data
from src.infrastructure.database import DatabaseManager

class AuthController:
    def __init__(self, db: DatabaseManager):
        self.db = db
        self.active_dek: bytes | None = None  

    def handle_login_attempt(self, password_str: str) -> tuple[bool, str]:
        secure_password = SecureString(password_str)
        
        try:
            salt = self.db.get_config("salt")
            
            if salt is None:
                return self._initialize_new_vault(secure_password)
            else:
                return self._unlock_vault(secure_password, salt)
        finally:
            secure_password.destroy()

    def _initialize_new_vault(self, secure_password: SecureString) -> tuple[bool, str]:
        salt = generate_salt()
        password_text = secure_password.get_bytes().decode('utf-8')
        kek = derive_kek(password_text, salt)
        dek = generate_dek()
        
        kek_iv, encrypted_dek = encrypt_data(kek, dek)
        
        self.db.save_config("salt", salt)
        self.db.save_config("kek_iv", kek_iv)
        self.db.save_config("encrypted_dek", encrypted_dek)
        
        self.active_dek = dek
        return True, "Sejf został pomyślnie utworzony i odblokowany"

    def _unlock_vault(self, secure_password: SecureString, salt: bytes) -> tuple[bool, str]:
        password_text = secure_password.get_bytes().decode('utf-8')
        kek = derive_kek(password_text, salt)
        
        kek_iv = self.db.get_config("kek_iv")
        encrypted_dek = self.db.get_config("encrypted_dek")
        
        try:
            dek = decrypt_data(kek, kek_iv, encrypted_dek)
            self.active_dek = dek
            return True, "Zalogowano pomyślnie"
        except InvalidTag:
            return False, "Błędne Master Password"