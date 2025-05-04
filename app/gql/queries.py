from graphene import Field, Int, List, ObjectType
from sqlalchemy.orm import joinedload

from app.db.models import Employer, Job, JobApplication, User
from app.gql.types import EmployerObject, JobApplicationObject, JobObject, UserObject


class Query(ObjectType):
    jobs = List(JobObject)
    job = Field(JobObject, id=Int(required=True))
    employers = List(EmployerObject)
    employer = Field(EmployerObject, id=Int(required=True))
    users = List(UserObject)
    user = Field(UserObject, id=Int(required=True))
    job_applications = List(JobApplicationObject)

    @staticmethod
    def resolve_job(root, info, id):
        session = info.context.get("db")
        return session.query(Job).filter(Job.id == id).first()

    @staticmethod
    def resolve_jobs(root, info):
        session = info.context.get("db")
        return session.query(Job).options(joinedload(Job.employer)).all()

    @staticmethod
    def resolve_employers(root, info):
        session = info.context.get("db")
        return session.query(Employer).all()

    @staticmethod
    def resolve_employer(root, info, id):
        session = info.context.get("db")
        return session.query(Employer).filter(Employer.id == id).first()

    @staticmethod
    def resolve_users(root, info):
        session = info.context.get("db")
        return session.query(User).all()

    @staticmethod
    def resolve_user(root, info, id):
        session = info.context.get("db")
        return session.query(User).filter(User.id == id).first()

    @staticmethod
    def resolve_job_applications(root, info):
        session = info.context.get("db")
        return session.query(JobApplication).all()
