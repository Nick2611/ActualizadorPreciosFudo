import tkinter as tk
from filtrar_productos import listar_categorias
from Actualizador_de_precios import actualizador

# Fetch token and categories
token, categorias = listar_categorias()
autorizacion = f'"Bearer {token}"'

def make_listbox(wn, cat, selected_items, ruta):
    """Abre una ventana secundaria para seleccionar elementos, utilizada por mainscreen"""
    auxS = tk.Toplevel(wn)
    auxS.geometry("300x300")
    nombres = list(cat.keys())
    indices = []

    lb = tk.Listbox(auxS, selectmode=tk.MULTIPLE)
    back_b = tk.Button(auxS, text="Volver", command=lambda: auxS.destroy())
    scrollb = tk.Scrollbar(auxS, orient=tk.VERTICAL)  # Create the scrollbar

    lb = tk.Listbox(auxS, selectmode=tk.MULTIPLE, yscrollcommand=scrollb.set)  # Link the scrollbar to the Listbox

    scrollb.config(command=lb.yview)  # Configure the scrollbar to control the Listbox

    # Function for finalizing selection
    def finalize_selection():
        selected_indices = lb.curselection()
        selected_items.extend([nombres[i] for i in selected_indices])  # Add selected items to the shared list
        for objeto in selected_items:
            if objeto in cat:
                indices.append(cat[objeto])
        auxS.destroy()
        actualizador(indices, ruta, autorizacion=autorizacion)

    finish_b = tk.Button(auxS, text="Finalizar", command=finalize_selection)

    # Add items to the Listbox
    for index, item in enumerate(cat):
        lb.insert(index, item)

    # Place widgets
    lb.place(relx=0.3, rely=0.1, relheight=0.6)  # Adjust height for scrollbar
    scrollb.place(relx=0.7, rely=0.1, relheight=0.6)  # Place scrollbar next to Listbox
    back_b.place(relx=0, rely=0)
    finish_b.place(relx=0.4, rely=0.7)


def mainscreen(cat):
    """Ventana principal del programa"""
    window = tk.Tk()
    window.title("Menú Principal")

    categorias = cat
    selected_items = []  # Lista para almacenar las selecciones de la ventana secundaria
    ruta = tk.IntVar(value=0)  # Variable para almacenar la ruta seleccionada

    # Configuración de la ventana principal
    window_width = 585
    window_height = 713 #OPCIONAL - modificar valores para ajustar el tamaño de la ventana a gusto
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    center_x = int((screen_width / 2) - (window_width / 2))
    center_y = int((screen_height / 2) - (window_height / 2))
    window.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
    window.configure(bg="#FFFFFF")

    # Widgets
    rectangle = tk.Frame(window, width=1000, height=100, bg="#6BA87E", bd=100, highlightthickness=0)
    rectangle.place(x=0, y=2)

    bienvenido_label = tk.Label(window, text="¡Bienvenido!", bg="#6BA87E", font=("times new roman", 40, "bold"))
    bienvenido_label.place(rely=0.03, relx=0.49, anchor="n")

    pregunta_label = tk.Label(window, text="¿Qué desea hacer hoy?", bg="#FFFFFF", font=("times new roman", 25, "bold"))
    pregunta_label.place(rely=0.18, relx=0.49, anchor="n")

    # Botones principales
    b1 = tk.Button(window, text="Cambiar todos los precios", command=lambda: [ruta.set(1), actualizador(selected_items, ruta.get(), autorizacion=autorizacion), window.destroy()])
    b2 = tk.Button(window, text="Cambiar todos menos algunos precios",
                   command=lambda: [ruta.set(2), make_listbox(window, categorias, selected_items, ruta.get())])
    b3 = tk.Button(window, text="Cambiar solo algunos precios", command=lambda: [ruta.set(3), make_listbox(window, categorias, selected_items, ruta.get())])
    exit_button = tk.Button(window, text="Salir", command=lambda: window.destroy())

    # Posicionamiento de los botones
    b1.place(rely=0.35, relx=0.49, anchor="n", width=280, height=50)
    b2.place(rely=0.5, relx=0.49, anchor="n", width=280, height=50)
    b3.place(rely=0.65, relx=0.49, anchor="n", width=280, height=50)
    exit_button.place(rely=0.92, relx=0.49, anchor="s", width=190, height=50)

    window.resizable(False, False)
    window.mainloop()


# Main Execution
mainscreen(categorias)

