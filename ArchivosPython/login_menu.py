import boto3
import hmac
import hashlib
import base64
import tkinter as tk
import os
from time import sleep

AWS_REGION = os.getenv('AWS_REGION')
USER_POOL_ID = os.getenv('USER_POOL_ID')
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')

# Initialize Cognito client
client = boto3.client('cognito-idp', region_name=AWS_REGION)

def get_secret_hash(username):
    message = username + CLIENT_ID
    dig = hmac.new(
        CLIENT_SECRET.encode('utf-8'),
        message.encode('utf-8'),
        hashlib.sha256
    ).digest()
    return base64.b64encode(dig).decode()

def sign_up(username, password, user_entered_username, api_key, api_secret):
 # --- Now call sign_up ---
    response = client.sign_up(
        ClientId=CLIENT_ID,
        Username=username,  # This is the email, used as the 'Username'
        Password=password,
        SecretHash=get_secret_hash(username),
        UserAttributes=[
            {'Name': 'email', 'Value': username.strip()},  # Use 'email' as the Username
            {'Name': 'custom:Username', 'Value': user_entered_username},  # Store the custom username here
            {'Name': 'custom:ApiKey', 'Value': api_key.strip()},
            {'Name': 'custom:ApiSecret', 'Value': api_secret.strip()},
        ]
    )
    print("Sign-up successful!")

def confirm_sign_up(username,confirmation_code):
    # Confirm sign-up
    response = client.confirm_sign_up(
        ClientId=CLIENT_ID,
        Username=username,
        ConfirmationCode= confirmation_code,
        SecretHash=get_secret_hash(username),
    )

    print(response)

def sign_in(username, password):
    # Call Cognito to authenticate
    try:
        response = client.initiate_auth(
            ClientId=CLIENT_ID,
            AuthFlow='USER_PASSWORD_AUTH',
            AuthParameters={
                'USERNAME': username,
                'PASSWORD': password,
                'SECRET_HASH': get_secret_hash(username)
            }
        )
        print("Authentication successful!")
        print(response['AuthenticationResult'])  # contains IdToken, AccessToken, RefreshToken

    except client.exceptions.NotAuthorizedException:
        print("Incorrect username or password.")
    except client.exceptions.UserNotConfirmedException:
        print("User is not confirmed.")
    except Exception as e:
        print(f"An error occurred: {e}")

# GUI Creation

def show_frame(frame):
    frame.tkraise()

root = tk.Tk()
root.geometry("400x300")

# Configure the grid
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)

main_frame = tk.Frame(root, background='#ffffff')
login_frame = tk.Frame(root, background='#ffffff')
signup_frame = tk.Frame(root, background='#ffffff')
confirmation_frame = tk.Frame(root, background='#ffffff')

for frame in (login_frame, signup_frame, main_frame, confirmation_frame):
    frame.grid(row=0, column=0, sticky="nsew")

tk.Button(main_frame, text="Go to Sign Up", command=lambda: show_frame(signup_frame)).pack(pady=10)
tk.Button(main_frame, text="Go to Log in", command=lambda: show_frame(login_frame)).pack()

# Build login frame
#Email
tk.Label(login_frame, text="Email", font=("Helvetica", 16)).pack(pady=10)
email = tk.Entry(login_frame, width=30)
email.pack(pady=10)

#Password
tk.Label(login_frame, text="Password", font=("Helvetica", 16)).pack(pady=10)
password = tk.Entry(login_frame, width=30)
password.pack(pady=10)

tk.Button(login_frame, text="Log In", command=lambda: sign_in(email.get(), password.get())).pack(pady=10)

# Build signup frame
#Email
tk.Label(signup_frame, text="Email", font=("Helvetica", 16)).pack(pady=10)
email = tk.Entry(signup_frame, width=30)
email.pack(pady=10)

#Password
tk.Label(signup_frame, text="Password", font=("Helvetica", 16)).pack(pady=10)
password = tk.Entry(signup_frame, width=30)
password.pack(pady=10)

#Username
tk.Label(signup_frame, text="Username", font=("Helvetica", 16)).pack(pady=10)
username = tk.Entry(signup_frame, width=30)
username.pack(pady=10)

#API Key
tk.Label(signup_frame, text="Api key", font=("Helvetica", 16)).pack(pady=10)
api_key = tk.Entry(signup_frame, width=30)
api_key.pack(pady=10)

#API Secret
tk.Label(signup_frame, text="Api secret", font=("Helvetica", 16)).pack(pady=10)
api_secret = tk.Entry(signup_frame, width=30)
api_secret.pack(pady=10)

#Sign up button
tk.Button(
    signup_frame,
    text="Sign up",
    command=lambda: [sign_up(email.get(), password.get(), username.get(), api_key.get(), api_secret.get()), show_frame(confirmation_frame)]
).pack(pady=10)
sleep(1.5)

#Confirmation code
tk.Label(confirmation_frame, text="Confirmation code", font=("Helvetica", 16)).pack(pady=10)
confirmation_code = tk.Entry(confirmation_frame, width=30)
confirmation_code.pack(pady=10)
tk.Button(confirmation_frame, text="Confirm", command=lambda: confirm_sign_up(email.get(), confirmation_code.get())).pack(pady=10)


#Back button
for frame in (login_frame, signup_frame):
    tk.Button(frame, text="Back", command=lambda: show_frame(main_frame)).pack()

# Start with login
show_frame(main_frame)

root.mainloop()
