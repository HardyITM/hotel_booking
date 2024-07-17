from sqladmin import Admin
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from starlette.responses import RedirectResponse

from app.config import settings as s
from app.exceptions import InvalidEmailOrPasswordException
from app.users.auth import authenticate_user, create_access_token
from app.users.dependencies import get_current_user


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        login, password = form["username"], form["password"]

        if login == s.ADM_LOGIN and password == s.ADM_PASSWORD:
            request.session.update({'pass': password, 'login': login})
            return True

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        password = request.session.get("pass")
        login = request.session.get("login")
        
        if not login and not password:
            return RedirectResponse(request.url_for("admin:login"), status_code=302)
        if password != s.ADM_PASSWORD or login != s.ADM_LOGIN:
            return RedirectResponse(request.url_for("admin:login"), status_code=302)
        
        return True


authentication_backend = AdminAuth(secret_key=s.SECRET_KEY)