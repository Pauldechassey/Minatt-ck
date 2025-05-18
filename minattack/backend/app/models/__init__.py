# Minatt-ck/minattack/backend/app/models/__init__.py

# from ..database import Base # Only if Base is defined one level up in database.py
                            # If Base is defined in, for example, a models.base_model module, adjust.
                            # Typically, Base is imported where models are defined.

from .attaque import Attaque
from .audit import Audit
from .domaine import Domaine
from .faille import Faille
from .sous_domaine import SousDomaine
from .technologie import Technologie
from .type_attaque import Type_attaque  # Assuming this is your class name for type_attaque.py
from .user import User
# from .utiliser import Utiliser # If Utiliser is also an SQLAlchemy model class

# Optional: define __all__ if you want to control what `from .models import *` imports
__all__ = [
    "Attaque", "Audit", "Domaine", "Faille", "SousDomaine", 
    "Technologie", "Type_attaque", "User" #, "Utiliser"
]
