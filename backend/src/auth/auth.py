import json
from flask import request, _request_ctx_stack
from functools import wraps
from jose import JWTError, jwt
from urllib.request import urlopen
from decouple import config

AUTH0_DOMAIN = config('AUTH0_DOMAIN')

## AUTH0_DOMAIN = 'udacity-fsnd.auth0.com'
ALGORITHMS = [str(config('ALGORITHM'))]
AUTH0_AUDIENCE = config('AUTH0_AUDIENCE')

## AuthError Exception
'''
AuthError Exception
A standardized way to communicate auth failure modes
'''
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


## Auth Header

'''
@TODO implement get_token_auth_header() method
    it should attempt to get the header from the request
        it should raise an AuthError if no header is present
    it should attempt to split bearer and the token
        it should raise an AuthError if the header is malformed
    return the token part of the header
'''
def get_token_auth_header():
    '''
    Retrieve access token from authorization header
        Parameters:
            None
        Returns:
            [token] string: The part of the header that contains the token
    '''
    headers = request.headers

    if 'Authorization' not in headers.keys():
        raise AuthError({
            'code': 'missing_authorization_header',
            'message': 'authorization not found in header'
        }, 401)

    authorization = headers['Authorization']

    token = authorization.split()[1]

    return token

'''
@TODO implement check_permissions(permission, payload) method
    @INPUTS
        permission: string permission (i.e. 'post:drink')
        payload: decoded jwt payload

    it should raise an AuthError if permissions are not included in the payload
        !!NOTE check your RBAC settings in Auth0
    it should raise an AuthError if the requested permission string is not in the payload permissions array
    return true otherwise
'''
def check_permissions(permission, payload):
    '''
    A function that checks user permission
        Parameters:
            permission (String) : Auth0 user permission in the form ['post:drink']
            payload (String): decoded jwt payload
        Returns:
            True (bool): a true value for a verified permission
    '''
    if 'permissions' not in payload:
        raise AuthError({
            'code': 'invalid_token',
            'message': 'permissions not included in token'
            }, 400)

    if permission not in payload['permissions']:
        raise AuthError({
            'code': 'unauthorized_access',
            'message': 'not authorized to access this resource'
            }, 403)

    return True


'''
@TODO implement verify_decode_jwt(token) method
    @INPUTS
        token: a json web token (string)

    it should be an Auth0 token with key id (kid)
    it should verify the token using Auth0 /.well-known/jwks.json
    it should decode the payload from the token
    it should validate the claims
    return the decoded payload

    !!NOTE urlopen has a common certificate error described here: https://stackoverflow.com/questions/50236117/scraping-ssl-certificate-verify-failed-error-for-http-en-wikipedia-org
'''
def verify_decode_jwt(token):
    '''
    A function that decodes and verifies a json web token
        Parameters:
            token (string) : JSON web token
        Returns:
            payload (dict): user payload containing key-value pairs
    '''
    json_url = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    json_jwks = json.loads(json_url.read())

    try:
        unverified_header = jwt.get_unverified_header(token)

        if 'kid' not in unverified_header:
            raise AuthError({
                'code': 'unauthorized',
                'message': 'authorization header is invalid'
                }, 401)

    except JWTError:
        raise AuthError({
            'code':'malformed_header',
            'message': 'request header is malformed'
        }, 400)

    rsa_key = {}

    for dict in json_jwks['keys']:
        if unverified_header['kid'] == dict['kid']:
            rsa_key = {**dict}

    if len(rsa_key) != 0:

        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=AUTH0_AUDIENCE,
                issuer=f'https://{AUTH0_DOMAIN}/'
                )
            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'expired_token',
                'message': 'token has expired'
                }, 401)

        except jwt.JWTError:
            raise AuthError({
                'code': 'bad_signature',
                'message': 'invalid token signature'
                }, 400)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claim',
                'message': 'signature verification failed'
                }, 400)

        except Exception:
            raise AuthError({
                'code': 'malformed_header',
                'message': 'request header is invalid'
                }, 400)


'''
@TODO implement @requires_auth(permission) decorator method
    @INPUTS
        permission: string permission (i.e. 'post:drink')

    it should use the get_token_auth_header method to get the token
    it should use the verify_decode_jwt method to decode the jwt
    it should use the check_permissions method validate claims and check the requested permission
    return the decorator which passes the decoded payload to the decorated method
'''
def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            try:
                payload = verify_decode_jwt(token)
            except:
                raise AuthError({
                    'code': 'unauthorized_access',
                    'message': 'no authorization to view this resource'
                    }, 401)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)
        return wrapper
    return requires_auth_decorator