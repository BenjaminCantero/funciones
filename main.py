
"""
main.py
Punto de entrada del Analizador de Funciones
"""
import tkinter as tk
from ui import AnalizadorApp

def iniciar_app() -> None:
    """Inicializa y ejecuta la aplicación principal."""
    root = tk.Tk()
    app = AnalizadorApp(root)
    root.mainloop()

if __name__ == "__main__":
    iniciar_app()
