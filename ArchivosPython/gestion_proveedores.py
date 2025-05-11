from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QLineEdit, QLabel, QMessageBox
)
from PyQt6.QtCore import Qt


class GestionProveedores(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("📋 Gestión de Proveedores")
        self.setFixedSize(700, 500)

        layout = QVBoxLayout()
        self.setLayout(layout)

        # Título
        titulo = QLabel("Gestión de Proveedores")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titulo.setStyleSheet("font-size: 22px; font-weight: bold;")
        layout.addWidget(titulo)

        # Tabla
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(3)
        self.tabla.setHorizontalHeaderLabels(["Nombre", "Contacto", "Rubro"])
        layout.addWidget(self.tabla)

        # Formulario para agregar proveedor
        form_layout = QHBoxLayout()

        self.input_nombre = QLineEdit()
        self.input_nombre.setPlaceholderText("Nombre")
        form_layout.addWidget(self.input_nombre)

        self.input_contacto = QLineEdit()
        self.input_contacto.setPlaceholderText("Contacto")
        form_layout.addWidget(self.input_contacto)

        self.input_rubro = QLineEdit()
        self.input_rubro.setPlaceholderText("Rubro")
        form_layout.addWidget(self.input_rubro)

        btn_agregar = QPushButton("Agregar")
        btn_agregar.clicked.connect(self.agregar_proveedor)
        form_layout.addWidget(btn_agregar)

        layout.addLayout(form_layout)

        # Botón eliminar fila seleccionada
        btn_eliminar = QPushButton("Eliminar fila seleccionada")
        btn_eliminar.clicked.connect(self.eliminar_fila)
        layout.addWidget(btn_eliminar)

        # Botón volver
        btn_volver = QPushButton("← Volver al Menú Principal")
        btn_volver.clicked.connect(self.volver_a_menu)
        layout.addWidget(btn_volver)

    def agregar_proveedor(self):
        nombre = self.input_nombre.text().strip()
        contacto = self.input_contacto.text().strip()
        rubro = self.input_rubro.text().strip()

        if not nombre or not contacto or not rubro:
            QMessageBox.warning(self, "Campos incompletos", "Todos los campos deben estar completos.")
            return

        fila_actual = self.tabla.rowCount()
        self.tabla.insertRow(fila_actual)
        self.tabla.setItem(fila_actual, 0, QTableWidgetItem(nombre))
        self.tabla.setItem(fila_actual, 1, QTableWidgetItem(contacto))
        self.tabla.setItem(fila_actual, 2, QTableWidgetItem(rubro))

        # Limpiar inputs
        self.input_nombre.clear()
        self.input_contacto.clear()
        self.input_rubro.clear()

    def eliminar_fila(self):
        fila = self.tabla.currentRow()
        if fila >= 0:
            self.tabla.removeRow(fila)
        else:
            QMessageBox.information(self, "Seleccionar fila", "Seleccioná una fila para eliminar.")

    def volver_a_menu(self):
        from ArchivosPython.pantalla_principal import PantallaPrincipal
        self.close()
        self.menu = PantallaPrincipal()
        self.menu.show()
