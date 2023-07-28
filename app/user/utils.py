"""
Helper functions for user.
"""

import random
from passlib.context import CryptContext

PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    """Hashes a password using bcrypt encryption algorithm.

    Args:
        password (str): The password to hash.

    Returns:
        str: The hashed password.
    """
    return PWD_CONTEXT.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a plain password against a hashed password using bcrypt.

    Args:
        plain_password (str): The plain password to verify.
        hashed_password (str): The hashed password to verify against.

    Returns:
        bool: True if the passwords match, False otherwise.
    """
    return PWD_CONTEXT.verify(plain_password, hashed_password)


def generate_name() -> str:
    """Generates a random name by reading from a list of names.

    Returns:
        str: The randomly generated name.
    """
    with open("core/storage/names.txt", "r", encoding="utf-8") as names_file:
        names = names_file.read().split("\n")

    return random.choice(names)
