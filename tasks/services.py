import string
import secrets


def create_worker_secret(token_len, algorithm):
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for i in range(token_len)) + f'_{algorithm}'
