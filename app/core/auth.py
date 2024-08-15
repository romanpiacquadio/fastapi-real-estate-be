from __future__ import annotations
import uuid

from datetime import datetime, timedelta
from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.core.dependencies import get_db
from app.apis.models.entities import User as UserModel

from app.core import config


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class User(BaseModel):
    name: str
    email: str    


class UserCreate(User):
    password: str


class UserInDB(User):
    hashed_password: str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")
router = APIRouter()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

fake_users_db = {
    "ubuntu": {
        "username": config.API_USERNAME,
        "hashed_password": get_password_hash(config.API_PASSWORD),
    }
}

def get_user(db: dict[str, dict[str, dict]], username: str | None) -> UserInDB | None:
    if username not in db:
        return None
    user_dict = db[username]
    return UserInDB(**user_dict)


def authenticate_user(
    fake_db: dict[str, dict[str, dict]],
    username: str,
    password: str,
) -> bool | UserInDB:
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        config.API_SECRET_KEY,
        algorithm=config.API_ALGORITHM,
    )
    return encoded_jwt


def get_current_user(token: str = Depends(oauth2_scheme)) -> UserInDB:
    credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token,
            config.API_SECRET_KEY,
            algorithms=[config.API_ALGORITHM],
        )
        username = payload.get("sub")

        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)

    except JWTError:
        raise credentials_exception

    user = get_user(fake_users_db, username=token_data.username)

    if user is None:
        raise credentials_exception
    return user


@router.post('/register', response_model=User, status_code=status.HTTP_201_CREATED )
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    # Verifica si el nombre de usuario ya existe
    db_user = db.query(UserModel).filter(UserModel.email == user.email).first() # resultado = existeUsuario(user.email)

    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    
    # Crear una instancia del modelo User
    new_user = UserModel(
        name=user.name,
        email=user.email,
        password=get_password_hash(user.password),  # Hashear la contraseña
    ) # new_user = crearUsuario(user)

    try:
        # Agregar el nuevo usuario a la base de datos
        presist_user_db(user)
        # db.add(new_user)
        # db.commit()
        # db.refresh(new_user)
    except Exception as e:
        print('e', e)
        # db.rollback()  # Deshacer cualquier cambio si ocurre un error
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error saving user to the database")
    
    return new_user     


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> dict[str, str]:
    user = authenticate_user(
        fake_users_db,
        form_data.username,
        form_data.password,
    )

    if not user:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(
        seconds=config.API_ACCESS_TOKEN_EXPIRE_MINUTES,
    )
    access_token = create_access_token(
        data={"sub": user.username},  # type: ignore
        expires_delta=access_token_expires,
    )
    return {"access_token": access_token, "token_type": "bearer"}
