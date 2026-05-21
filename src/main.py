import sys
import os
from PyQt6.QtWidgets import QApplication, QMessageBox
from src.infrastructure.database import DatabaseManager
from src.ui.controllers.auth_controller import AuthController
from src.ui.views.login_view import LoginView
from src.ui.views.main_view import MainView
from src.ui.controllers.vault_controller import VaultController
from src.core.inactivity_filter import InactivityFilter

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("MenagoHasel")
    app.setDesktopFileName("menagohasel")
    
    TIMEOUT_MS = 300000 
    inactivity_filter = InactivityFilter(TIMEOUT_MS)
    app.installEventFilter(inactivity_filter)
    
    db = None
    auth_controller = None
    
    login_window = LoginView()
    main_window = None 
    
    def on_login_success(active_db, active_auth):
        nonlocal main_window
        main_window = MainView()
        vault_controller = VaultController(active_db, active_auth.active_dek)
        
        def refresh_table():
            records = vault_controller.get_all_decrypted_records()
            main_window.populate_table(records)

        def on_add_requested():
            if vault_controller.handle_add_record(main_window):
                refresh_table() 

        def on_copy_requested(record_id):
            title = vault_controller.handle_copy_password(record_id)
            if title:
                QMessageBox.information(main_window, "Copied", f"Password for '{title}' copied to clipboard!")

        def on_delete_requested(record_id):
            vault_controller.delete_vault_record(record_id)
            refresh_table()

        def on_edit_requested(record_id):
            if vault_controller.handle_edit_record(main_window, record_id):
                refresh_table()

        main_window.logout_requested.connect(on_logout)
        main_window.add_requested.connect(on_add_requested)
        main_window.copy_requested.connect(on_copy_requested)
        main_window.delete_requested.connect(on_delete_requested)
        main_window.edit_requested.connect(on_edit_requested)
        
        refresh_table()
        login_window.close()
        main_window.show()

    def on_logout():
        nonlocal main_window, db, auth_controller
        
        if auth_controller is None or auth_controller.active_dek is None:
            return
            
        auth_controller.active_dek = None 
        auth_controller = None
        
        if db:
            db.close()
            db = None
        
        if main_window:
            main_window.close()
            main_window = None 
            
        login_window.clear_fields()
        login_window.show()

    def on_login_attempt(username: str, password: str):
        nonlocal db, auth_controller
        safe_username = "".join(c for c in username if c.isalnum() or c in ("-", "_")).lower()
        profiles_dir = "profiles"
        
        if not os.path.exists(profiles_dir):
            os.makedirs(profiles_dir)
            
        db_path = os.path.join(profiles_dir, f"{safe_username}.db")
        
        if not os.path.exists(db_path):
            login_window.show_error("Profile does not exist. Please register first.")
            return

        db = DatabaseManager(db_path)
        db.initialize_schema()
        auth_controller = AuthController(db)
        success, message = auth_controller.handle_login_attempt(password)
        
        if success:
            on_login_success(db, auth_controller)
        else:
            db.close()
            db = None
            auth_controller = None
            login_window.show_error(message)

    def on_register_attempt(username: str, password: str):
        nonlocal db, auth_controller
        safe_username = "".join(c for c in username if c.isalnum() or c in ("-", "_")).lower()
        profiles_dir = "profiles"
        
        if not os.path.exists(profiles_dir):
            os.makedirs(profiles_dir)
            
        db_path = os.path.join(profiles_dir, f"{safe_username}.db")
        
        if os.path.exists(db_path):
            login_window.show_error("Profile already exists. Please log in.")
            return
            
        db = DatabaseManager(db_path)
        db.initialize_schema()
        auth_controller = AuthController(db)
        
        success, message = auth_controller.handle_login_attempt(password)
        if success:
            login_window.show_success("Profile created successfully! You can now log in.")
            login_window.clear_fields()
        
        db.close()
        db = None
        auth_controller = None

    inactivity_filter.timeout_reached.connect(on_logout)
    login_window.login_attempted.connect(on_login_attempt)
    login_window.register_attempted.connect(on_register_attempt)
    login_window.show()
    
    exit_code = app.exec()
    
    if db:
        db.close()
        
    sys.exit(exit_code)

if __name__ == "__main__":
    main()