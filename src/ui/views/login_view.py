from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QHBoxLayout, QApplication
from PyQt6.QtCore import pyqtSignal
from src.ui.styles.accessibility import HIGH_CONTRAST_STYLESHEET

class LoginView(QWidget):
    login_attempted = pyqtSignal(str, str)
    register_attempted = pyqtSignal(str, str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("MenagoHasel - Login")
        self.setFixedSize(300, 280)
        self.is_high_contrast = False
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout()
        
        self.accessibility_btn = QPushButton("Wysoki kontrast")
        self.accessibility_btn.clicked.connect(self._toggle_accessibility)
        layout.addWidget(self.accessibility_btn)

        layout.addWidget(QLabel("Nazwa użytkownika:"))
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("e.g., Bartek, Karol, etc.")
        layout.addWidget(self.username_input)

        layout.addWidget(QLabel("Master Password:"))
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setPlaceholderText("Wpisz haslo")
        layout.addWidget(self.password_input)

        btn_layout = QHBoxLayout()
        self.login_btn = QPushButton("Zaloguj")
        self.login_btn.clicked.connect(self._on_login_clicked)
        
        self.register_btn = QPushButton("Stwórz konto")
        self.register_btn.clicked.connect(self._on_register_clicked)
        
        btn_layout.addWidget(self.login_btn)
        btn_layout.addWidget(self.register_btn)
        
        layout.addLayout(btn_layout)
        self.setLayout(layout)

    def _on_login_clicked(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not username or not password:
            self.show_error("Oba pola wymagane")
            return

        self.login_attempted.emit(username, password)

    def _on_register_clicked(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not username or not password:
            self.show_error("Oba pola wymagane")
            return

        self.register_attempted.emit(username, password)

    def clear_fields(self):
        self.username_input.clear()
        self.password_input.clear()

    def show_error(self, message: str):
        QMessageBox.critical(self, "Error", message)
        
    def show_success(self, message: str):
        QMessageBox.information(self, "Success", message)
        
    def _toggle_accessibility(self):
        self.is_high_contrast = not self.is_high_contrast
        app = QApplication.instance()
        
        if self.is_high_contrast:
            app.setStyleSheet(HIGH_CONTRAST_STYLESHEET)
        else:
            app.setStyleSheet("")