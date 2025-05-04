from fastapi import Request
from sqlalchemy.orm import Session


def get_context(request: Request) -> dict[str, Request | Session]:
    # user = authenticate_user(request)
    return {"request": request, "db": request.state.db}
    # return {"request": request, "db": request.state.db, "user": user}


# OR, here Middleware no needed!
# /database.py
# @contextmanager
# def graphql_db_session():
#     db = SessionLocal()
#     try:
#         yield db
#    except Exception:
#         db.rollback()
#         raise
#     finally:
#         db.close()

# /context.py
# def get_graphql_context(request: Request):
#     return {
#         "request": request,
#         "db": graphql_db_session  # Funkcja, nie wynik
#     }

# Then in resolvers:
# class MyResolver(Mutation):
#     @staticmethod
#     def mutate(root, info):
#         with info.context["get_db"]() as db:
#             # operacje na db
#             return MyResult(...
