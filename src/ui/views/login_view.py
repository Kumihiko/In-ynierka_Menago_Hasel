from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QHBoxLayout
from PyQt6.QtCore import pyqtSignal

class LoginView(QWidget):
    login_attempted = pyqtSignal(str, str)
    register_attempted = pyqtSignal(str, str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("MenagoHasel - Login")
        self.setFixedSize(300, 240)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout()

        layout.addWidget(QLabel("User Profile / Login:"))
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("e.g., bartosz, mama")
        layout.addWidget(self.username_input)

        layout.addWidget(QLabel("Master Password:"))
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setPlaceholderText("Enter master password")
        layout.addWidget(self.password_input)

        btn_layout = QHBoxLayout()
        self.login_btn = QPushButton("Unlock Vault")
        self.login_btn.clicked.connect(self._on_login_clicked)
        
        self.register_btn = QPushButton("Create Profile")
        self.register_btn.clicked.connect(self._on_register_clicked)
        
        btn_layout.addWidget(self.login_btn)
        btn_layout.addWidget(self.register_btn)
        
        layout.addLayout(btn_layout)
        self.setLayout(layout)

    def _on_login_clicked(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not username or not password:
            self.show_error("Both fields are required!")
            return

        self.login_attempted.emit(username, password)

    def _on_register_clicked(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not username or not password:
            self.show_error("Both fields are required to register!")
            return

        self.register_attempted.emit(username, password)

    def clear_fields(self):
        self.username_input.clear()
        self.password_input.clear()

    def show_error(self, message: str):
        QMessageBox.critical(self, "Error", message)
        
    def show_success(self, message: str):
        QMessageBox.information(self, "Success", message)