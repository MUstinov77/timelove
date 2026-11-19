from datetime import datetime, timedelta, timezone
from uuid import UUID, uuid7

import jwt
from jwt.exceptions import DecodeError, ExpiredSignatureError, InvalidTokenError

from backend.app.core.configuration import get_settings
from backend.app.schema.auth import AccessTokenPayload

settings = get_settings()


class JWTService:

    def __init__(self):
        self.settings = get_settings()
        self.access_token_expire_minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES
        self.auth_secret_key = settings.AUTH_SECRET_KEY
        self.algorithm = settings.JWT_ALGORITHM
        self.token_expire_hours = settings.TOKEN_EXPIRE_HOURS
        self.jwt_issuer = settings.JWT_ISSUER

    def create_and_encode_access_token(self, user_id: UUID):
        now = datetime.now(timezone.utc)
        token_payload = {
            "iss": self.jwt_issuer,
            "iat": now,
            "exp": now + timedelta(minutes=self.access_token_expire_minutes),
            "sub": str(user_id),
            "jti": str(uuid7()),
            "token_type": "access"
        }

        token = jwt.encode(
            token_payload,
            self.auth_secret_key,
            algorithm=self.algorithm
        )
        return token

    def decode_access_token(self, token: str):
        try:
            decoded_payload = jwt.decode(
                token,
                self.auth_secret_key,
                algorithms=[self.algorithm],
                issuer=self.jwt_issuer,
                options={
                    "require": [
                        "iss",
                        "sub",
                        "jti",
                        "iat",
                        "exp",
                        "token_type"
                    ]
                }
            )
            return AccessTokenPayload.model_validate(decoded_payload)

        except TypeError:
            raise ValueError("Wrong payload fields types")
        except ExpiredSignatureError:
            raise ValueError("Token expired")
        except DecodeError:
            raise ValueError("Token decode error")
        except InvalidTokenError:
            raise ValueError("Invalid token")
