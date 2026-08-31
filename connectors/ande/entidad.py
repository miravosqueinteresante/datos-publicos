import json
import os
import unicodedata

_REGISTRO = None
_RUTA = os.path.join(os.path.dirname(__file__), "entidades.json")


def _cargar():
    global _REGISTRO
    if _REGISTRO is None:
        with open(_RUTA, encoding="utf-8") as f:
            _REGISTRO = json.load(f)
    return _REGISTRO


def get(entidad_id):
    """Retorna dict de la entidad o None."""
    return _cargar().get(entidad_id)


def listar_ids():
    """Retorna lista de IDs canónicos."""
    return list(_cargar().keys())


def _normalizar(texto):
    """Quita tildes y pasa a minúsculas."""
    nfkd = unicodedata.normalize("NFKD", texto)
    return "".join(c for c in nfkd if not unicodedata.combining(c)).lower()


def nombre_a_id(nombre):
    """Convierte nombre display a ID canónico. None si no encuentra."""
    normalizado = _normalizar(nombre)
    for eid, meta in _cargar().items():
        if _normalizar(meta["nombre"]) == normalizado:
            return eid
        if _normalizar(meta.get("sigla", "")) == normalizado:
            return eid
    return None
