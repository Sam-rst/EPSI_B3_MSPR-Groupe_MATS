# apps/api/src/core/middlewares/limiter.py

from slowapi import Limiter
from slowapi.util import get_remote_address

# Un seul limiter pour toute l'app
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["100/hour"]  # Limite globale, adapte-la à ton besoin
)
