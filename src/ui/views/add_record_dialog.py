from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, 
                             QLabel, QLineEdit, QPushButton, QMessageBox)
from src.core.password_policy import PasswordPolicyManager

class AddRecordDialog(QDialog):
    # Wstrzykujemy manager polityki haseł do konstruktora
    def __init__(self, policy_manager: PasswordPolicyManager, parent=None, current_title="", current_login=""):
        super().__init__(parent)
        self.policy_manager = policy_manager
        
        self.setWindowTitle("Edytuj wpis" if current_title else "Dodaj nowy wpis")
        self.setFixedSize(350, 220) # Lekko poszerzone dla nowego przycisku
        self._setup_ui()
        
        if current_title:
            self.title_input.setText(current_title)
        if current_login:
            self.login_input.setText(current_login)

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

        # Pole hasła wraz z przyciskiem generatora w jednym rzędzie
        pass_layout = QHBoxLayout()
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Tajne hasło")
        # Wyłączamy kropki, żeby użytkownik widział wygenerowane słowa
        self.password_input.setEchoMode(QLineEdit.EchoMode.Normal) 
        
        self.generate_btn = QPushButton("Generuj")
        self.generate_btn.clicked.connect(self._on_generate_clicked)
        
        pass_layout.addWidget(self.password_input)
        pass_layout.addWidget(self.generate_btn)
        
        layout.addWidget(QLabel("Hasło:"))
        layout.addLayout(pass_layout)

        # Przyciski dolne
        btn_layout = QHBoxLayout()
        self.save_btn = QPushButton("Zapisz")
        self.save_btn.clicked.connect(self.accept) 
        
        self.cancel_btn = QPushButton("Anuluj")
        self.cancel_btn.clicked.connect(self.reject) 

        btn_layout.addWidget(self.save_btn)
        btn_layout.addWidget(self.cancel_btn)
        
        layout.addLayout(btn_layout)
        self.setLayout(layout)
        
    def _on_generate_clicked(self):
        try:
            # Generujemy hasło z 5 słów
            new_password = self.policy_manager.generate_diceware_password(num_words=5)
            self.password_input.setText(new_password)
        except Exception as e:
            QMessageBox.critical(self, "Błąd Generatora", str(e))

    def get_data(self) -> dict | None:
        title = self.title_input.text().strip()
        login = self.login_input.text().strip()
        password = self.password_input.text().strip()

        if not title or not password:
            QMessageBox.warning(self, "Błąd", "Pola 'Tytuł' i 'Hasło' są wymagane!")
            return None

        # Walidacja hasła przed zwróceniem danych
        is_valid, message = self.policy_manager.validate_password(password)
        if not is_valid:
            QMessageBox.warning(self, "Słabe hasło", message)
            return None

        return {
            "title": title,
            "login": login,
            "password": password
        }