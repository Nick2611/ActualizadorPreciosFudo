import sys

from PyQt6 import QtCore
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QLabel, QPushButton, QWidget, QHBoxLayout, QSizePolicy,
    QSizePolicy, QMenu,
)
from PyQt6.QtCore import Qt, QSize, QPoint
from PyQt6.QtGui import QFont, QColor, QPalette, QPixmap, QIcon, QAction, QCursor


# Clase principal que representa la ventana principal del ERP
class PantallaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ERP - Panel Principal")  # Título de la ventana
        self.setFixedSize(1000, 550)  # Tamaño fijo de la ventana
        self.setStyleSheet("background-color: #f2f1f0;")  # Color de fondo

        self.init_ui()  # Llama a la función que inicializa la interfaz gráfica

    # def ejecutar_actualizador(self):
    #     from ArchivosPython.filtrar_productos import listar_categorias
    #     token, categorias = listar_categorias()
    #
    #     # Por ahora, usamos todos los productos sin filtro (ruta = 1)
    #     ruta = 1
    #     categorias_filtradas = []
    #     autorizacion = f'Bearer {token}'
    #
    #     actualizador(categorias_filtradas, ruta, autorizacion)
    #
    # def abrir_gestion_stock(self):
    #     self.close()  # Cierra la pantalla principal actual
    #     self.stock_window = GestionStock()  # Crea instancia de la ventana de stock
    #     self.stock_window.show()  # La muestra
    #
    # def abrir_calculadora_ganancias(self):
    #     self.close()  # Cierra la pantalla principal actual
    #     self.ventana_ganancias = CalculadoraGanancias()
    #     self.ventana_ganancias.show()

    def crear_modulo_widget(self, image_path: str, name_text: str, description_text: str, button_purpose: str) -> QWidget:
        widget = QWidget()
        widget.setStyleSheet("background-color: white; border-radius: 20px; border: 1px solid #ccc;")
        widget.setFixedSize(250, 400)

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 40, 20, 50)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        label = QLabel()
        label.setStyleSheet("border: white")
        pixmap = QPixmap(image_path)
        if not pixmap.isNull():
            label.setPixmap(
                pixmap.scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        else:
            label.setText("Image not found")

        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)

        text_label = QLabel(name_text)
        text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        text_label.setStyleSheet("font-size: 18px; font-weight: bold; color: black; border: white")
        layout.addWidget(text_label)

        description_label = QLabel(description_text)
        description_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        description_label.setStyleSheet("font-size: 10px; color: black; border: white")
        layout.addWidget(description_label)
        layout.addStretch()  # Esto empuja el botón hacia abajo

        purpose_button = QPushButton(button_purpose)
        purpose_button.setFixedSize(150, 35)
        purpose_button.setStyleSheet(
            "border-radius: 5px; background-color: rgb(80, 117, 158); border: 1px solid grey; color: white;")
        purpose_button.setCursor(Qt.CursorShape.PointingHandCursor)

        layout.addWidget(purpose_button, alignment=Qt.AlignmentFlag.AlignCenter)

        widget.setLayout(layout)
        return widget

    def init_ui(self):
        username = QApplication.instance().property("username") or "Usuario"

        # ─── Barra azul superior y sus componentes ─────────────────────────────────────────
        color_widget = QWidget()
        color_widget.setFixedHeight(50)
        color_widget.setStyleSheet("background-color: rgb(80, 117, 158);")
        color_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        color_layout = QHBoxLayout()
        color_layout.setContentsMargins(20, 0, 20, 0)

        labelTitle = QLabel("ERP")
        labelTitle.setStyleSheet("color: white; font-weight: bold; font: Helvetica; font-size: 30px;")
        labelTitle.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        color_layout.addWidget(labelTitle)

        user_button = QPushButton()
        user_button.setIcon(QIcon("../image_icons/user_icon.png"))
        user_button.setIconSize(QSize(35, 35))
        user_button.setStyleSheet("""
            border: none;
            background-color: transparent;
        """)
        user_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.menu = QMenu(user_button)  # importante: pasamos el botón como parent
        self.menu.setStyleSheet("""
            QMenu {
                background-color: white;
                border: 1px solid #ccc;
            }
            QMenu::item {
                padding: 8px 20px;
                background-color: white;
                color: black;
            }
            QMenu::item:selected {
                background-color: rgb(80, 117, 158);  /* hover background */
                color: white;                         /* hover text color */
            }
        """)
        info_action = QAction("Ver información del usuario", self)
        logout_action = QAction("Cerrar sesión", self)

        self.menu.addAction(info_action)
        self.menu.addAction(logout_action)

        def show_menu():
            pos = user_button.mapToGlobal(QPoint(0, user_button.height()))
            self.menu.popup(pos)  # popup es no-bloqueante y más confiable en algunos entornos

        user_button.clicked.connect(show_menu)
        color_layout.addWidget(user_button, alignment=Qt.AlignmentFlag.AlignRight)

        color_widget.setLayout(color_layout)

        # ─── 3 Modulos principales ─────────────────────
        stock_widget = self.crear_modulo_widget("../image_icons/stock.png", "Gestión de Stock", "Gestión de productos y stock", "Ver stock")
        revenue_widget = self.crear_modulo_widget("../image_icons/revenue.png", "Ganancias", "Calculadora de Ganancias", "Calcular ganancias")
        prices_widget = self.crear_modulo_widget("../image_icons/prices.png", "Actualizador de Precios", "Actualiza precios de productos", "Actualizar precios")

        # ─── Layout central para los modulos ────────────────────────────
        center_layout = QHBoxLayout()
        center_layout.setSpacing(40)
        center_layout.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)
        center_layout.addWidget(stock_widget)
        center_layout.addWidget(revenue_widget)
        center_layout.addWidget(prices_widget)

        # ─── Layout vertical principal ─────────────────────────────────
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(color_widget)
        main_layout.addStretch()
        main_layout.addLayout(center_layout)
        main_layout.addStretch()

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setProperty("username", "EXAMPLE")  # Simulación para pruebas locales
    window = PantallaPrincipal()
    window.show()
    sys.exit(app.exec())

