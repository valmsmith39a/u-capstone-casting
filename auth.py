import json
from flask import request, _request_ctx_stack
from functools import wraps
from jose import jwt
from urllib.request import urlopen

AUTH0_DOMAIN = "dev-waoix1p9.us.auth0.com"
ALGORITHMS = ["RS256"]
API_AUDIENCE = "casting"


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


def get_token_auth_header():

    if "Authorization" not in request.headers:
        # 401 unauthorized
        raise AuthError(
            {"code": "invalid_header", "description": "Invalid header"}, 401)

    auth_header = request.headers["Authorization"]
    header_parts = auth_header.split(" ")

    if len(header_parts) != 2:
        raise AuthError(
            {"code": "invalid_header", "description": "Invalid header"}, 401)

    elif header_parts[0].lower() != "bearer":
        raise AuthError(
            {"code": "invalid_header", "description": "Invalid header"}, 401)

    return header_parts[1]


def check_permissions(permission, payload):
    if "permissions" not in payload:
        raise AuthError(
            {"code": "unauthorized", "description": "Permissions field not found"},
            401
        )

    permissions = [permission.strip() for permission in payload["permissions"]]

    if permission not in permissions:
        raise AuthError({"code": "unauthorized", "description": "User permission not found in permissions"
                         }, 401)

    return True


def verify_decode_jwt(token):

    # get public key from Auth0
    jsonurl = urlopen(f"https://{AUTH0_DOMAIN}/.well-known/jwks.json")

    # get JSON Web Key Set
    # https://auth0.com/docs/tokens/json-web-tokens/json-web-key-sets
    jwks = json.loads(jsonurl.read())

    # get headr from token
    unverified_header = jwt.get_unverified_header(token)

    # find a key object with a key id (kid) that matches the key id in unverified_header

    rsa_key = {}

    if "kid" not in unverified_header:
        raise AuthError(
            {"Code": "invalid_header", "description": "Authorization malformed."}
        )

    for key in jwks["keys"]:
        if key["kid"] == unverified_header["kid"]:
            rsa_key = {
                "kty": key["kty"],
                "kid": key["kid"],
                "use": key["use"],
                "n": key["n"],
                "e": key["e"]
            }

    if rsa_key:
        try:
            # validate JWT using the key
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer="https://" + AUTH0_DOMAIN + "/"
            )

            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError(
                {"code": "token_expired", "descriptions": "Token expired."}, 401)

        except jwt.JWTClaimsError:
            raise AuthError(
                {
                    "code": "invalid_claims",
                    "descriptions": "Incorrect claims. Please check the audience and issuer."
                }
            )

        except Exception:
            raise AuthError(
                {
                    "code": "invalid_header",
                    "description": "Unable to parse authentication token"
                }
            )

    raise AuthError(
        {
            "code": "invalid_header",
            "description": "Unable to find the approrpirate key."
        },
        400
    )


def requires_auth(permission=""):
    def requires_auth_decorator(f):
        @ wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)

        return wrapper

    return requires_auth_decorator
