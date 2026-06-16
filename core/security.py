from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
from core import settings

# --- Hashing de Senha ---
# Forçando o uso do bcrypt interno do passlib se o bcrypt da biblioteca externa falhar
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    # O bcrypt tem um limite estrito de 72 bytes.
    # Garantimos que a string não ultrapasse esse limite codificando para utf-8 e limitando.
    # Em um cenário real, você deveria validar o tamanho máximo da senha no frontend e no schema.
    truncated_password = password.encode('utf-8')[:72].decode('utf-8', 'ignore')
    return pwd_context.hash(truncated_password)

# --- Token JWT ---
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None
