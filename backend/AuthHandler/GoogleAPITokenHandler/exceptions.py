class ReAuthenticationRequired(Exception):
    http_status = 401
class TokenNotFound(Exception):
    http_status = 400