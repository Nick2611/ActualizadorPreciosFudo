import requests
import json
import sys
from time import sleep
from user_token import main


def listar_categorias():
    """Funcion utilizada para recuperar las categorias de productos disponibles en la API de Fu.do
        utilizada por el archivo pantalla_principal.py para mostrar las categorias en la ventana principal"""

    #Llama a la funcion get_api_token del programa user_token para conseguir el token utilizado en las autorizaciones
    token = main()
    autorizacion = f'Bearer {token}'
    categorias = {}

    #URL base de donde solicitar la informacion
    url = "https://api.fu.do/v1alpha1/product-categories?sort=id&include=products&page%5Bnumber%5D=0&page%5Bsize%5D=0"

    # Define los headers para el request inicial de informacion
    headers = {
        "Accept": "application/json",
        "authorization": autorizacion

    }

    #Manejo de excepciones a la hora de realizar el request de informacion
    try:
        response = requests.get(url, headers=headers)
        items = response.json()
        items_json_str = json.dumps(items)
        items_json = json.loads(items_json_str)
    except requests.exceptions.HTTPError as errh:
        print(f"Error http {errh}")
        sleep(1)
        sys.exit(1)

    # Extrae la informacion de las categorias y las guarda en un diccionario
    for objeto in items_json["data"]:
        nombre = objeto["attributes"]["name"]
        categorias[nombre] = objeto["id"]

    #Retorna el token y las categorias
    return token, categorias

listar_categorias()
