from PyQt6.QtCore import QObject, QEvent, QTimer, pyqtSignal

class InactivityFilter(QObject):
    timeout_reached = pyqtSignal()
    
    def __init__(self, timeout_ms: int, parent=None):
        super().__init__(parent)
        self.timer = QTimer(self)
        self.timer.setInterval(timeout_ms)
        self.timer.timeout.connect(self.timeout_reached.emit)
        self.timer.start()
        
    def eventFilter(self, obj: QObject, event: QEvent) -> bool:
        if event.type() in (QEvent.Type.MouseMove, QEvent.Type.MouseButtonPress, QEvent.Type.KeyPress):
            self.timer.start()  # Resetowanie czasu przy aktywnosci
            
        return super().eventFilter(obj, event)