import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from urllib.parse import parse_qs

User = get_user_model()

class JwtAuthMiddleware:
    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        query_string = scope.get("query_string", b"").decode()
        query_params = parse_qs(query_string)

        token = None
        if "token" in query_params:
            token = query_params["token"][0]

        scope["user"] = None

        if token:
            try:
                UntypedToken(token)
                decoded = jwt.decode(
                    token,
                    settings.SECRET_KEY,
                    algorithms=["HS256"],
                )
                user_id = decoded.get("user_id")
                scope["user"] = await self.get_user(user_id)
            except (InvalidToken, TokenError, jwt.DecodeError):
                scope["user"] = None

        return await self.inner(scope, receive, send)

    @staticmethod
    async def get_user(user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None
