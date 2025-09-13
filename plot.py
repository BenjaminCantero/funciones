
"""
plot.py
Funciones para graficar la función y sus elementos destacados
"""
from typing import Any, Optional
import matplotlib.pyplot as plt
import sympy as sp
from core import x, generar_muestra_x, evaluar_lista_segura
from config import FIGURE_SIZE, NPOINTS, RANGO_EXTRA, COLOR_RAIZ, COLOR_Y0, COLOR_PUNTO_EVAL, TITULO_GRAFICA, XLABEL, YLABEL, LEGENDA_FONT_SIZE
from utils import formatear_numero

def graficar_funcion(
    f: Any,
    dominio: Any,
    raices: Any,
    y0: Any,
    valor_txt: Optional[str] = None,
    eval_info: Optional[dict] = None
) -> None:
    """
    Genera la gráfica de la función, mostrando dominio, recorrido, intersecciones y punto evaluado.
    """
    xs_samples = generar_muestra_x(dominio, npoints=NPOINTS, rango_extra=RANGO_EXTRA)
    xs_plot, ys_plot = evaluar_lista_segura(f, xs_samples)
    if not xs_plot:
        xs_fallback = [i * 0.1 for i in range(-100, 101)]
        xs_plot, ys_plot = evaluar_lista_segura(f, xs_fallback)
    plt.figure(figsize=FIGURE_SIZE)
    plt.plot(xs_plot, ys_plot, label=f"f(x) = {sp.srepr(f) if len(str(f))>40 else f}", linewidth=2)
    plt.axhline(0, linewidth=1, color='black')
    plt.axvline(0, linewidth=1, color='black')
    plt.grid(True)
    plt.title(TITULO_GRAFICA)
    plt.xlabel(XLABEL)
    plt.ylabel(YLABEL)
    # Intersecciones con eje X
    try:
        if isinstance(raices, (list, tuple)):
            for r in raices:
                try:
                    r_eval = float(sp.N(r))
                    y_at_r = float(sp.N(f.subs(x, r)))
                    plt.scatter(r_eval, y_at_r, marker='o', s=50, color=COLOR_RAIZ, label=f"Raíz ≈ {formatear_numero(r_eval)}")
                except Exception:
                    continue
    except Exception:
        pass
    # Intersección con eje Y
    try:
        if not isinstance(y0, str):
            y0f = float(sp.N(y0))
            plt.scatter(0.0, y0f, marker='s', s=50, color=COLOR_Y0, label=f"f(0)={formatear_numero(y0f)}")
    except Exception:
        pass
    # Punto evaluado
    if eval_info is not None and valor_txt is not None:
        try:
            valor_sym = sp.sympify(valor_txt)
            y_val = float(sp.N(f.subs(x, valor_sym)))
            x_val = float(sp.N(valor_sym))
            plt.scatter(x_val, y_val, color=COLOR_PUNTO_EVAL, s=70, label=f"Punto evaluado ({formatear_numero(x_val)},{formatear_numero(y_val)})")
        except Exception:
            pass
    plt.legend(loc='best', fontsize=LEGENDA_FONT_SIZE)
    plt.tight_layout()
    plt.show()
