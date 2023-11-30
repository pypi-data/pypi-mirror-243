from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from aurori.users import userManager
from aurori.config import config_manager
from .typemodels import Token, TokenData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token", auto_error=False)


async def get_manadatory_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    secret = config_manager.config["SECURITY"]["secret_key"]
    algorithm = config_manager.config["SECURITY"]["jwt_algorithm"]

    try:
        payload = jwt.decode(token, secret, algorithms=[algorithm])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except jwt.PyJWTError:
        raise credentials_exception
    user = userManager.getUser(
        token_data.username
    )  # get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_optional_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    secret = config_manager.config["SECURITY"]["secret_key"]
    algorithm = config_manager.config["SECURITY"]["jwt_algorithm"]

    try:
        payload = jwt.decode(token, secret, algorithms=[algorithm])
        username: str = payload.get("sub")
        if username is None:
            token_data = None
        else:
            token_data = TokenData(username=username)
    except jwt.PyJWTError:
        token_data = None
    if token_data is not None:
        user = userManager.getUser(
            token_data.username
        )  # get_user(fake_users_db, username=token_data.username)
        return user
    return None
