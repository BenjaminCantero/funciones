import tkinter as tk
from ui import AnalizadorApp

def iniciar_app():
    root = tk.Tk()
    app = AnalizadorApp(root)
    root.mainloop()

if __name__ == "__main__":
    iniciar_app()
