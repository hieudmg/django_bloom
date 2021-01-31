from cryptography.fernet import Fernet
from django_bloom.secrets import SECRET_KEY
import base64

fernet = Fernet(base64.urlsafe_b64encode(SECRET_KEY.encode()[:32]))


def encrypt(message: str) -> str:
    try:
        return base64.urlsafe_b64encode(fernet.encrypt(message.encode())).decode()
    except:
        return ''


def decrypt(token: str) -> str:
    try:
        return fernet.decrypt(base64.urlsafe_b64decode(token.encode())).decode()
    except:
        return ''
