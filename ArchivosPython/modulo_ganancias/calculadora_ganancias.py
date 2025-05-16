from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt6.QtCore import Qt
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import random
from datetime import datetime, timedelta


class CalculadoraGanancias(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("📈 Ganancias del Mes")
        self.setFixedSize(700, 500)

        layout = QVBoxLayout()
        self.setLayout(layout)

        # Título
        titulo = QLabel("Proyección de Ganancias del Mes")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titulo.setStyleSheet("font-size: 22px; font-weight: bold;")
        layout.addWidget(titulo)

        # Crear figura de matplotlib para insertar en el layout
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        # Botón volver
        btn_volver = QPushButton("← Volver al Menú Principal")
        btn_volver.clicked.connect(self.volver_a_menu)
        layout.addWidget(btn_volver)

        # Cargar gráfico con datos simulados
        self.generar_datos_simulados()

    def generar_datos_simulados(self):
        # Genera datos aleatorios para los últimos 30 días
        hoy = datetime.today()
        fechas = [hoy - timedelta(days=i) for i in range(29, -1, -1)]
        fechas_str = [f.strftime("%d/%m") for f in fechas]
        ganancias = [random.randint(8000, 25000) for _ in fechas]

        # Limpiar y plotear gráfico
        self.ax.clear()
        self.ax.bar(fechas_str, ganancias)
        self.ax.set_title("Ganancias Diarias (últimos 30 días)")
        self.ax.set_ylabel("Pesos")
        self.ax.tick_params(axis='x', rotation=45)
        self.figure.tight_layout()
        self.canvas.draw()

    def volver_a_menu(self):
        from ArchivosPython.gestion_principal.pantalla_principal import PantallaPrincipal
        self.close()
        self.menu = PantallaPrincipal()
        self.menu.show()
