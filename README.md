# Analizador de Funciones

Aplicación para analizar funciones matemáticas, desarrollada para MAT1185 - Unidad 2 (Parte B).

## Características
- Interfaz gráfica con Tkinter.
- Parseo y análisis simbólico con SymPy.
- Cálculo de dominio, recorrido, intersecciones y evaluación paso a paso.
- Gráficas profesionales con Matplotlib.
- Manejo de errores y discontinuidades.
- Arquitectura modular: `main.py`, `ui.py`, `core.py`, `plot.py`, `config.py`, `utils.py`.

## Requisitos
- Python 3.8 o superior
- Paquetes: sympy, matplotlib

## Instalación
1. Instala Python desde [python.org](https://www.python.org/).
2. Instala las dependencias ejecutando en PowerShell:
   ```powershell
   pip install sympy matplotlib
   ```

## Uso
1. Ejecuta el programa principal:
   ```powershell
   python main.py
   ```
2. Ingresa la función en el formato aceptado (ejemplo: `x^2 - 4`, `2*x + 1`, `sin(x)`).
3. (Opcional) Ingresa un valor para `x` para evaluar la función en ese punto.
4. Haz clic en "Analizar" para ver los resultados y la gráfica.

## Ejemplos de funciones válidas
- `x^2 - 4`
- `1/(x-2)`
- `(x+1)/(x-1)`
- `2*x^3 - x`
- `sin(x)`

## Notas
- Puedes usar `^` para potencias (se convierte internamente a `**`).
- Solo se admite la variable `x`.
- Si la función tiene discontinuidades, la gráfica las omitirá en esos puntos.


## Estructura del proyecto
- `main.py`: punto de entrada.
- `ui.py`: interfaz gráfica y lógica de pestañas.
- `core.py`: lógica matemática y helpers.
- `plot.py`: funciones de graficado con Matplotlib.
- `config.py`: configuración y constantes globales.
- `utils.py`: utilidades y validaciones auxiliares.

## Cumplimiento de la rúbrica
El proyecto cumple con los siguientes criterios:
- Evaluación de funciones simbólicas.
- Cálculo y justificación paso a paso de dominio, recorrido e intersecciones.
- Evaluación en un punto y marcado en la gráfica.
- Gráfica profesional con dominio, recorrido, intersecciones, títulos, etiquetas y colores.
- Manejo de errores y entradas inválidas.
- Arquitectura modular y código limpio.
- Interfaz intuitiva y amigable con pestañas e instrucciones.
- Documentación y repositorio colaborativo en GitHub.

---
Desarrollado para fines educativos. Para dudas o mejoras, abre un issue en el repositorio.

S