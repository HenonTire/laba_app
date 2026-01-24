# chat/middleware.py
from urllib.parse import parse_qs
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from channels.db import database_sync_to_async
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from django.conf import settings
import jwt

User = get_user_model()


class JwtAuthMiddleware:
    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        query_string = scope["query_string"].decode()
        params = parse_qs(query_string)

        token = params.get("token")
        if not token:
            scope["user"] = AnonymousUser()
            return await self.inner(scope, receive, send)

        token = token[0]

        try:
            # Validate token signature & expiry
            UntypedToken(token)

            decoded = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=["HS256"],
            )

            user_id = decoded.get("user_id")
            if not user_id:
                scope["user"] = AnonymousUser()
            else:
                scope["user"] = await self.get_user(user_id)

        except (InvalidToken, TokenError, jwt.PyJWTError) as e:
            print("❌ JWT WS auth failed:", str(e))
            scope["user"] = AnonymousUser()

        return await self.inner(scope, receive, send)

    @database_sync_to_async
    def get_user(self, user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return AnonymousUser()
