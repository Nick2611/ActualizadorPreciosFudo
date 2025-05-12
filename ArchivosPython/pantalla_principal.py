import sys
from ArchivosPython.Actualizador_de_precios import actualizador
from ArchivosPython.gestion_stock import GestionStock
from ArchivosPython.calculadora_ganancias import CalculadoraGanancias
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QLabel, QPushButton, QWidget, QHBoxLayout
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

# Clase principal que representa la ventana principal del ERP
class PantallaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ERP - Panel Principal")  # Título de la ventana
        self.setFixedSize(600, 500)  # Tamaño fijo de la ventana
        self.setStyleSheet("background-color: #f2f1f0;")  # Color de fondo

        self.init_ui()  # Llama a la función que inicializa la interfaz gráfica

    def ejecutar_actualizador(self):
        from ArchivosPython.filtrar_productos import listar_categorias
        token, categorias = listar_categorias()

        # Por ahora, usamos todos los productos sin filtro (ruta = 1)
        ruta = 1
        categorias_filtradas = []
        autorizacion = f'Bearer {token}'

        actualizador(categorias_filtradas, ruta, autorizacion)

    def abrir_gestion_stock(self):
        self.close()  # Cierra la pantalla principal actual
        self.stock_window = GestionStock()  # Crea instancia de la ventana de stock
        self.stock_window.show()  # La muestra

    def abrir_calculadora_ganancias(self):
        self.close()  # Cierra la pantalla principal actual
        self.ventana_ganancias = CalculadoraGanancias()
        self.ventana_ganancias.show()

    def abrir_gestion_proveedores(self):
        self.close()  # Cierra esta ventana
        self.ventana_proveedores = GestionProveedores()
        self.ventana_proveedores.show()

    def init_ui(self):
        # Obtiene el nombre del usuario desde las propiedades de la aplicación
        username = QApplication.instance().property("username") or "Usuario"

        # Layout principal vertical
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)  # Alineación arriba
        layout.setContentsMargins(30, 30, 30, 30)  # Márgenes internos
        layout.setSpacing(20)  # Espaciado entre elementos

        # Mensaje de bienvenida con el nombre del usuario
        label_bienvenida = QLabel(f"Hola, {username}! Bienvenido al sistema")
        label_bienvenida.setFont(QFont("Helvetica Neue", 18))
        label_bienvenida.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label_bienvenida)

        # Creación de los botones principales del sistema
        btn_stock = QPushButton("Gestión de Stock")
        btn_stock.clicked.connect(self.abrir_gestion_stock) #conecto el botón de Gestión Stock
        btn_precios = QPushButton("Actualización de Precios")
        btn_precios.clicked.connect(self.ejecutar_actualizador) #conecto el botón de Actualizar Precios
        btn_ganancias = QPushButton("Calculadora de Ganancias")
        btn_ganancias.clicked.connect(self.abrir_calculadora_ganancias) #conecto el botón de Calculadora Ganancias
        btn_proveedores = QPushButton("Gestión de Proveedores")
        btn_proveedores.clicked.connect(self.abrir_gestion_proveedores) #conecto el botón de Gestion de Proveedores

        # Aplica estilo y tamaño a todos los botones y los agrega al layout
        for btn in [btn_stock, btn_precios, btn_ganancias, btn_proveedores]:
            btn.setFixedSize(250, 50)
            btn.setStyleSheet("border-radius: 10px; background-color: white; border: 2px solid grey; color: black;")
            layout.addWidget(btn, alignment=Qt.AlignmentFlag.AlignHCenter)

        # Contenedor final que se asigna a la ventana
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

# Permite ejecutar el archivo directamente para pruebas
if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setProperty("username", "EjemploUsuario")  # Simulación para pruebas locales
    window = PantallaPrincipal()
    window.show()
    sys.exit(app.exec())

