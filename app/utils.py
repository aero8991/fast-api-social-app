from passlib.context import CryptContext


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def bcrypt_hash(password: str):
    return pwd_context.hash(password)

def verify_password(plain_passowrd, hash_password):
    return pwd_context.verify(plain_passowrd, hash_password)