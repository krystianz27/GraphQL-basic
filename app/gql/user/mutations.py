from graphene import Field, Mutation, String
from graphql import GraphQLError
from sqlalchemy import exists

from app.db.models import User
from app.gql.types import UserObject
from app.gql.utils import (
    authenticate_user,
    generate_token,
    hash_password,
    verify_password,
)


# Uses info.context.get("db") to get the database session
class LoginUser(Mutation):
    class Arguments:
        email = String(required=True)
        password = String(required=True)

    token = String()

    @staticmethod
    def mutate(root, info, email, password):
        # db = info.context.get("db")
        db = info.context["db"]

        if db is None:
            raise GraphQLError("Database session not found")

        user = db.query(User).filter(User.email == email).first()

        if not user:
            raise GraphQLError("User not found")

        verify_password(user.password_hash, password)

        token = generate_token(email)

        return LoginUser(token=token)  # type: ignore


class RegisterUser(Mutation):
    class Arguments:
        username = String(required=True)
        email = String(required=True)
        password = String(required=True)
        role = String(required=True)

    user = Field(lambda: UserObject)

    @staticmethod
    def mutate(root, info, username, email, password, role):
        db = info.context.get("db")
        if db is None:
            raise GraphQLError("Database session not found")

        if role == "admin":
            current_user = authenticate_user(info.context.get("request"))
            if current_user.role != "admin":  # type: ignore
                raise GraphQLError("Only admin can create an admin user")

        user_exists = db.query(exists().where(User.email == email)).scalar()

        if user_exists:
            raise GraphQLError("User already exists with this email")

        user = User(
            username=username,
            email=email,
            password_hash=hash_password(password),
            role=role,
        )
        db.add(user)
        db.commit()
        db.refresh(user)

        return RegisterUser(user=user)  # type: ignore
