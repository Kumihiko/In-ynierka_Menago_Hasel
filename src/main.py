import sys
from PyQt6.QtWidgets import QApplication, QMessageBox  # Dodany import QMessageBox
from src.infrastructure.database import DatabaseManager
from src.ui.controllers.auth_controller import AuthController
from src.ui.views.login_view import LoginView
from src.ui.views.main_view import MainView
from src.ui.controllers.vault_controller import VaultController

def main():
    app = QApplication(sys.argv)
    
    # 1. Inicjalizacja warstwy infrastruktury
    db = DatabaseManager("vault.db")
    db.initialize_schema()
    
    # 2. Inicjalizacja kontrolera autoryzacji
    auth_controller = AuthController(db)
    
    # 3. Referencje do okien (aby nie usunął ich Garbage Collector)
    login_window = LoginView()
    main_window = None 
    
    # --- LOGIKA PRZEŁĄCZANIA OKIEN ---
    
    def on_login_success(): # Naprawione wcięcie
        nonlocal main_window
        main_window = MainView()
        
        # Tworzymy Kontroler Sejfu przekazując mu odszyfrowany klucz z RAM
        vault_controller = VaultController(db, auth_controller.active_dek)
        
        def refresh_table():
            records = vault_controller.get_all_decrypted_records()
            main_window.populate_table(records)

        def on_add_requested():
            if vault_controller.handle_add_record(main_window):
                refresh_table() # Jeśli zapis się udał, odświeżamy tabelę nowymi danymi

        def on_copy_requested(record_id):
            title = vault_controller.handle_copy_password(record_id)
            if title:
                QMessageBox.information(main_window, "Skopiowano", f"Hasło dla '{title}' skopiowano do schowka!")

        def on_delete_requested(record_id):
            # Kontroler usuwa z bazy
            vault_controller.delete_vault_record(record_id)
            # Automatyczne przeładowanie widoku
            refresh_table()

        def on_edit_requested(record_id):
            if vault_controller.handle_edit_record(main_window, record_id):
                refresh_table()

            
            
        # Podpinamy prawdziwe funkcje pod sygnały okna
        main_window.logout_requested.connect(on_logout)
        main_window.add_requested.connect(on_add_requested)
        main_window.copy_requested.connect(on_copy_requested)
        main_window.delete_requested.connect(on_delete_requested)
        main_window.edit_requested.connect(on_edit_requested)
        
        # Pobieramy prawdziwe zaszyfrowane hasła z bazy na start
        refresh_table()
        
        login_window.close()
        main_window.show()

    def on_logout():
        nonlocal main_window
        auth_controller.active_dek = None 
        main_window.close()
        login_window.show()

    def on_login_attempt(password: str):
        success, message = auth_controller.handle_login_attempt(password)
        
        if success:
            on_login_success()
        else:
            login_window.show_error(message)

    # --- START APLIKACJI ---
    
    login_window.login_attempted.connect(on_login_attempt)
    login_window.show()
    
    exit_code = app.exec()
    
    # Bezpieczne zamknięcie bazy po wyjściu z aplikacji
    db.close()
    sys.exit(exit_code)

if __name__ == "__main__":
    main()