import json
from PyQt6.QtWidgets import QDialog, QApplication
from src.infrastructure.database import DatabaseManager
from src.core.crypto import encrypt_data, decrypt_data
from src.ui.views.add_record_dialog import AddRecordDialog

class VaultController:
    def __init__(self, db: DatabaseManager, active_dek: bytes):
        self.db = db
        self.active_dek = active_dek
        self._cached_records = []

    def get_all_decrypted_records(self) -> list[dict]:
        records = self.db.get_all_records()
        self._cached_records.clear()
        
        for row in records:
            try:
                decrypted_bytes = decrypt_data(self.active_dek, row['record_iv'], row['encrypted_password'])
                payload = json.loads(decrypted_bytes.decode('utf-8'))
                
                self._cached_records.append({
                    "id": row['id'],
                    "title": row['title'],
                    "login": payload["login"],
                    "password": payload["password"]
                })
            except Exception as e:
                print(f"Błąd integralności rekordu ID {row['id']}: {e}")
                
        return self._cached_records

    def handle_add_record(self, parent_window) -> bool:
        dialog = AddRecordDialog(parent_window)
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_data()
            if data:
                payload = json.dumps({
                    "login": data["login"],
                    "password": data["password"]
                }).encode('utf-8')
                
                iv, encrypted_payload = encrypt_data(self.active_dek, payload)
                
                self.db.add_record(
                    title=data["title"],
                    encrypted_password=encrypted_payload,
                    record_iv=iv
                )
                return True
        return False

    def handle_copy_password(self, record_id: int) -> str | None:
        for record in self._cached_records:
            if record["id"] == record_id:
                clipboard = QApplication.clipboard()
                clipboard.setText(record["password"])
                return record["title"]
        return None