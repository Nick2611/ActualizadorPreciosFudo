from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QAction, QIcon, QKeySequence
from PyQt6.QtWidgets import (
    QApplication,
    QCheckBox,
    QLabel,
    QMainWindow,
    QStatusBar,
    QToolBar,
    QPushButton,
    QWidgetAction,
    QWidget,
    QSizePolicy,
)
from filtrar_productos import listar_categorias

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My App")
        self.setFixedSize(600,600)
        self.setStyleSheet("background-color: rgba(220, 216, 213, 1);")

        app = QApplication.instance()
        username = app.property("username")

        label = QLabel("Hello!")
        label.setStyleSheet("color: black;")

        # The `Qt` namespace has a lot of attributes to customize
        # widgets. See: http://doc.qt.io/qt-6/qt.html
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Set the central widget of the Window. Widget will expand
        # to take up all the space in the window by default.
        self.setCentralWidget(label)

        toolbar = QToolBar("My main toolbar")
        self.setUnifiedTitleAndToolBarOnMac(False)  # Add this line
        toolbar.setStyleSheet("background-color: white; border: none;")
        self.addToolBar(toolbar)

        stock_overview_button = QPushButton("Stock Overview")
        stock_overview_button.setStyleSheet(
            "border-radius: 10px; background-color: white; border: 2px solid grey; color: black;")
        stock_overview_button.setFixedSize(120, 50)  # Set custom size for the button
        widget_action = QWidgetAction(toolbar)
        widget_action.setDefaultWidget(stock_overview_button)
        toolbar.addAction(widget_action)

        toolbar.addSeparator()

        button = QPushButton("Generate Report")
        button.setStyleSheet(
            "border-radius: 10px; background-color: white; border: 2px solid grey; color: black;")
        button.setFixedSize(120, 50)  # Set custom size for the button
        widget_action = QWidgetAction(toolbar)
        widget_action.setDefaultWidget(button)
        button.setStyleSheet(button.styleSheet())  # Reapply the stylesheet
        toolbar.addAction(widget_action)

        toolbar.addSeparator()

        # Add a button to the toolbar
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        toolbar.addWidget(spacer)  # Add this before your button

        # Now add your account button
        account = QPushButton(f"Hola, {username}")
        account.setStyleSheet(
            "border-radius: 10px; background-color: white; color: black; font-size: 15px;")
        account.setFixedSize(120, 50)

        toolbar.addWidget(account)


        # toolbar.addWidget(QLabel("Hello"))
        # toolbar.addWidget(QCheckBox())


    def toolbar_button_clicked(self, s):
        print("click", s)

window = MainWindow()
window.show()
