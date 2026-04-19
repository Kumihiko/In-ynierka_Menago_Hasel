import sys
from PyQt6.QtWidgets import QApplication, QMessageBox
from src.infrastructure.database import DatabaseManager
from src.ui.controllers.auth_controller import AuthController
from src.ui.views.login_view import LoginView

def main():
    app = QApplication(sys.argv)
    
    db = DatabaseManager("vault.db")
    db.initialize_schema()
    
    auth_controller = AuthController(db)
    
    login_window = LoginView()
    
    def on_login_attempt(password: str):
        success, message = auth_controller.handle_login_attempt(password)
        
        if success:
            QMessageBox.information(login_window, "Sukces", message)
            print("W RAM znajduje się teraz odszyfrowany klucz DEK gotowy do pracy.")
        else:
            login_window.show_error(message)

    login_window.login_attempted.connect(on_login_attempt)
    
    login_window.show()
    

    exit_code = app.exec()
    
    db.close()
    sys.exit(exit_code)

if __name__ == "__main__":
    main()