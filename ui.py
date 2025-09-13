"""
ui.py
Interfaz gráfica principal del Analizador de Funciones
"""
from typing import Any
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox, scrolledtext
import sympy as sp
import traceback
from core import parsear_funcion, calcular_dominio, calcular_recorrido, intersecciones, evaluar_paso_a_paso
from plot import graficar_funcion
from config import TITULO_GRAFICA


class AnalizadorApp:
    """
    Clase principal para la interfaz gráfica del Analizador de Funciones.
    Ahora incluye una pestaña de instrucciones de uso.
    """
    def __init__(self, root: Any):
        self.root = root
        self.root.title(TITULO_GRAFICA)
        self.root.geometry("800x660")
        self.root.resizable(False, False)
        self.estilo = ttk.Style("flatly")
        # Notebook para pestañas
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True)
        # Pestaña principal
        self.tab_principal = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_principal, text="Analizador")
        # Pestaña de instrucciones
        self.tab_instrucciones = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_instrucciones, text="Instrucciones de uso")
        # Configuración de placeholders
        self.placeholder_funcion = " Ejemplo: 2x^2 + 4"
        self.placeholder_color = "grey"
        self.text_color = "black"
        self.placeholder_activo = True
        # Crear componentes en pestaña principal
        self._crear_titulo(self.tab_principal)
        self._crear_entradas(self.tab_principal)
        self._crear_botones(self.tab_principal)
        self._crear_resultados(self.tab_principal)
        self._crear_pie(self.tab_principal)
        # Crear instrucciones en la segunda pestaña
        self._crear_instrucciones(self.tab_instrucciones)


    def _crear_titulo(self, parent: Any) -> None:
        ttk.Label(parent, text="Analizador de Funciones", font=("Segoe UI", 18, "bold")).pack(pady=12)

    def _crear_entradas(self, parent: Any) -> None:
        frame = ttk.Frame(parent)
        frame.pack(pady=5)
        self.entry_funcion = self._entrada(frame, "Función f(x):", 0, self.placeholder_funcion, 45, placeholder=True)
        self.entry_valor = self._entrada(frame, "Valor de x (opcional):", 1, "", 20)

    def _entrada(self, parent: Any, texto: str, fila: int, valor_defecto: str = "", ancho: int = 30, placeholder: bool = False) -> Any:
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

    def _crear_botones(self, parent: Any) -> None:
        frame = ttk.Frame(parent)
        frame.pack(pady=10)
        self._boton(frame, "Analizar", self.on_analizar, 0, PRIMARY)
        self._boton(frame, "Limpiar", self.on_limpiar, 1, WARNING)
        self._boton(frame, "Ayuda / Ejemplos", self.show_ayuda, 2, INFO)

    def _boton(self, parent: Any, texto: str, accion: Any, columna: int, estilo: Any) -> None:
        btn = ttk.Button(parent, text=texto, command=accion, width=18, bootstyle=estilo)
        btn.grid(row=0, column=columna, padx=6)

    def _crear_resultados(self, parent: Any) -> None:
        ttk.Label(parent, text="Resultados detallados:", font=("Segoe UI", 11, "bold")).pack(pady=(8, 4))
        self.text_result = scrolledtext.ScrolledText(parent, height=16, width=94, font=("Consolas", 10))
        self.text_result.pack(padx=10, pady=4)

    def _crear_pie(self, parent: Any) -> None:
        pie_texto = (
            "Incluye: Dominio, Recorrido, Intersecciones, Evaluación simbólica, Gráfica y errores manejados."
        )
        ttk.Label(parent, text=pie_texto, wraplength=760, justify='left').pack(pady=(10, 0))

    def _crear_instrucciones(self, parent: Any) -> None:
        instrucciones = (
            """
            📝  INSTRUCCIONES DE USO
            ──────────────────────────────

            1️⃣  Ingresa la función en el campo "Función f(x)".
                Ejemplo:  x^2 - 4   |   2x^2+3x-1   |   sin(x)

            2️⃣  (Opcional) Ingresa un valor para x en el campo correspondiente para evaluar la función en ese punto.

            3️⃣  Haz clic en "Analizar" para ver:
                • Dominio
                • Recorrido
                • Intersecciones
                • Evaluación simbólica
                • Gráfica profesional

            4️⃣  Usa "Limpiar" para borrar los campos y resultados.

            5️⃣  Haz clic en "Ayuda / Ejemplos" para ver ejemplos de funciones válidas.

            ──────────────────────────────
            💡  NOTAS IMPORTANTES
            ──────────────────────────────
            • Puedes usar ^ para potencias (se convierte internamente a **).
            • Solo se admite la variable x.
            • Si la función tiene discontinuidades, la gráfica las omitirá en esos puntos.
            • El resultado incluye justificación simbólica y gráfica profesional.

            ──────────────────────────────
            📚  EJEMPLOS DE FUNCIONES VÁLIDAS
            ──────────────────────────────
            - x^2 - 4
            - 1/(x-2)
            - (x+1)/(x-1)
            - 2x^3 - x
            - sin(x)
            """
        )
        frame = ttk.Frame(parent)
        frame.pack(fill='both', expand=True, padx=18, pady=18)
        label_titulo = ttk.Label(frame, text="Instrucciones de uso", font=("Segoe UI", 16, "bold"), foreground="#2a7ae2")
        label_titulo.pack(pady=(0,10))
        text_instr = scrolledtext.ScrolledText(frame, height=26, width=90, font=("Segoe UI", 12), wrap='word', background="#f7f7fa")
        text_instr.pack(padx=6, pady=6, fill='both', expand=True)
        text_instr.insert('1.0', instrucciones)
        text_instr.configure(state='disabled')

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
            self.text_result.insert('end', f"🔎  Función simbólica:\n{sp.pretty(f)}\n\n")

            # Dominio
            self.text_result.insert('end', "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
            self.text_result.insert('end', "📐  Dominio\n")
            self.text_result.insert('end', "Se utiliza continuous_domain de SymPy para encontrar el conjunto de valores reales donde la función es continua.\n")
            self.text_result.insert('end', f"Expresión analizada: {sp.pretty(f)}\n")
            dominio = calcular_dominio(f)
            self.text_result.insert('end', f"Dominio calculado: {dominio}\n\n")

            # Recorrido
            self.text_result.insert('end', "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
            self.text_result.insert('end', "📊  Recorrido\n")
            self.text_result.insert('end', "Se utiliza function_range de SymPy para determinar el conjunto de valores posibles de la función en el dominio calculado.\n")
            self.text_result.insert('end', f"Dominio usado: {dominio}\n")
            recorrido = calcular_recorrido(f, dominio)
            self.text_result.insert('end', f"Recorrido calculado: {recorrido}\n\n")

            # Intersecciones
            self.text_result.insert('end', "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
            self.text_result.insert('end', "📍  Intersecciones\n")
            self.text_result.insert('end', "Se resuelve f(x)=0 para encontrar raíces (eje X) y se evalúa f(0) para la intersección con el eje Y.\n")
            raices, y0 = intersecciones(f)
            self.text_result.insert('end', f"Raíces encontradas (f(x)=0): {raices}\n")
            self.text_result.insert('end', f"Intersección con eje Y (f(0)): {y0}\n\n")
        except Exception as e:
            messagebox.showerror("Error de parseo", str(e))
            return

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
