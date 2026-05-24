HIGH_CONTRAST_STYLESHEET = """
QWidget {
    background-color: #000000;
    color: #FFFF00;
    font-size: 18px;
    font-weight: bold;
    font-family: Arial;
}

QLineEdit {
    background-color: #000000;
    color: #FFFF00;
    border: 3px solid #FFFF00;
    padding: 8px;
}

QPushButton {
    background-color: #FFFF00;
    color: #000000;
    border: 2px solid #FFFFFF;
    padding: 10px;
}

QPushButton:hover {
    background-color: #FFFFFF;
    color: #000000;
}

QLabel {
    color: #00FFFF;
}

QTableWidget {
    background-color: #000000;
    color: #FFFF00;
    gridline-color: #FFFFFF;
    border: 3px solid #FFFF00;
}

QHeaderView::section {
    background-color: #000000;
    color: #00FFFF;
    border: 1px solid #FFFFFF;
    padding: 4px;
}
"""