# main.py
import sys
from PySide6.QtWidgets import QApplication

# Import controller yang sudah menggabungkan semua
from app.gui_controller import MainWindow

def main():
    # Create application
    app = QApplication(sys.argv)
    
    # Create main window  
    window = MainWindow()
    window.show()
    
    print("Application started successfully!")
    
    # Run application
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
    
