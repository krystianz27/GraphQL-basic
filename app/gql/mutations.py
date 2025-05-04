from graphene import ObjectType

from app.gql.employer.mutations import AddEmployer, DeleteEmployer, UpdateEmployer
from app.gql.job.mutations import AddJob, ApplyToJob, DeleteJob, UpdateJob
from app.gql.user.mutations import LoginUser, RegisterUser


class Mutation(ObjectType):
    add_job = AddJob.Field()
    update_job = UpdateJob.Field()
    delete_job = DeleteJob.Field()
    apply_to_job = ApplyToJob.Field()

    add_employer = AddEmployer.Field()
    update_employer = UpdateEmployer.Field()
    delete_employer = DeleteEmployer.Field()

    login_user = LoginUser.Field()
    register_user = RegisterUser.Field()
