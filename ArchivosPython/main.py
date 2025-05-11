import sys
from PyQt6.QtWidgets import QApplication
from ArchivosPython.login_menu import LoginSignupApp

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Iniciamos el login
    ventana_login = LoginSignupApp()

    # Cuando el login es exitoso, se abre la pantalla principal.
    def abrir_menu_principal(auth_result):
        # Extrae el nombre del usuario de Cognito (puede cambiarse por username real).
        from jwt import decode
        claims = decode(auth_result.get('IdToken'), options={"verify_signature": False})
        username = claims.get("custom:Username", "Usuario")

        app.setProperty("username", username)

        from ArchivosPython.pantalla_principal import PantallaPrincipal
        ventana_menu = PantallaPrincipal()
        ventana_menu.show()

    ventana_login.login_successful.connect(abrir_menu_principal)
    ventana_login.login_ui()
    ventana_login.show()

    sys.exit(app.exec())
