import os
import hmac
import hashlib
import base64
import boto3
import time

from botocore.exceptions import ClientError
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QMainWindow,
    QLineEdit, QCheckBox
)
from PyQt6.QtCore import pyqtSignal, Qt
from dotenv import load_dotenv

load_dotenv()
AWS_REGION = os.getenv('AWS_REGION')
USER_POOL_ID = os.getenv('USER_POOL_ID')
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')

client = boto3.client('cognito-idp', region_name=AWS_REGION)


class LoginSignupApp(QMainWindow):
    login_successful = pyqtSignal(dict)  # Signal to emit authentication result

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login / Signup")
        self.setBaseSize(350, 500)
        self.setStyleSheet("background-color: rgba(242, 241, 240, 1);")


    def login_ui(self):
        #Login UI
        self.setFixedSize(350, 500)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(10)

        # Wrapper for form elements
        form_layout = QVBoxLayout()
        form_layout.setSpacing(15)

        # "Log In" label
        log_in_label = QLabel("Log In")
        log_in_label.setStyleSheet("""
            color: black;
            font-size: 30px;
            font-weight: bold;
            font-family: Helvetica Neue;
        """)
        log_in_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        form_layout.addWidget(log_in_label)

        # Email label
        email_label = QLabel("Email")
        email_label.setStyleSheet("""
            color: black;
            font-size: 15px;
            font-family: Helvetica Neue;
        """)
        email_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        form_layout.addWidget(email_label)

        self.login_email_input = QLineEdit()
        self.login_email_input.setStyleSheet("border-radius: 10px; background-color: rgba(230, 226, 223, 1); border: 1px solid grey; color: black;")
        self.login_email_input.setFixedSize(250, 35)
        self.login_email_input.setAlignment(Qt.AlignmentFlag.AlignLeft)
        form_layout.addWidget(self.login_email_input)

        # Password label
        password_label = QLabel("Password")
        password_label.setStyleSheet("""
            color: black;
            font-size: 15px;
            font-family: Helvetica Neue;
        """)
        password_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        form_layout.addWidget(password_label)

        password_layout = QHBoxLayout()

        self.login_password_input = QLineEdit()
        self.login_password_input.setStyleSheet("border-radius: 10px; background-color: rgba(230, 226, 223, 1); border: 1px solid grey; color: black;")
        self.login_password_input.setFixedSize(250, 35)
        self.login_password_input.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.login_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        password_layout.addWidget(self.login_password_input)

        show_password_checkbox = QCheckBox("Show")
        show_password_checkbox.setStyleSheet("color: black; font-size: 12px; font-family: Helvetica Neue; background-color: rgba(230, 226, 223, 1)")
        show_password_checkbox.toggled.connect(lambda checked: self.login_password_input.setEchoMode(QLineEdit.EchoMode.Normal if checked else QLineEdit.EchoMode.Password))
        password_layout.addWidget(show_password_checkbox)

        form_layout.addLayout(password_layout)

        # Log In button
        log_in_button = QPushButton("Log In")
        log_in_button.setFixedSize(150, 35)
        log_in_button.setStyleSheet("border-radius: 5px; background-color: rgb(80, 117, 158); border: 1px solid grey; color: white;")
        log_in_button.clicked.connect(self.check_login_data)
        form_layout.addWidget(log_in_button, alignment=Qt.AlignmentFlag.AlignHCenter)

        #Don't have an accont label and sign up button
        dont_have_account_label = QLabel("Don't have an account?")
        dont_have_account_label.setStyleSheet("""
            color: black;
            font-size: 12px;
            font-family: Helvetica Neue;
        """)
        dont_have_account_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        form_layout.addWidget(dont_have_account_label)

        # Signup button
        signup_button = QPushButton("Sign up")
        signup_button.setFixedSize(100, 35)
        signup_button.setStyleSheet("border-radius: 5px; background-color: rgba(242, 241, 240, 1); border: 1px solid grey; color: rgb(65, 79, 111);")
        signup_button.clicked.connect(self.signup_ui)
        form_layout.addWidget(signup_button)

        # Form container
        form_widget = QWidget()
        form_widget.setLayout(form_layout)
        main_layout.addWidget(form_widget, alignment=Qt.AlignmentFlag.AlignTop)

        # Final container
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def signup_ui(self):
        self.setFixedSize(340,680)
        signup_layout = QVBoxLayout()
        signup_layout.setContentsMargins(20, 20, 20, 20)
        signup_layout.setSpacing(5)

        # Wrapper for form elements
        signup_form_layout = QVBoxLayout()
        signup_form_layout.setSpacing(15)

        # "Sign up" label
        signup_label = QLabel("Sign up")
        signup_label.setStyleSheet("""
                    color: black;
                    font-size: 30px;
                    font-weight: bold;
                    font-family: Helvetica Neue;
                """)
        signup_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        signup_form_layout.addWidget(signup_label)

        # Email label
        signup_email_label = QLabel("Email")
        signup_email_label.setStyleSheet("""
                    color: black;
                    font-size: 15px;
                    font-family: Helvetica Neue;
                """)
        signup_email_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        signup_form_layout.addWidget(signup_email_label)

        self.signup_email_input = QLineEdit()
        self.signup_email_input.setStyleSheet(
            "border-radius: 10px; background-color: rgba(230, 226, 223, 1); border: 1px solid grey; color: black;")
        self.signup_email_input.setFixedSize(250, 35)
        self.signup_email_input.setAlignment(Qt.AlignmentFlag.AlignLeft)
        signup_form_layout.addWidget(self.signup_email_input)

        # Username label
        signup_username_label = QLabel("Username")
        signup_username_label.setStyleSheet("""
                    color: black;
                    font-size: 15px;
                    font-family: Helvetica Neue;
                """)
        signup_username_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        signup_form_layout.addWidget(signup_username_label)

        self.signup_username_input = QLineEdit()
        self.signup_username_input.setStyleSheet(
            "border-radius: 10px; background-color: rgba(230, 226, 223, 1); border: 1px solid grey; color: black;")
        self.signup_username_input.setFixedSize(250, 35)
        self.signup_username_input.setAlignment(Qt.AlignmentFlag.AlignLeft)
        signup_form_layout.addWidget(self.signup_username_input)

        # API Key label
        signup_apikey_label = QLabel("API Key")
        signup_apikey_label.setStyleSheet("""
                    color: black;
                    font-size: 15px;
                    font-family: Helvetica Neue;
                """)
        signup_apikey_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        signup_form_layout.addWidget(signup_apikey_label)

        self.signup_apikey_input = QLineEdit()
        self.signup_apikey_input.setStyleSheet(
            "border-radius: 10px; background-color: rgba(230, 226, 223, 1); border: 1px solid grey; color: black;")
        self.signup_apikey_input.setFixedSize(250, 35)
        self.signup_apikey_input.setAlignment(Qt.AlignmentFlag.AlignLeft)
        signup_form_layout.addWidget(self.signup_apikey_input)

        # API Secret label
        signup_apisecret_label = QLabel("API Secret")
        signup_apisecret_label.setStyleSheet("""
                    color: black;
                    font-size: 15px;
                    font-family: Helvetica Neue;
                """)
        signup_apisecret_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        signup_form_layout.addWidget(signup_apisecret_label)

        self.signup_apisecret_input = QLineEdit()
        self.signup_apisecret_input.setStyleSheet(
            "border-radius: 10px; background-color: rgba(230, 226, 223, 1); border: 1px solid grey; color: black;")
        self.signup_apisecret_input.setFixedSize(250, 35)
        self.signup_apisecret_input.setAlignment(Qt.AlignmentFlag.AlignLeft)
        signup_form_layout.addWidget(self.signup_apisecret_input)

        # Password label
        signup_password_label = QLabel("Password")
        signup_password_label.setStyleSheet("""
                    color: black;
                    font-size: 15px;
                    font-family: Helvetica Neue;
                """)
        signup_password_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        signup_form_layout.addWidget(signup_password_label)

        self.signup_password_input = QLineEdit()
        self.signup_password_input.setStyleSheet(
            "border-radius: 10px; background-color: rgba(230, 226, 223, 1); border: 1px solid grey; color: black;")
        self.signup_password_input.setFixedSize(250, 35)
        self.signup_password_input.setAlignment(Qt.AlignmentFlag.AlignLeft)
        signup_form_layout.addWidget(self.signup_password_input)

        # Show password checkbox
        show_password_checkbox = QCheckBox("Show Password")
        show_password_checkbox.setStyleSheet("color: black; font-size: 12px; font-family: Helvetica Neue; background-color: rgba(242, 241, 240, 1)")
        signup_form_layout.addWidget(show_password_checkbox, alignment=Qt.AlignmentFlag.AlignLeft)

        # Sign up button
        signup_button = QPushButton("Sign up")
        signup_button.setFixedSize(150, 35)
        signup_button.setStyleSheet(
            "border-radius: 5px; background-color: rgb(80, 117, 158); border: 1px solid grey; color: white;")
        signup_button.clicked.connect(self.send_signup_data)
        signup_form_layout.addWidget(signup_button, alignment=Qt.AlignmentFlag.AlignHCenter)

        # Already have an account
        have_account_label = QLabel("Already have an account?")
        have_account_label.setStyleSheet("""
                    color: black;
                    font-size: 12px;
                    font-family: Helvetica Neue;
                """)
        have_account_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        signup_form_layout.addWidget(have_account_label)

        # Login button
        login_button = QPushButton("Log in")
        login_button.setFixedSize(100, 35)
        login_button.setStyleSheet(
            "border-radius: 5px; background-color: rgba(242, 241, 240, 1); border: 1px solid grey; color: rgb(65, 79, 111);")
        login_button.clicked.connect(self.login_ui)
        signup_form_layout.addWidget(login_button)

        # Form container
        form_widget = QWidget()
        form_widget.setLayout(signup_form_layout)
        signup_layout.addWidget(form_widget, alignment=Qt.AlignmentFlag.AlignTop)

        # Final container
        container = QWidget()
        container.setLayout(signup_layout)
        self.setCentralWidget(container)

    def confirmation_ui(self, email):
        self.setFixedSize(500, 300)
        confirmation_layout = QVBoxLayout()
        confirmation_layout.setContentsMargins(20, 20, 20, 20)
        confirmation_layout.setSpacing(5)

        # Wrapper for form elements
        confirmation_form_layout = QVBoxLayout()
        confirmation_form_layout.setSpacing(15)

        # "Enter confirmation code" label
        confirmation_label = QLabel("Enter confirmation code")
        confirmation_label.setStyleSheet("""
                            color: black;
                            font-size: 30px;
                            font-weight: bold;
                            font-family: Helvetica Neue;
                        """)
        confirmation_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        confirmation_form_layout.addWidget(confirmation_label)

        # Confirmation code label
        confirmation_code_label = QLabel("Confirmation code")
        confirmation_code_label.setStyleSheet("""
                            color: black;
                            font-size: 15px;
                            font-family: Helvetica Neue;
                        """)
        confirmation_code_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        confirmation_form_layout.addWidget(confirmation_code_label)

        self.confirmation_code_input = QLineEdit()
        self.confirmation_code_input.setStyleSheet(
            "border-radius: 10px; background-color: rgba(230, 226, 223, 1); border: 1px solid grey; color: black;")
        self.confirmation_code_input.setFixedSize(250, 35)
        self.confirmation_code_input.setAlignment(Qt.AlignmentFlag.AlignLeft)
        confirmation_form_layout.addWidget(self.confirmation_code_input)

        # Send button
        send_button = QPushButton("Send")
        send_button.setFixedSize(100, 35)
        send_button.setStyleSheet(
            "border-radius: 5px; background-color: rgb(80, 117, 158); border: 1px solid grey; color: white;")
        send_button.clicked.connect(lambda: self.send_confirmation_code(email))
        confirmation_form_layout.addWidget(send_button, alignment=Qt.AlignmentFlag.AlignHCenter)

        # Form container
        confirmation_form_widget = QWidget()
        confirmation_form_widget.setLayout(confirmation_form_layout)
        confirmation_layout.addWidget(confirmation_form_widget, alignment=Qt.AlignmentFlag.AlignTop)

        # Final container
        container = QWidget()
        container.setLayout(confirmation_layout)
        self.setCentralWidget(container)

    def send_signup_data(self):
        # Logic to send login info
        email = self.signup_email_input.text().strip()
        username = self.signup_username_input.text()
        password = self.signup_password_input.text()
        api_key = self.signup_apikey_input.text().strip()
        api_secret = self.signup_apisecret_input.text().strip()

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
            time.sleep(0.5)
            self.confirmation_ui(email=email)

        except ClientError as e:
            print(e.response['Error']['Message'])

    def send_confirmation_code(self, email):
        # Confirm sign-up
        confirmation_code = self.confirmation_code_input.text().strip()  # Use the correct QLineEdit instance
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
        email = self.login_email_input.text().strip()
        password = self.login_password_input.text()

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

    def get_secret_hash(self, username):
        message = username + CLIENT_ID
        dig = hmac.new(
            CLIENT_SECRET.encode('utf-8'),
            message.encode('utf-8'),
            hashlib.sha256
        ).digest()
        return base64.b64encode(dig).decode()
