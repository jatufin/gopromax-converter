import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GoPro Video Converter")
        self.setGeometry(100, 100, 800, 600)
        label = QLabel("Welcome!", self)
        label.setGeometry(50, 50, 700, 50)

def main():
    app  = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
