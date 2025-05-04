# from fastapi import Request
# from starlette.middleware.base import BaseHTTPMiddleware

# from app.db.database import SessionLocal
# from app.db.models import User


# class UserMiddleware(BaseHTTPMiddleware):
#     async def dispatch(self, request: Request, call_next):
#         if request.url.path.startswith("/graphql"):
#             # Tymczasowa sesja tylko do pobrania użytkownika
#             with SessionLocal() as temp_db:
#                 user = (
#                     temp_db.query(User)
#                     .filter_by(token=request.headers.get("Authorization"))
#                     .first()
#                 )
#                 request.state.user = user  # Dodaj użytkownika do request

#             # Przekazujemy tylko fabrykę sesji do resolverów
#             request.state.get_db = SessionLocal
#             response = await call_next(request)
#             return response
#         return await call_next(request)

#

# OR

# database.py
# from fastapi import Depends
# from sqlalchemy.orm import Session

# def get_db() -> Generator[Session, None, None]:
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# # context.py (dla Graphene)
# def get_graphql_context(request: Request):
#     return {
#         "request": request,
#         "db_gen": get_db()  # Przekazujemy generator, nie sesję!
#     }

# # W resolverze:
# db = next(info.context["db_gen"])  # Pobierz sesję z generatora
# try:
#     user = db.query(User).get(user_id)
# finally:
#     next(info.context["db_gen"], None)  # Wymuś zamknięcie (wejście do finally)
