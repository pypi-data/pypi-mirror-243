"""  """
import os
import base64
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import padding

HOME = os.environ["HOME"]


def __get_decrypt_key():
    decrypt_key = os.environ.get("POSIT_UTIL6", False)

    if not decrypt_key:
        try:
            with open(f"{HOME}/.util", "rb") as key_file:
                key = key_file.read()
                key = key.decode()

        except FileNotFoundError as e:
            print(f"{e} - Run . ./posit-util and set your credentials first.")

        one = base64.b64decode("LS0tLS1CRUdJTiBSU0EgUFJJVkFURSBLRVktLS0tLQo=").decode()
        two = base64.b64decode("LS0tLS1FTkQgUlNBIFBSSVZBVEUgS0VZLS0tLS0=").decode()
        key_string = one + key + two

        decrypt_key = serialization.load_pem_private_key(
            key_string.encode(), password=None, backend=default_backend()
        )

    return decrypt_key


def get_decrypted_redshift_values(
    db_username: str = "",
    db_password: str = "",
    decryptkey: str = "",
) -> dict:
    """Function to load environment variables to decrypt
       db username and password

    Raises:
        Exception: If environment variables are not present an
        exception is raised

    Returns:
        list: db redshift username and db redshift password
    """
    if db_username != "":
        envar_db_user = db_username
    elif "POSIT_UTIL1" in os.environ:
        envar_db_user = base64.b64decode(os.environ["POSIT_UTIL1"])
    else:
        raise Exception("Missing POSIT_UTIL1 environment variable")

    if db_password != "":
        envar_db_pass = db_password
    elif "POSIT_UTIL2" in os.environ:
        envar_db_pass = base64.b64decode(os.environ["POSIT_UTIL2"])
    else:
        raise Exception("Missing POSIT_UTIL2 environment variable")

    if decryptkey != "":
        decrypt_key = decryptkey
    else:
        decrypt_key = __get_decrypt_key()

    dec_db_user = decrypt_key.decrypt(envar_db_user, padding.PKCS1v15())[:-1].decode()
    dec_db_pass = decrypt_key.decrypt(envar_db_pass, padding.PKCS1v15())[:-1].decode()

    decrypted_db_data = {"db_user": dec_db_user, "db_pass": dec_db_pass}
    return decrypted_db_data


def get_decrypted_s3_values(
    access_key: str = "",
    secret_access_key: str = "",
    session_token: str = "",
    decryptkey: str = "",
) -> dict:
    """Function to load environment variables to decrypt
       db username and password

    Raises:
        Exception: If environment variables are not present an
        exception is raised

    Returns:
        dict:
    """

    if access_key != "":
        envar_access_key = access_key
    elif "POSIT_UTIL3" in os.environ:
        envar_access_key = base64.b64decode(os.environ["POSIT_UTIL3"])
    else:
        raise Exception("Missing POSIT_UTIL3 environment variable")

    if secret_access_key != "":
        envar_secret_access_key = secret_access_key
    elif "POSIT_UTIL4" in os.environ:
        envar_secret_access_key = base64.b64decode(os.environ["POSIT_UTIL4"])
    else:
        raise Exception("Missing POSIT_UTIL4 environment variable")

    if session_token != "":
        envar_session_token = session_token
    elif "POSIT_UTIL5" in os.environ:
        envar_session_token = base64.b64decode(os.environ["POSIT_UTIL5"])
    else:
        raise Exception("Missing POSIT_UTIL5 environment variable")

    if decryptkey != "":
        decrypt_key = decryptkey
    else:
        decrypt_key = __get_decrypt_key()

    dec_access_key = decrypt_key.decrypt(envar_access_key, padding.PKCS1v15())[
        :-1
    ].decode()
    dec_secret_access_key = decrypt_key.decrypt(
        envar_secret_access_key, padding.PKCS1v15()
    )[:-1].decode()
    dec_session_token = decrypt_key.decrypt(envar_session_token, padding.PKCS1v15())[
        :-1
    ].decode()

    decrypted_s3_data = {
        "access_key": dec_access_key,
        "secret_access_key": dec_secret_access_key,
        "session_token": dec_session_token,
    }
    return decrypted_s3_data


def get_all_decrypted_values(
    db_username: str = "",
    db_password: str = "",
    access_key: str = "",
    secret_access_key: str = "",
    session_token: str = "",
    decryptkey: str = "",
) -> dict:
    """_summary_

    Args:
        db_username (str, optional): _description_. Defaults to "".
        db_password (str, optional): _description_. Defaults to "".
        access_key (str, optional): _description_. Defaults to "".
        secret_access_key (str, optional): _description_. Defaults to "".
        session_token (str, optional): _description_. Defaults to "".
        decryptkey (str, optional): _description_. Defaults to "".

    Returns:
        dict: _description_
    """
    db_dict = get_decrypted_redshift_values(
        db_username,
        db_password,
        decryptkey,
    )
    s3_dict = get_decrypted_s3_values(
        access_key,
        secret_access_key,
        session_token,
        decryptkey,
    )
    all_dict = db_dict.copy()
    for key, val in s3_dict.items():
        all_dict[key] = val

    return all_dict
