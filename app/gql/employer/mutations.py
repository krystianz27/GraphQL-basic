from graphene import Boolean, Field, Int, Mutation, String

from app.db.models import Employer
from app.gql.types import EmployerObject
from app.gql.utils import admin_user


class AddEmployer(Mutation):
    class Arguments:
        name = String(required=True)
        contact_email = String(required=True)
        industry = String(required=True)

    employer = Field(lambda: EmployerObject)

    @staticmethod
    @admin_user
    def mutate(root, info, name, contact_email, industry):
        session = info.context.get("db")
        if not session:
            raise Exception("Database session not found")

        employer = Employer(name=name, contact_email=contact_email, industry=industry)
        session.add(employer)
        session.commit()
        session.refresh(employer)

        return AddEmployer(employer=employer)  # type: ignore


class UpdateEmployer(Mutation):
    class Arguments:
        id = Int(required=True)
        name = String()
        contact_email = String()
        industry = String()

    employer = Field(lambda: EmployerObject)

    @staticmethod
    @admin_user
    def mutate(root, info, id, name=None, contact_email=None, industry=None):
        session = info.context.get("db")
        if not session:
            raise Exception("Database session not found")

        employer = session.query(Employer).filter(Employer.id == id).first()

        if not employer:
            raise Exception(f"Employer with ID {id} not found")

        if name is not None:
            employer.name = name
        if contact_email is not None:
            employer.contact_email = contact_email
        if industry is not None:
            employer.industry = industry

        session.commit()
        session.refresh(employer)

        return UpdateEmployer(employer=employer)  # type: ignore


class DeleteEmployer(Mutation):
    class Arguments:
        id = Int(required=True)

    success = Boolean()

    @staticmethod
    @admin_user
    def mutate(root, info, id):
        session = info.context.get("db")
        if not session:
            raise Exception("Database session not found")

        employer = session.query(Employer).filter(Employer.id == id).first()

        if not employer:
            raise Exception(f"Employer with ID {id} not found")

        session.delete(employer)
        session.commit()
        return DeleteEmployer(success=True)  # type: ignore
