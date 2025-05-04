from fastapi import Request

# from fastapi.middleware import BaseHTTPMiddleware
# from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from app.db.database import db_session

# from starlette.requests import Request as StarletteRequest
# from starlette.types import ASGIApp, Receive, Scope, Send


class DBSessionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path.startswith("/graphql") or request.url.path.startswith(
            "/playground"
        ):
            db_generator = db_session()
            try:
                db = next(db_generator)
                request.state.db = db
                response = await call_next(request)
            finally:
                try:
                    next(
                        db_generator
                    )  # Execute finally in db_session() to close session
                except StopIteration:
                    pass  # Expected Generator Behavior
            return response
        return await call_next(request)


# class DBSessionMiddleware(BaseHTTPMiddleware):
#     async def dispatch(self, request: Request, call_next):
#         if request.url.path.startswith("/graphql"):
#             request.state.get_db = SessionLocal  # Przekazujemy klasę, nie instancję!
#             response = await call_next(request)
#             return response
#         return await call_next(request)
# # Then in resolvers:
#
#         # Ręczne zarządzanie sesją
#         db: Session = info.context["get_db"]()
# try:
#      ...
# finally:
#      db.close()


# OR


# class DBSessionMiddleware(BaseHTTPMiddleware):
#     async def dispatch(self, request: Request, call_next):
#         if request.url.path.startswith("/graphql"):
#             with SessionLocal() as db:  # Użyj contextmanager bezpośrednio
#                 request.state.db = db
#                 response = await call_next(request)

#             return response
#         return await call_next(request)


# ANOTHER VERSION


# here Middleware no needed!
# /database.py
# @contextmanager
# def graphql_db_session():
#     db = SessionLocal()
#     try:
#         yield db
#    except Exception as e:
#         db.rollback()
#         raise GraphQLError(f"Database error: {str(e)}")
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
#           with info.context["get_db"]() as db:
#               user = db.query(User).get(user_id)
#               if not user:
#                   raise GraphQLError("User not found")
#               user.name = "Updated Name"
#               return UpdateUser(success=True).
