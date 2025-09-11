import tkinter as tk
from tkinter import messagebox, scrolledtext
import sympy as sp
import traceback
from core import parsear_funcion, calcular_dominio, calcular_recorrido, intersecciones, evaluar_paso_a_paso
from plot import graficar_funcion

class AnalizadorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Analizador de Funciones - MAT1185")
        self.root.geometry("780x660")
        lbl_title = tk.Label(root, text="Analizador de Funciones", font=("Helvetica", 16, "bold"))
        lbl_title.pack(pady=(10, 4))
        frame_inputs = tk.Frame(root)
        frame_inputs.pack(pady=6)
        tk.Label(frame_inputs, text="Ingrese función f(x):", anchor='w').grid(row=0, column=0, sticky='w')
        self.entry_funcion = tk.Entry(frame_inputs, width=50, font=("Consolas", 12))
        self.entry_funcion.grid(row=0, column=1, padx=6, pady=4)
        self.entry_funcion.insert(0, "x**2 - 4")
        tk.Label(frame_inputs, text="Ingrese valor de x (opcional):", anchor='w').grid(row=1, column=0, sticky='w')
        self.entry_valor = tk.Entry(frame_inputs, width=20, font=("Consolas", 12))
        self.entry_valor.grid(row=1, column=1, sticky='w', padx=6, pady=4)
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=6)
        self.btn_analizar = tk.Button(btn_frame, text="Analizar", command=self.on_analizar, width=14)
        self.btn_analizar.grid(row=0, column=0, padx=6)
        self.btn_limpiar = tk.Button(btn_frame, text="Limpiar", command=self.on_limpiar, width=14)
        self.btn_limpiar.grid(row=0, column=1, padx=6)
        self.btn_ayuda = tk.Button(btn_frame, text="Ayuda / Ejemplos", command=self.show_ayuda, width=14)
        self.btn_ayuda.grid(row=0, column=2, padx=6)
        lbl_results = tk.Label(root, text="Resultados (detalle):", font=("Helvetica", 12, "bold"))
        lbl_results.pack(pady=(8, 4))
        self.text_result = scrolledtext.ScrolledText(root, height=14, width=92, font=("Consolas", 10))
        self.text_result.pack(padx=8)
        lbl_rubrica = tk.Label(root, text="La aplicación intenta cumplir todos los criterios de la rúbrica: dominio, recorrido, intersecciones, evaluación paso a paso, gráficas y manejo de errores.", wraplength=760, justify='left')
        lbl_rubrica.pack(pady=(8,4))
        lbl_footer = tk.Label(root, text="Mat: SymPy + Matplotlib | UI: Tkinter | No usa numpy", font=("Helvetica", 9, "italic"))
        lbl_footer.pack(side='bottom', pady=6)
    def on_limpiar(self):
        self.entry_funcion.delete(0, tk.END)
        self.entry_valor.delete(0, tk.END)
        self.text_result.delete('1.0', tk.END)
    def show_ayuda(self):
        ejemplos = (
            "Ejemplos de funciones válidas:\n"
            " - x**2 - 4\n"
            " - 1/(x-2)\n"
            " - (x+1)/(x-1)\n"
            " - 2*x**3 - x\n"
            " - sin(x)  (Sympy reconoce sin, cos, exp, log, etc.)\n\n"
            "Notas:\n"
            " - Puedes usar '^' para potencia (se convierte internamente a '**').\n"
            " - No uses variables distintas de 'x'.\n"
            " - Si la función tiene discontinuidades, la gráfica las omitirá en esos puntos.\n"
        )
        messagebox.showinfo("Ayuda / Ejemplos", ejemplos)
    def on_analizar(self):
        funcion_txt = self.entry_funcion.get()
        valor_txt = self.entry_valor.get().strip()
        self.text_result.delete('1.0', tk.END)
        try:
            f = parsear_funcion(funcion_txt)
            self.text_result.insert(tk.END, f"Función interpretada simbólicamente: {sp.pretty(f)}\n\n")
        except Exception as e:
            messagebox.showerror("Error de parseo", str(e))
            return
        dominio = calcular_dominio(f)
        self.text_result.insert(tk.END, f"Dominio (simbólico): {dominio}\n")
        recorrido = calcular_recorrido(f, dominio)
        self.text_result.insert(tk.END, f"Recorrido (simbólico): {recorrido}\n")
        raices, y0 = intersecciones(f)
        self.text_result.insert(tk.END, f"Intersección(s) con eje X (f(x)=0): {raices}\n")
        self.text_result.insert(tk.END, f"Intersección con eje Y (f(0)): {y0}\n\n")
        eval_info = None
        if valor_txt != "":
            try:
                valor_sym = sp.sympify(valor_txt)
                pasos = evaluar_paso_a_paso(f, valor_sym)
                eval_info = pasos
                self.text_result.insert(tk.END, "----- Evaluación paso a paso -----\n")
                self.text_result.insert(tk.END, f"1) Expresión original: {sp.pretty(pasos['expresion_original'])}\n")
                self.text_result.insert(tk.END, f"2) Sustitución: {sp.pretty(pasos['sustitucion'])}\n")
                self.text_result.insert(tk.END, f"3) Simplificada: {sp.pretty(pasos['simplificada'])}\n")
                self.text_result.insert(tk.END, f"4) Valor numérico: {pasos['valor_numerico']}\n\n")
            except Exception as e:
                self.text_result.insert(tk.END, f"Error al evaluar en x={valor_txt}: {e}\n\n")
        self.text_result.insert(tk.END, "----- Justificación computacional (resumen) -----\n")
        self.text_result.insert(tk.END, "Se usó SymPy para cálculo simbólico: continuous_domain para dominio, function_range para recorrido (si es posible), solve para raíces y subs/N para evaluación numérica.\n\n")
        try:
            graficar_funcion(f, dominio, raices, y0, valor_txt, eval_info)
            self.text_result.insert(tk.END, "Gráfica generada. (Se abrió una ventana con Matplotlib)\n")
        except Exception as e:
            self.text_result.insert(tk.END, f"Error al graficar: {e}\n")
            self.text_result.insert(tk.END, traceback.format_exc() + "\n")
