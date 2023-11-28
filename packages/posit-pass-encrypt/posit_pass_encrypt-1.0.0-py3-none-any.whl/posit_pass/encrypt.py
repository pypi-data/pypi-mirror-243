"""Posit encryption package"""
import os
import base64
import getpass
from getpass4 import getpass as gp4
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding


def gen_encrypted_values(pretty: bool = False) -> dict:
    """Function to request values to encrypt and load to environment variables

    Returns:
        list: db redshift username, db redshift password, s3_access_key, s3_secret_access_key, s3_session_token and decrypt key
    """
    username_redshift = input("Enter your Redshift username: ") + "\n"

    if pretty:
        password_redshift = gp4("Enter your Redshift password: ") + "\n"
    else:
        password_redshift = getpass.getpass("Enter your Redshift password: ") + "\n"

    if pretty:
        s3_access_key = gp4("Enter S3 access key: ") + "\n"
    else:
        s3_access_key = getpass.getpass("Enter S3 access key: ") + "\n"

    if pretty:
        s3_secret_access_key = gp4("Enter S3 secret access key: ") + "\n"
    else:
        s3_secret_access_key = getpass.getpass("Enter S3 secret access key: ") + "\n"

    s3_session_token = input("Enter S3 session token: ") + "\n"

    # Encryption steps
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend(),
    )

    public_key = private_key.public_key()
    padding_pkcs = padding.PKCS1v15()

    encrypted_redshift_user = public_key.encrypt(
        username_redshift.encode(), padding_pkcs
    )

    encrypted_redshift_pass = public_key.encrypt(
        password_redshift.encode(),
        padding_pkcs,
    )

    encrypted_s3_access_key = public_key.encrypt(
        s3_access_key.encode(),
        padding_pkcs,
    )

    encrypted_s3_secret_access_key = public_key.encrypt(
        s3_secret_access_key.encode(),
        padding_pkcs,
    )

    encrypted_s3_session_token = public_key.encrypt(
        s3_session_token.encode(),
        padding_pkcs,
    )

    private_key_str = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption(),
    )

    os.environ["POSIT_UTIL1"] = base64.b64encode(encrypted_redshift_user).decode()
    os.environ["POSIT_UTIL2"] = base64.b64encode(encrypted_redshift_pass).decode()
    os.environ["POSIT_UTIL3"] = base64.b64encode(encrypted_s3_access_key).decode()
    os.environ["POSIT_UTIL4"] = base64.b64encode(
        encrypted_s3_secret_access_key
    ).decode()
    os.environ["POSIT_UTIL5"] = base64.b64encode(encrypted_s3_session_token).decode()

    user_path = os.path.expanduser("~")
    with open(f"{user_path}/.util", "wb") as f:
        f.write(private_key_str[31:-30])

    print("Utility ran successfully.")
