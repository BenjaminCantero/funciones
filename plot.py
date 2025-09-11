import matplotlib.pyplot as plt
import sympy as sp
from core import x, generar_muestra_x, evaluar_lista_segura

#feat: módulo para graficar funciones matemáticas con matplotlib y sympy

#Permite visualizar funciones, raíces, valor en x=0 y puntos evaluados específicos.
#Integra utilidades del módulo 'core' para generar muestras del dominio y evaluar de forma segura.
#Incluye la función principal graficar_funcion que muestra una gráfica clara y detallada.
#Útil para análisis visual y educativo de funciones matemáticas.

def graficar_funcion(f, dominio, raices, y0, valor_txt=None, eval_info=None):
    xs_samples = generar_muestra_x(dominio, npoints=300, rango_extra=8)
    xs_plot, ys_plot = evaluar_lista_segura(f, xs_samples)
    if not xs_plot:
        xs_fallback = [i * 0.1 for i in range(-100, 101)]
        xs_plot, ys_plot = evaluar_lista_segura(f, xs_fallback)
    plt.figure(figsize=(8,5))
    plt.plot(xs_plot, ys_plot, label=f"f(x) = {sp.srepr(f) if len(str(f))>40 else f}", linewidth=2)
    plt.axhline(0, linewidth=1, color='black')
    plt.axvline(0, linewidth=1, color='black')
    plt.grid(True)
    plt.title("Gráfica de la función")
    plt.xlabel("x")
    plt.ylabel("f(x)")
    try:
        if isinstance(raices, (list, tuple)):
            for r in raices:
                try:
                    r_eval = float(sp.N(r))
                    y_at_r = float(sp.N(f.subs(x, r)))
                    plt.scatter(r_eval, y_at_r, marker='o', s=50, label=f"Raíz ≈ {round(r_eval,4)}")
                except Exception:
                    continue
    except Exception:
        pass
    try:
        if not isinstance(y0, str):
            y0f = float(sp.N(y0))
            plt.scatter(0.0, y0f, marker='s', s=50, label=f"f(0)={round(y0f,4)}")
    except Exception:
        pass
    if eval_info is not None and valor_txt is not None:
        try:
            valor_sym = sp.sympify(valor_txt)
            y_val = float(sp.N(f.subs(x, valor_sym)))
            x_val = float(sp.N(valor_sym))
            plt.scatter(x_val, y_val, color='red', s=70, label=f"Punto evaluado ({round(x_val,4)},{round(y_val,4)})")
        except Exception:
            pass
    plt.legend(loc='best', fontsize='small')
    plt.tight_layout()
    plt.show()
