from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from base64 import b64encode, b64decode

from core.config import config


# Seems like this will not be needed anytime soon
# But we'll keep it here just in case


# class Encryption:
#     def __init__(self) -> None:
#         self.password = config.PRIVATE_KEY_PASSWORD.encode('utf-8')

#         try:
#             self.private_key = self._read()

#         except FileNotFoundError as e:
#             # Log this, "new key generated"
#             self.private_key = self._generate()

#         self.public_key = self.private_key.public_key()


#     def encrypt(self, str):
#         """Expects normal python string, returns base64 encoded string"""
#         message = str.encode('utf-8')

#         encrypted = self.public_key.encrypt(
#             message,
#             padding.OAEP(
#                 mgf=padding.MGF1(algorithm=hashes.SHA256()),
#                 algorithm=hashes.SHA256(),
#                 label=None
#             )
#         )

#         message_encrypted = b64encode(encrypted)
#         return message_encrypted.decode('utf-8')

#     def decrypt(self, str):
#         """Expects base64 encoded string, returns normal python string"""
#         encrypted = b64decode(str)
        

#         decrypted = self.private_key.decrypt(
#             encrypted,
#             padding.OAEP(
#                 mgf=padding.MGF1(algorithm=hashes.SHA256()),
#                 algorithm=hashes.SHA256(),
#                 label=None
#             )
#         )
#         return decrypted.decode('utf-8')
    
#     def get_public_key(self):
#         pem = self.public_key.public_bytes(
#             encoding=serialization.Encoding.PEM,
#             format=serialization.PublicFormat.SubjectPublicKeyInfo
#         )
#         return pem


#     def _read(self):
#         with open("private_key.pem", "rb") as key_file:
#             private_key = serialization.load_pem_private_key(
#                 key_file.read(),
#                 password=self.password,
#                 backend=default_backend()
#             )

#         return private_key

#     def _generate(self):
#         private_key = rsa.generate_private_key(
#             public_exponent=65537,
#             key_size=2048,
#             backend=default_backend()
#         )

#         pem = private_key.private_bytes(
#             encoding=serialization.Encoding.PEM,
#             format=serialization.PrivateFormat.PKCS8,
#             encryption_algorithm=serialization.BestAvailableEncryption(self.password)
#         )

#         with open('private_key.pem', 'wb') as f:
#             f.write(pem)

#         return private_key
