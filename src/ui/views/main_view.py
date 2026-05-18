from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QTableWidget, QTableWidgetItem, 
                             QHeaderView, QLabel, QMessageBox)
from PyQt6.QtCore import pyqtSignal

class MainView(QWidget):

    logout_requested = pyqtSignal()
    add_requested = pyqtSignal()
    copy_requested = pyqtSignal(int)
    delete_requested = pyqtSignal(int)
    edit_requested = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Menedżer Haseł")
        self.resize(600, 400)
        self._setup_ui()

    def _setup_ui(self):
        main_layout = QVBoxLayout()

        # Pasek górny
        top_layout = QHBoxLayout()
        self.info_label = QLabel("")
        self.logout_btn = QPushButton("Zablokuj i Wyloguj")
        self.logout_btn.clicked.connect(self.logout_requested.emit)
        
        top_layout.addWidget(self.info_label)
        top_layout.addStretch()
        top_layout.addWidget(self.logout_btn)
        main_layout.addLayout(top_layout)

        # Tabela danych
        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["Tytuł", "Login", "Hasło"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        main_layout.addWidget(self.table)

        # Pasek dolny
        bottom_layout = QHBoxLayout()
        self.add_btn = QPushButton("Dodaj nowe hasło")
        self.add_btn.clicked.connect(self.add_requested.emit)
        
        self.btn_edit = QPushButton("Edytuj wybrane hasło")
        self.btn_delete = QPushButton("Usuń wybrane hasło")
        
        self.btn_delete.clicked.connect(self._on_delete_clicked)
        self.btn_edit.clicked.connect(self._on_edit_clicked)
        
        self.copy_btn = QPushButton("Kopiuj wybrane hasło")
        self.copy_btn.clicked.connect(self._on_copy_clicked)

        bottom_layout.addWidget(self.add_btn)
        bottom_layout.addWidget(self.btn_edit)
        bottom_layout.addWidget(self.btn_delete)
        bottom_layout.addWidget(self.copy_btn)
        main_layout.addLayout(bottom_layout)
        
        self.setLayout(main_layout)

    def _on_copy_clicked(self):
        current_row = self.table.currentRow()
        if current_row >= 0:
            record_id = self.table.item(current_row, 0).data(99)
            self.copy_requested.emit(record_id)
        else:
            QMessageBox.warning(self, "Uwaga", "Wybierz najpierw wiersz z tabeli!")

    def populate_table(self, records: list[dict]):
        self.displayed_records = records
        self.table.setRowCount(0)
        
        for row_idx, record in enumerate(records):
            self.table.insertRow(row_idx)
            
            title_item = QTableWidgetItem(record['title'])
            title_item.setData(99, record['id'])
            
            login_item = QTableWidgetItem(record['login'])
            pass_item = QTableWidgetItem("********")
            
            self.table.setItem(row_idx, 0, title_item)
            self.table.setItem(row_idx, 1, login_item)
            self.table.setItem(row_idx, 2, pass_item)
            
    def _get_selected_record_id(self) -> int | None:
        selected_indexes = self.table.selectionModel().selectedRows()
        if not selected_indexes:
            QMessageBox.warning(self, "Brak selekcji", "Proszę zaznaczyć rekord z tabeli.")
            return None
        
        row = selected_indexes[0].row()
        return self.displayed_records[row]['id']
    
    def _on_delete_clicked(self):
        record_id = self._get_selected_record_id()
        if record_id is None:
            return
            
        reply = QMessageBox.question(
            self, 'Potwierdzenie', 'Czy na pewno chcesz bezpowrotnie usunąć to hasło?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, 
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.delete_requested.emit(record_id)
            
    def _on_edit_clicked(self) -> None:
        record_id = self._get_selected_record_id()
        if record_id is None:
            return
        
        self.edit_requested.emit(record_id)