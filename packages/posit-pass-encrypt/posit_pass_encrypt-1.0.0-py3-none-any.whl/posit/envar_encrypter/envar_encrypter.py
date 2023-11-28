"""Posit decryption utility"""
import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
import getpass
from getpass4 import getpass as gp4


def gen_encrypted_values(pretty: bool = False):
    """Function to request values to encrypt and load to environment variables

    Returns:
        list: db redshift username, db redshift password, s3_access_key, s3_secret_access_key, s3_session_token and decrypt key
    """
    username_redshift = input("Enter your Redshift username: ")

    if pretty:
        password_redshift = gp4("Enter your Redshift password: ")
    else:
        password_redshift = getpass.getpass("Enter your Redshift password: ")

    if pretty:
        s3_access_key = gp4("Enter S3 access key: ")
    else:
        s3_access_key = getpass.getpass("Enter S3 access key: ")

    if pretty:
        s3_secret_access_key = gp4("Enter S3 secret access key: ")
    else:
        s3_secret_access_key = getpass.getpass("Enter S3 secret access key: ")

    s3_session_token = input("Enter S3 session token: ")

    # Encryption steps
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend(),
    )

    public_key = private_key.public_key()
    padding_oaep = padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None,
    )

    encrypted_redshift_user = public_key.encrypt(
        username_redshift.encode(), padding_oaep
    )

    encrypted_redshift_pass = public_key.encrypt(
        password_redshift.encode(),
        padding_oaep,
    )

    encrypted_s3_access_key = public_key.encrypt(
        s3_access_key.encode(),
        padding_oaep,
    )

    encrypted_s3_secret_access_key = public_key.encrypt(
        s3_secret_access_key.encode(),
        padding_oaep,
    )

    private_key_str = str(
        private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        )
    )

    os.environ["POSIT_UTIL1"] = encrypted_redshift_user.hex()
    os.environ["POSIT_UTIL2"] = encrypted_redshift_pass.hex()
    os.environ["POSIT_UTIL3"] = encrypted_s3_access_key.hex()
    os.environ["POSIT_UTIL4"] = encrypted_s3_secret_access_key.hex()
    os.environ["POSIT_UTIL5"] = s3_session_token

    user_path = os.path.expanduser("~")
    print(user_path)
    with open(f"{user_path}/.util", "w") as f:
        f.write(private_key_str[31:-30])

    # encrypted_data = {
    #     "db_user": encrypted_redshift_user.hex(),
    #     "db_password": encrypted_redshift_pass.hex(),
    #     "s3_access_key": encrypted_s3_access_key.hex(),
    #     "s3_secret_access_key": encrypted_s3_secret_access_key.hex(),
    #     "s3_session_token": s3_session_token,
    #     "decryptkey": private_key_str[31:-30]
    # }
