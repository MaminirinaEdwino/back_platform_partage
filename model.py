from pydantic import BaseModel
from typing import Optional

class Fichier(BaseModel):
    id: int
    name: str
    description: str
    chemin : str
    categorie: int = 1

class FichierUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None