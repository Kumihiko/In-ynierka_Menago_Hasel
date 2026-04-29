from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, 
                             QLabel, QLineEdit, QPushButton, QMessageBox)

class AddRecordDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Dodaj nowy wpis")
        self.setFixedSize(300, 200)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout()

        # Pola formularza
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("np. Konto w banku, Facebook")
        layout.addWidget(QLabel("Tytuł:"))
        layout.addWidget(self.title_input)

        self.login_input = QLineEdit()
        self.login_input.setPlaceholderText("Login lub e-mail")
        layout.addWidget(QLabel("Login:"))
        layout.addWidget(self.login_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Tajne hasło")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(QLabel("Hasło:"))
        layout.addWidget(self.password_input)

        # Przyciski
        btn_layout = QHBoxLayout()
        self.save_btn = QPushButton("Zapisz")
        self.save_btn.clicked.connect(self.accept) 
        
        self.cancel_btn = QPushButton("Anuluj")
        self.cancel_btn.clicked.connect(self.reject) 

        btn_layout.addWidget(self.save_btn)
        btn_layout.addWidget(self.cancel_btn)
        
        layout.addLayout(btn_layout)
        self.setLayout(layout)

    def get_data(self) -> dict | None:
        title = self.title_input.text().strip()
        login = self.login_input.text().strip()
        password = self.password_input.text().strip()

        if not title or not password:
            QMessageBox.warning(self, "Błąd", "Pola 'Tytuł' i 'Hasło' są wymagane!")
            return None

        return {
            "title": title,
            "login": login,
            "password": password
        }