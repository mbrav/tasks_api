from app import db, models, schemas
from app.config import settings
from app.services import AuthService
from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session

auth_service = AuthService(
    secret=settings.SECRET_KEY,
    algorithm=settings.CRYPT_ALGORITHM,
    expire=settings.TOKEN_EXPIRE_MINUTES)


async def get_auth_user(
    db_session: Session = Depends(db.get_database),
    token: str = Depends(auth_service.oauth2_scheme)
) -> models.User:
    """Get user object based on provided credentials from database"""

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'})

    try:
        payload = jwt.decode(token, auth_service.SECRET_KEY,
                             algorithms=[auth_service.CRYPT_ALGORITHM])
        username: str = payload.get('sub')
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except (JWTError, ValidationError):
        raise credentials_exception

    user = auth_service.get_user(
        db_session=db_session,
        username=token_data.username)
    if user is None:
        raise HTTPException(
            status_code=404, detail=f"User '{token_data.username}' not found")
    return user


async def get_active_user(
    current_user: models.User = Depends(get_auth_user)
) -> models.User:
    """Check if user is active"""

    if current_user.is_active is False:
        raise HTTPException(status_code=400, detail='Inactive user')
    return current_user


async def get_active_superuser(
    current_user: models.User = Depends(get_auth_user),
) -> models.User:
    """Check if user is supperuser"""
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return current_user
