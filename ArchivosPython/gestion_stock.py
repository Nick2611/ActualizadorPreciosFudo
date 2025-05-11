from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QLabel, QHeaderView
)
from PyQt6.QtGui import QColor
from PyQt6.QtCore import Qt
from ArchivosPython.filtrar_productos import listar_categorias
import requests
import json


class GestionStock(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestión de Stock")
        self.setFixedSize(700, 500)

        # Layout principal vertical
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Título de la pantalla.
        titulo = QLabel("📦 Inventario actual")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titulo.setStyleSheet("font-size: 24px; font-weight: bold;")
        self.layout.addWidget(titulo)

        # Tabla de productos
        self.tabla = QTableWidget()
        self.layout.addWidget(self.tabla)

        # Botón para volver al menú principal
        self.btn_volver = QPushButton("← Volver al Menú Principal")
        self.btn_volver.setStyleSheet("background-color: #f2f2f2;")
        self.btn_volver.clicked.connect(self.volver_a_menu)
        self.layout.addWidget(self.btn_volver)

        # Botón para actualizar/re-cargar la tabla
        self.btn_actualizar = QPushButton("🔄 Actualizar Stock")
        self.btn_actualizar.clicked.connect(self.cargar_datos)
        self.layout.addWidget(self.btn_actualizar)

        # Carga inicial de datos
        self.cargar_datos()

    def cargar_datos(self):
        # Obtiene token y categorías desde la API
        token, categorias = listar_categorias()
        url = "https://api.fu.do/v1alpha1/products?include=productCategory"
        headers = {
            "Accept": "application/json",
            "authorization": f"Bearer {token}"
        }

        try:
            response = requests.get(url, headers=headers)
            data = response.json()
        except Exception as e:
            print("Error al cargar productos:", e)
            return

        productos = data.get("data", [])

        # Configura la tabla
        self.tabla.setRowCount(len(productos))
        self.tabla.setColumnCount(3)
        self.tabla.setHorizontalHeaderLabels(["Producto", "Stock", "Categoría"])
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        for i, producto in enumerate(productos):
            nombre = producto["attributes"]["name"]
            stock = producto["attributes"]["stock"]
            categoria_id = producto["relationships"]["productCategory"]["data"]["id"]

            # Buscar nombre de la categoría desde el diccionario original
            categoria = next((k for k, v in categorias.items() if v == categoria_id), "Desconocida")

            # Cargar celdas
            item_nombre = QTableWidgetItem(nombre)
            item_stock = QTableWidgetItem(str(stock))
            item_categoria = QTableWidgetItem(categoria)

            # Colorear si el stock es bajo
            if stock <= 5:
                item_stock.setBackground(QColor(255, 204, 204))  # rojo claro

            self.tabla.setItem(i, 0, item_nombre)
            self.tabla.setItem(i, 1, item_stock)
            self.tabla.setItem(i, 2, item_categoria)

    def volver_a_menu(self):
        # Cierra esta ventana y abre la pantalla principal
        from ArchivosPython.pantalla_principal import PantallaPrincipal
        self.close()
        self.nueva_ventana = PantallaPrincipal()
        self.nueva_ventana.show()
