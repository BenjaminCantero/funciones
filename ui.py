import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox, scrolledtext
import sympy as sp
import traceback

from core import parsear_funcion, calcular_dominio, calcular_recorrido, intersecciones, evaluar_paso_a_paso
from plot import graficar_funcion

class AnalizadorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Analizador de Funciones - MAT1185")
        self.root.geometry("800x660")
        self.root.resizable(False, False)

        self.estilo = ttk.Style("flatly")

        # Placeholder config
        self.placeholder_funcion = " Ejemplo: 2x^2 + 4"
        self.placeholder_color = "grey"
        self.text_color = "black"
        self.placeholder_activo = True

        self._crear_titulo()
        self._crear_entradas()
        self._crear_botones()
        self._crear_resultados()
        self._crear_pie()

    def _crear_titulo(self):
        ttk.Label(self.root, text="Analizador de Funciones", font=("Segoe UI", 18, "bold")).pack(pady=12)

    def _crear_entradas(self):
        frame = ttk.Frame(self.root)
        frame.pack(pady=5)

        self.entry_funcion = self._entrada(frame, "Función f(x):", 0, self.placeholder_funcion, 45, placeholder=True)
        self.entry_valor = self._entrada(frame, "Valor de x (opcional):", 1, "", 20)

    def _entrada(self, parent, texto, fila, valor_defecto="", ancho=30, placeholder=False):
        ttk.Label(parent, text=texto).grid(row=fila, column=0, sticky='w', padx=6, pady=6)
        entry = ttk.Entry(parent, width=ancho, font=("Consolas", 11))
        entry.grid(row=fila, column=1, padx=6, pady=6)

        if placeholder:
            entry.insert(0, valor_defecto)
            entry.configure(foreground=self.placeholder_color)
            entry.bind("<FocusIn>", self._on_focusin_funcion)
            entry.bind("<FocusOut>", self._on_focusout_funcion)
        elif valor_defecto:
            entry.insert(0, valor_defecto)

        return entry

    def _crear_botones(self):
        frame = ttk.Frame(self.root)
        frame.pack(pady=10)

        self._boton(frame, "Analizar", self.on_analizar, 0, PRIMARY)
        self._boton(frame, "Limpiar", self.on_limpiar, 1, WARNING)
        self._boton(frame, "Ayuda / Ejemplos", self.show_ayuda, 2, INFO)

    def _boton(self, parent, texto, accion, columna, estilo):
        btn = ttk.Button(parent, text=texto, command=accion, width=18, bootstyle=estilo)
        btn.grid(row=0, column=columna, padx=6)

    def _crear_resultados(self):
        ttk.Label(self.root, text="Resultados detallados:", font=("Segoe UI", 11, "bold")).pack(pady=(8, 4))
        self.text_result = scrolledtext.ScrolledText(self.root, height=16, width=94, font=("Consolas", 10))
        self.text_result.pack(padx=10, pady=4)

    def _crear_pie(self):
        pie_texto = (
            "Incluye: Dominio, Recorrido, Intersecciones, Evaluación simbólica, Gráfica y errores manejados."
        )
        ttk.Label(self.root, text=pie_texto, wraplength=760, justify='left').pack(pady=(10, 0))

    # === Placeholder handling ===

    def _on_focusin_funcion(self, event):
        entry = event.widget
        if self.placeholder_activo:
            entry.delete(0, 'end')
            entry.configure(foreground=self.text_color)
            self.placeholder_activo = False

    def _on_focusout_funcion(self, event):
        entry = event.widget
        if not entry.get().strip():
            entry.insert(0, self.placeholder_funcion)
            entry.configure(foreground=self.placeholder_color)
            self.placeholder_activo = True

    # ============================

    def on_limpiar(self):
        self.entry_funcion.delete(0, 'end')
        self.entry_funcion.insert(0, self.placeholder_funcion)
        self.entry_funcion.configure(foreground=self.placeholder_color)
        self.placeholder_activo = True

        self.entry_valor.delete(0, 'end')
        self.text_result.delete('1.0', 'end')

    def show_ayuda(self):
        ejemplos = (
            "Ejemplos válidos:\n"
            " - x**2 - 4\n"
            " - 1/(x-2)\n"
            " - sin(x), cos(x), log(x), exp(x)\n\n"
            "Notas:\n"
            " - Puedes usar '^' (se convierte internamente a '**').\n"
            " - Solo se permite la variable 'x'.\n"
            " - Discontinuidades se omiten en la gráfica.\n"
        )
        messagebox.showinfo("Ayuda / Ejemplos", ejemplos)

    def on_analizar(self):
        funcion_txt = self.entry_funcion.get().strip()
        valor_txt = self.entry_valor.get().strip()
        self.text_result.delete('1.0', 'end')

        if self.placeholder_activo or not funcion_txt:
            messagebox.showwarning("Función no ingresada", "No se ha insertado ninguna función.\nPor favor escríbela antes de analizar.")
            return

        try:
            f = parsear_funcion(funcion_txt)
            self.text_result.insert('end', f"Función simbólica: {f}\n\n")
        except Exception as e:
            messagebox.showerror("Error de parseo", str(e))
            return

        dominio = calcular_dominio(f)
        recorrido = calcular_recorrido(f, dominio)
        raices, y0 = intersecciones(f)

        self.text_result.insert('end', f"Dominio: {dominio}\n")
        self.text_result.insert('end', f"Recorrido: {recorrido}\n")
        self.text_result.insert('end', f"Intersecciones eje X: {raices}\n")
        self.text_result.insert('end', f"Intersección eje Y: {y0}\n\n")

        eval_info = None
        if valor_txt:
            try:
                valor_sym = sp.sympify(valor_txt)
                pasos = evaluar_paso_a_paso(f, valor_sym)
                eval_info = pasos
                self.text_result.insert('end', "----- Evaluación paso a paso -----\n")
                for i, (clave, valor) in enumerate(pasos.items(), 1):
                    self.text_result.insert('end', f"{i}) {clave.replace('_', ' ').capitalize()}: {valor}\n")
                self.text_result.insert('end', "\n")
            except Exception as e:
                self.text_result.insert('end', f"Error al evaluar x={valor_txt}: {e}\n\n")

        try:
            graficar_funcion(f, dominio, raices, y0, valor_txt, eval_info)
        except Exception as e:
            self.text_result.insert('end', f"Error al graficar: {e}\n")
            self.text_result.insert('end', traceback.format_exc() + "\n")
