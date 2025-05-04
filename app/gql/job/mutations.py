from graphene import Boolean, Field, Int, Mutation, String
from graphql import GraphQLError

from app.db.models import Job, JobApplication
from app.gql.types import JobApplicationObject, JobObject
from app.gql.utils import admin_user, auth_user_same_as


class AddJob(Mutation):
    class Arguments:
        title = String(required=True)
        description = String(required=True)
        employer_id = Int(required=True)

    job = Field(lambda: JobObject)

    @staticmethod
    @admin_user
    def mutate(root, info, title, description, employer_id):
        db = info.context.get("db")
        if db is None:
            raise GraphQLError("Database session not found")

        job = Job(title=title, description=description, employer_id=employer_id)
        db.add(job)
        db.commit()
        db.refresh(job)

        return AddJob(job=job)  # type: ignore


class UpdateJob(Mutation):
    class Arguments:
        id = Int(required=True)
        title = String()
        description = String()
        employer_id = Int()

    job = Field(lambda: JobObject)

    @staticmethod
    @admin_user
    def mutate(root, info, id, title, description, employer_id):
        db = info.context.get("db")
        if db is None:
            raise GraphQLError("Database session not found")

        job = db.query(Job).filter(Job.id == id).first()
        # job = (
        #     db.query(Job)
        #     .options(joinedload(Job.employer))
        #     .filter(Job.id == id)
        #     .first()
        # )
        if not job:
            raise Exception(f"Job with ID {id} not found")

        if title:
            job.title = title
        if description:
            job.description = description
        if employer_id:
            job.employer_id = employer_id

        db.commit()
        db.refresh(job)

        return UpdateJob(job=job)  # type: ignore


class DeleteJob(Mutation):
    class Arguments:
        id = Int(required=True)

    success = Boolean()

    @staticmethod
    @admin_user
    def mutate(root, info, id):
        db = info.context.get("db")
        if db is None:
            raise GraphQLError("Database session not found")

        job = db.query(Job).filter(Job.id == id).first()
        if not job:
            raise Exception(f"Job with ID {id} not found")

        db.delete(job)
        db.commit()

        return DeleteJob(success=True)  # type: ignore


class ApplyToJob(Mutation):
    class Arguments:
        job_id = Int(required=True)
        user_id = Int(required=True)

    job_application = Field(lambda: JobApplicationObject)

    @staticmethod
    @auth_user_same_as
    def mutate(root, info, job_id, user_id) -> "ApplyToJob":
        db = info.context.get("db")
        if db is None:
            raise GraphQLError("Database session not found")

        existing_application = (
            db.query(JobApplication)
            .filter(JobApplication.job_id == job_id, JobApplication.user_id == user_id)
            .first()
        )

        if existing_application:
            raise GraphQLError("You have already applied to this job")

        job_application = JobApplication(job_id=job_id, user_id=user_id)
        db.add(job_application)
        db.commit()
        db.refresh(job_application)

        return ApplyToJob(job_application=job_application)  # type: ignore
