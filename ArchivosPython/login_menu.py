import sys
import os
import hmac
import hashlib
import base64
import boto3
import time
from botocore.exceptions import ClientError
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QStackedLayout
)
from PyQt6.QtCore import pyqtSignal
from dotenv import load_dotenv

load_dotenv()
AWS_REGION = os.getenv('AWS_REGION')
USER_POOL_ID = os.getenv('USER_POOL_ID')
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')

client = boto3.client('cognito-idp', region_name=AWS_REGION)


class LoginSignupApp(QWidget):
    login_successful = pyqtSignal(dict)  # Signal to emit authentication result

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login / Signup")
        self.setBaseSize(500, 500)

        # Main layout
        main_layout = QVBoxLayout()
        main_widget = QWidget()

        # Top buttons
        btn_layout = QHBoxLayout()
        self.login_btn = QPushButton("Log In")
        self.signup_btn = QPushButton("Sign Up")
        self.login_btn.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        self.signup_btn.clicked.connect(lambda: self.stack.setCurrentIndex(2))
        btn_layout.addWidget(self.login_btn)
        btn_layout.addWidget(self.signup_btn)
        main_layout.addLayout(btn_layout)

        # Stacked layout for forms
        self.stack = QStackedLayout()

        # Log In form
        login_widget = QWidget()
        login_layout = QVBoxLayout()
        login_layout.addWidget(QLabel("Email:"))
        self.log_in_email = QLineEdit()
        login_layout.addWidget(self.log_in_email)

        login_layout.addWidget(QLabel("Password:"))
        self.log_in_password = QLineEdit()
        login_layout.addWidget(self.log_in_password)

        self.send_login = QPushButton("Log in")
        self.send_login.clicked.connect(self.check_login_data)
        login_layout.addWidget(self.send_login)

        login_widget.setLayout(login_layout)

        # Sign Up form
        signup_widget = QWidget()
        signup_layout = QVBoxLayout()

        signup_layout.addWidget(QLabel("Email:"))
        self.email = QLineEdit()
        signup_layout.addWidget(self.email)

        signup_layout.addWidget(QLabel("Username:"))
        self.username = QLineEdit()
        signup_layout.addWidget(self.username)

        signup_layout.addWidget(QLabel("Password:"))
        self.password = QLineEdit()
        signup_layout.addWidget(self.password)

        signup_layout.addWidget(QLabel("Api key:"))
        self.api_key = QLineEdit()
        signup_layout.addWidget(self.api_key)

        signup_layout.addWidget(QLabel("Api secret:"))
        self.api_secret = QLineEdit()
        signup_layout.addWidget(self.api_secret)

        self.send_info = QPushButton("Sign Up")
        self.send_info.clicked.connect(self.send_sign_up_data)
        signup_layout.addWidget(self.send_info)

        signup_widget.setLayout(signup_layout)

        # confirmation form
        confirmation_widget = QWidget()
        confirmation_layout = QVBoxLayout()
        confirmation_layout.addWidget(QLabel("Confirmation Code:"))
        self.confirmation_code = QLineEdit()
        confirmation_layout.addWidget(self.confirmation_code)
        self.confirmation_buttton = QPushButton("Confirm")
        self.confirmation_buttton.clicked.connect(self.send_confirmation_code)
        confirmation_layout.addWidget(self.confirmation_buttton)
        confirmation_widget.setLayout(confirmation_layout)

        # Add both widgets to stack
        self.stack.addWidget(main_widget)
        self.stack.addWidget(login_widget)
        self.stack.addWidget(signup_widget)
        self.stack.addWidget(confirmation_widget)

        # Add stack to main layout
        main_layout.addLayout(self.stack)

        self.setLayout(main_layout)

    def get_secret_hash(self, username):
        message = username + CLIENT_ID
        dig = hmac.new(
            CLIENT_SECRET.encode('utf-8'),
            message.encode('utf-8'),
            hashlib.sha256
        ).digest()
        return base64.b64encode(dig).decode()

    def send_sign_up_data(self):
        # Logic to send login info
        email = self.email.text().strip()
        username = self.username.text()
        password = self.password.text()
        api_key = self.api_key.text().strip()
        api_secret = self.api_secret.text().strip()

        secret_hash = self.get_secret_hash(email)

        try:
            response = client.sign_up(
                ClientId=CLIENT_ID,
                Username=email,  # This is the email, used as the 'Username'
                Password=password,
                SecretHash=secret_hash,
                UserAttributes=[
                    {'Name': 'email', 'Value': email},  # Use 'email' as the Username
                    {'Name': 'custom:Username', 'Value': username},  # Store the custom username here
                    {'Name': 'custom:ApiKey', 'Value': api_key},
                    {'Name': 'custom:ApiSecret', 'Value': api_secret},
                ]
            )
            print("Sign-up successful!")
            time.sleep(1.5)

            # Switch to confirmation code input
            self.stack.setCurrentIndex(3)

        except ClientError as e:
            print(e.response['Error']['Message'])

    def send_confirmation_code(self):
        # Confirm sign-up
        self.stack.setCurrentIndex(3)
        email = self.email.text().strip()
        confirmation_code = self.confirmation_code.text().strip()  # Use the correct QLineEdit instance
        try:
            response = client.confirm_sign_up(
                ClientId=CLIENT_ID,
                Username=email,
                ConfirmationCode=confirmation_code,  # Pass the confirmation code text
                SecretHash=self.get_secret_hash(email),
            )
            print(response)
        except ClientError as e:
            print(e.response['Error']['Message'])

    def check_login_data(self):
        # Call Cognito to authenticate
        email = self.log_in_email.text().strip()
        password = self.log_in_password.text()

        try:
            response = client.initiate_auth(
                ClientId=CLIENT_ID,
                AuthFlow='USER_PASSWORD_AUTH',
                AuthParameters={
                    'USERNAME': email,
                    'PASSWORD': password,
                    'SECRET_HASH': self.get_secret_hash(email)
                }
            )
            print("Authentication successful!")
            auth_result = response.get("AuthenticationResult")
            if auth_result:
                self.login_successful.emit(auth_result)  # Emit the authentication result
            # You might want to close the login window here if successful
            self.close()

        except client.exceptions.NotAuthorizedException:
            print("Incorrect username or password.")
        except client.exceptions.UserNotConfirmedException:
            print("User is not confirmed.")
        except Exception as e:
            print(f"An error occurred: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginSignupApp()
    window.show()
    sys.exit(app.exec())