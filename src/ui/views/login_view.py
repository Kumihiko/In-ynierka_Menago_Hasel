from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtCore import pyqtSignal

class LoginView(QWidget):
    login_attempted = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Menedżer Haseł - Logowanie")
        self.setFixedSize(300, 150)
        
        self._layout = QVBoxLayout()
        
        self._label = QLabel("Wprowadź Master Password:")
        self._layout.addWidget(self._label)
        
        self._password_input = QLineEdit()
        self._password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self._layout.addWidget(self._password_input)
        
        self._login_button = QPushButton("Odblokuj Sejf")
        self._login_button.clicked.connect(self._on_login_clicked)
        self._layout.addWidget(self._login_button)
        
        self.setLayout(self._layout)

    def _on_login_clicked(self) -> None:
        password = self._password_input.text()
        if not password:
            self.show_error("Hasło nie może być puste!")
            return
            
        self.login_attempted.emit(password)
        self._password_input.clear()

    def show_error(self, message: str) -> None:
        QMessageBox.critical(self, "Błąd", message)