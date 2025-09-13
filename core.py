"""
core.py
Funciones matemáticas principales para el Analizador de Funciones
"""
from typing import Any, Tuple, Dict, Union
import sympy as sp
import math
x = sp.Symbol('x')

def limpiar_input(raw: str) -> str:
    """
    Limpia la entrada del usuario para sympy.
    Reemplaza '^' por '**', elimina espacios y agrega '*' donde falta.
    """
    s = raw.strip()
    s = s.replace('^', '**')
    s = s.replace(' ', '')
    out = ""
    for i, ch in enumerate(s):
        out += ch
        if i+1 < len(s):
            a, b = ch, s[i+1]
            if (a.isdigit() or a == ')') and (b == 'x' or b == '('):
                out += '*'
            if a == 'x' and (b.isdigit() or b == 'x' or b == '('):
                out += '*'
    out = out.replace('**', '^TEMP^').replace('* *', '*').replace('^TEMP^', '**')
    return out

def parsear_funcion(funcion_str: str) -> Any:
    """
    Convierte el string limpiado a expresión sympy.
    """
    if not funcion_str or funcion_str.strip() == "":
        raise ValueError("No ingresaste ninguna función.")
    s = limpiar_input(funcion_str)
    try:
        expr = sp.sympify(s)
        return sp.simplify(expr)
    except Exception as e:
        raise ValueError(f"Sympy no pudo interpretar la función: {e}")

def calcular_dominio(f: Any) -> Union[Any, str]:
    """
    Calcula el dominio simbólico de la función.
    """
    try:
        dom = sp.calculus.util.continuous_domain(f, x, sp.S.Reals)
        return dom
    except Exception as e:
        return f"No se pudo determinar simbólicamente ({e})"

def calcular_recorrido(f: Any, dominio: Any) -> Union[Any, str]:
    """
    Calcula el recorrido simbólico de la función.
    """
    try:
        if isinstance(dominio, str):
            raise Exception("Dominio simbólico no disponible")
        rango = sp.calculus.util.function_range(f, x, dominio)
        return rango
    except Exception as e:
        return f"No se pudo calcular simbólicamente ({e})"

def intersecciones(f: Any) -> Tuple[Any, Any]:
    """
    Calcula raíces (eje X) y f(0) (eje Y).
    """
    try:
        raices = sp.solve(sp.Eq(f, 0), x)
    except Exception:
        raices = "No se pudieron determinar las raíces simbólicamente"
    try:
        y0 = sp.simplify(f.subs(x, 0))
    except Exception:
        y0 = "No se pudo calcular f(0)"
    return raices, y0

def evaluar_paso_a_paso(f: Any, valor_x: Any) -> Dict[str, Any]:
    """
    Muestra el paso a paso de la evaluación de la función en un punto.
    """
    pasos: Dict[str, Any] = {}
    pasos['expresion_original'] = sp.simplify(f)
    try:
        pasos['sustitucion'] = f.subs(x, valor_x)
        pasos['simplificada'] = sp.simplify(pasos['sustitucion'])
        try:
            valor_numerico = sp.N(pasos['simplificada'])
            pasos['valor_numerico'] = valor_numerico
        except Exception:
            pasos['valor_numerico'] = "No se pudo obtener valor numérico"
    except Exception as e:
        pasos['sustitucion'] = f"Error en la sustitución: {e}"
        pasos['simplificada'] = pasos['sustitucion']
        pasos['valor_numerico'] = pasos['sustitucion']
    return pasos

def generar_muestra_x(dominio_sym: Any, npoints: int = 500, rango_extra: int = 5) -> list:
    """
    Genera una lista de puntos x para graficar evitando discontinuidades.
    """
    xs = []
    try:
        if isinstance(dominio_sym, (sp.Union, sp.Interval)):
            intervals = []
            if isinstance(dominio_sym, sp.Union):
                for a in dominio_sym.args:
                    intervals.append(a)
            else:
                intervals = [dominio_sym]
            for inter in intervals:
                a = inter.start
                b = inter.end
                if a is sp.S.NegativeInfinity:
                    a = -rango_extra
                if b is sp.S.Infinity:
                    b = rango_extra
                try:
                    a_f = float(a)
                except Exception:
                    a_f = -rango_extra
                try:
                    b_f = float(b)
                except Exception:
                    b_f = rango_extra
                if a_f == b_f:
                    xs.append(a_f)
                else:
                    step = (b_f - a_f) / max(40, min(npoints, 800))
                    if step == 0:
                        xs.append(a_f)
                    else:
                        cur = a_f
                        while cur <= b_f:
                            xs.append(cur)
                            cur += step
        else:
            xs = [i * 0.1 for i in range(-50, 51)]
    except Exception:
        xs = [i * 0.1 for i in range(-50, 51)]
    xs_unique = sorted(list({round(v, 12) for v in xs}))
    return xs_unique

def evaluar_lista_segura(f, xs):
    fx = sp.lambdify(x, f, "math")
    xs_valid = []
    ys_valid = []
    for xi in xs:
        try:
            yi = fx(xi)
            if yi is None:
                continue
            if isinstance(yi, complex):
                continue
            if math.isinf(yi) or math.isnan(float(yi)):
                continue
            xs_valid.append(float(xi))
            ys_valid.append(float(yi))
        except Exception:
            continue
    return xs_valid, ys_valid
