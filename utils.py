"""
utils.py
Funciones auxiliares para validaciones y formateos
"""
from typing import Any

def es_numero(valor: Any) -> bool:
    """Verifica si un valor puede convertirse a float."""
    try:
        float(valor)
        return True
    except Exception:
        return False

def formatear_numero(valor: Any, decimales: int = 4) -> str:
    """Formatea un número con la cantidad de decimales indicada."""
    try:
        return f"{float(valor):.{decimales}f}"
    except Exception:
        return str(valor)
