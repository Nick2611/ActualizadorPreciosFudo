import jwt
import json
import sys
import requests
from PyQt6.QtWidgets import QApplication
from login_menu import LoginSignupApp  # Import your login menu application
from time import sleep

def main():
    def get_user_tokens():
        app = QApplication(sys.argv)
        login_window = LoginSignupApp()

        user_tokens = {}

        def handle_login_success(auth_result):
            nonlocal user_tokens
            user_tokens['id_token'] = auth_result.get('IdToken')
            print("Tokens received in user_token.py:", user_tokens)
            app.quit()  # Close the application after successful login


        login_window.login_successful.connect(handle_login_success)
        login_window.show()
        app.exec()  # Start the PyQt event loop

        return user_tokens

    def get_api_token(headers, data):

        try:
            response = requests.post(url, headers=headers, data=json.dumps(data))
            response.raise_for_status()  # Raise HTTPError for bad responses
        except requests.exceptions.HTTPError as errh:
            print(f"HTTP Error: {errh}")
            sleep(1)
            sys.exit(1)  # Exit program with status 1 (or any non-zero code)
        except requests.exceptions.ConnectionError as errc:
            print(f"Connection Error: {errc}")
            sleep(1)
            sys.exit(1)  # Exit program
        except requests.exceptions.Timeout as errt:
            print(f"Timeout Error: {errt}")
            sleep(1)
            sys.exit(1)  # Exit program
        except requests.exceptions.RequestException as err:
            print(f"Request Exception: {err}")
            sleep(1)
            sys.exit(1)  # Exit program

        try:
            token = response.json().get('token')
            if token:
                print(f"Token obtenido: {token}")
                print()
                return token
            else:
                print("No se pudo obtener el token.")

        except json.JSONDecodeError as json_err:
            print(f"Error al decodificar la respuesta JSON: {json_err}")
            sys.exit(1)  # Exit program

    tokens = get_user_tokens()

    # Check if tokens are received
    if tokens:
        claims = jwt.decode(tokens["id_token"], options={"verify_signature": False})
        api_key, api_secret = claims["custom:ApiKey"], claims["custom:ApiSecret"]
        url = "https://auth.fu.do/api"
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        data = {
            "apiKey": api_key,
            "apiSecret": api_secret,
        }

        return get_api_token(headers, data)

    return None