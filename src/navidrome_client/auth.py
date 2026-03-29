import hashlib
import os

from .config import NavidromeConfig


def build_auth_params(config: NavidromeConfig) -> dict[str, str]:
    """
    Build Subsonic authentication query parameters.

    Subsonic token-based auth:
        token = md5(password and salt)
        salt = random hex string (regenerated every call for security)

    Returns a dict ready to be passed as query params to every API request.
    """
    salt = os.urandom(8).hex()  # 16-char hex salt
    token = hashlib.md5((config.password + salt).encode()).hexdigest()

    return {
        "u": config.user,
        "t": token,
        "s": salt,
        "v": config.api_version,
        "c": config.client_name,
        "f": "json",
    }

