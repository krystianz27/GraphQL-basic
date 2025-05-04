from datetime import datetime, timedelta, timezone
from functools import wraps

import jwt
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from fastapi import Request
from graphql import GraphQLError  # , GraphQLResolveInfo
from sqlalchemy.orm import Session

from app.db.models import User
from app.settings.config import get_settings

settings = get_settings()
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
TOKEN_EXPIRATION = settings.token_expiration


def generate_token(email):
    expiration_time = datetime.now(timezone.utc) + timedelta(minutes=TOKEN_EXPIRATION)
    payload = {"sub": email, "exp": expiration_time}

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token


def get_authenticated_user(context) -> User | GraphQLError:
    request_object = context.get("request")
    auth_header = request_object.headers.get("Authorization")

    if not auth_header:
        raise GraphQLError("Authorization header is missing")

    parts = auth_header.split()

    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise GraphQLError(
            "Invalid authorization header format. Expected 'Bearer <token>'."
        )

    token = parts[1]

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise GraphQLError("Token has expired")
    except jwt.DecodeError:
        raise GraphQLError("Invalid token. Token format error")
    except jwt.InvalidTokenError:
        raise GraphQLError("Invalid token. Please log in again.")
    except jwt.PyJWTError:
        raise GraphQLError("Invalid token. Please log in again.")

    email = payload.get("sub")
    if not email:
        raise GraphQLError("Invalid token payload: missing subject (email).")

    db: Session = request_object.state.db
    user = db.query(User).filter(User.email == payload["sub"]).first()

    if not user:
        raise GraphQLError("User not found")

    return user


def authenticate_user(request: Request) -> User:
    auth_header = request.headers.get("Authorization")

    if not auth_header:
        raise GraphQLError("Authorization header is missing")

    parts = auth_header.split()

    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise GraphQLError(
            "Invalid authorization header format. Expected 'Bearer <token>'."
        )

    token = parts[1]

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise GraphQLError("Token has expired")
    except jwt.DecodeError:
        raise GraphQLError("Invalid token. Token format error")
    except jwt.InvalidTokenError:
        raise GraphQLError("Invalid token. Please log in again.")
    except jwt.PyJWTError:
        raise GraphQLError("Invalid token. Please log in again.")

    email = payload.get("sub")
    if not email:
        raise GraphQLError("Invalid token payload: missing subject (email).")

    db: Session = request.state.db
    user = db.query(User).filter(User.email == payload["sub"]).first()

    if not user:
        raise GraphQLError("User not found")

    return user


def hash_password(pwd):
    ph = PasswordHasher()
    return ph.hash(pwd)


def verify_password(pwd_hash, pwd):
    ph = PasswordHasher()

    try:
        ph.verify(pwd_hash, pwd)
    except VerifyMismatchError:
        raise GraphQLError("Invalid password")


def admin_user(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # info = args[1]
        # current_user = get_authenticated_user(args[1].context)
        current_user = authenticate_user(args[1].context.get("request"))
        if current_user.role != "admin":  # type: ignore
            raise GraphQLError("Only admin can perform this action")
        return func(*args, **kwargs)

    return wrapper


def auth_user(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # info = args[1]
        authenticate_user(args[1].context.get("request"))

        return func(*args, **kwargs)

    return wrapper


# def auth_user(func):
#     @wraps(func)
#     def wrapper(*args, **kwargs):
#         info = next((arg for arg in args if isinstance(arg, GraphQLResolveInfo)), None)

#         if info is None:
#             raise GraphQLError("Resolver info not found in arguments")

#         request = info.context.get("request")
#         if not request:
#             raise GraphQLError("Request not found in context")

#         authenticate_user(request)

#         return func(*args, **kwargs)

#     return wrapper


def auth_user_same_as(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        current_user = authenticate_user(args[1].context.get("request"))
        user_id = kwargs.get("user_id")

        if current_user.id != user_id:
            raise GraphQLError("You can only perform this action on your own account")
        return func(*args, **kwargs)

    return wrapper
