from enum import Enum


class TypeAttaque(str, Enum):
    SQLI = "sqli"
    XSS = "xss"
    CSRF = "csrf"
    HEADERS = "headers_cookies"
