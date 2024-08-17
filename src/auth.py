import os
import json
from typing import Optional
from typing_extensions import Annotated

from fastapi import HTTPException, status, Request

import strawberry
from strawberry.permission import BasePermission

import firebase_admin
from firebase_admin import credentials
from firebase_admin.auth import verify_id_token


GOOGLE_APPLICATION_CREDENTIALS_JSON = os.getenv("GOOGLE_APPLICATION_CREDENTIALS_JSON")
if not GOOGLE_APPLICATION_CREDENTIALS_JSON:
    raise EnvironmentError("GOOGLE_APPLICATION_CREDENTIALS_JSON environment variable not set")

cred_data = json.loads(GOOGLE_APPLICATION_CREDENTIALS_JSON)
cred = credentials.Certificate(cred_data)
firebase_admin.initialize_app(cred)


class IsAuthenticated(BasePermission):
    message = "Not logged in or Invalid credentials"

    def has_permission(self, source, info: strawberry.Info, **kwargs) -> bool:
        request: Request = info.context["request"]
        authorization: str = request.headers.get("Authorization")

        if authorization:
            scheme, _, token = authorization.partition(" ")
            if scheme.lower() == "bearer":
                try:
                    # TESTING PURPOSES
                    # CASE IN WHICH THE TOKEN IS VALID
                    if token == "TEST": return True
                    # REMOVE IN PRODUCTION
                    print(token)
                    verified_user = verify_id_token(id_token=token)
                    info.context["user"] = verified_user
                    return True
                except HTTPException:
                    return False
                except Exception:
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Not logged in or Invalid credentials",
                        headers={"WWW-Authenticate": "Bearer"},
                    )
        return False
