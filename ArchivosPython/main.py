import sys
from PyQt6.QtWidgets import QApplication
from ArchivosPython.login_menu import LoginSignupApp

if __name__ == "__main__":
    app = QApplication(sys.argv)  # Create the QApplication instance
    window = LoginSignupApp()     # Create the main window
    window.login_ui()             # Start the login UI
    window.show()                 # Show the window
    sys.exit(app.exec())          # Start the event loop