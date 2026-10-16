"""
funciones.py
Define las funciones de prueba (con numpy) y su ambiente controlado:
intervalo [a, b], estimaciones iniciales x0 / x1, derivadas, función de
iteración g(x) para punto fijo y escenarios para el análisis de sensibilidad.
"""
import numpy as np

TOL = 1e-6
MAX_ITER = 100


# Polinómica (raíz simple): f(x) = x^3 - x - 2
def f_polinomica(x):
    return x**3 - x - 2

def df_polinomica(x):
    return 3 * x**2 - 1

def d2f_polinomica(x):
    return 6 * x

def g_polinomica(x):
    return np.cbrt(x + 2)


# Polinómica (raíz doble): f(x) = (x - 2)^2  -> toca el eje en x = 2
def f_doble(x):
    return (x - 2) ** 2

def df_doble(x):
    return 2 * (x - 2)

def d2f_doble(x):
    return 2.0 + 0 * x

def g_doble(x):
    # x = (x^2 + 4) / 4  <=>  (x - 2)^2 = 0 ; g'(2) = 1 (caso límite)
    return (x**2 + 4) / 4


# Logarítmica: f(x) = ln(x) + x - 4
def f_logaritmica(x):
    return np.log(x) + x - 4

def df_logaritmica(x):
    return 1 / x + 1

def d2f_logaritmica(x):
    return -1 / x**2

def g_logaritmica(x):
    return 4 - np.log(x)


# Exponencial: f(x) = e^(-x) - x
def f_exponencial(x):
    return np.exp(-x) - x

def df_exponencial(x):
    return -np.exp(-x) - 1

def d2f_exponencial(x):
    return np.exp(-x)

def g_exponencial(x):
    return np.exp(-x)


# Trigonométrica: f(x) = cos(x) - x
def f_trigonometrica(x):
    return np.cos(x) - x

def df_trigonometrica(x):
    return -np.sin(x) - 1

def d2f_trigonometrica(x):
    return -np.cos(x)

def g_trigonometrica(x):
    return np.cos(x)


# Mixta: f(x) = sqrt(x) - cos(x)
def f_mixta(x):
    return np.sqrt(x) - np.cos(x)

def df_mixta(x):
    return 0.5 / np.sqrt(x) + np.sin(x)

def d2f_mixta(x):
    return -0.25 * x ** (-1.5) + np.cos(x)

LAMBDA_MIXTA = 0.5

def g_mixta(x):
    # Despeje con relajación: x = x - λ·f(x), con λ = 0,5
    # g'(r) = 1 - λ·f'(r) ≈ 0,39 < 1  -> converge
    return x - LAMBDA_MIXTA * (np.sqrt(x) - np.cos(x))

def g_mixta_alternativa(x):
    # Despeje "natural": sqrt(x) = cos(x) -> x = cos²(x)
    # g'(r) = -sin(2r) ≈ -0,96 -> |g'| casi 1, converge lentísimo
    return np.cos(x) ** 2


# Ambiente controlado de cada función
# a, b   -> intervalo para métodos cerrados (bisección, falsa posición)
# x0     -> estimación inicial (punto fijo, Newton, Newton mejorado)
# x0, x1 -> estimaciones iniciales para secante
FUNCIONES = [
    {
        "clave": "polinomica_simple",
        "categoria": "Polinómica (raíz simple)",
        "expresion": "f(x) = x³ − x − 2",
        "f": f_polinomica, "df": df_polinomica, "d2f": d2f_polinomica,
        "g": g_polinomica, "g_expresion": "g(x) = ∛(x + 2)",
        "a": 1.0, "b": 2.0, "x0": 1.0, "x1": 2.0,
        "rango_grafico": (0.0, 2.5),
        "raiz_doble": False,
        "intervalos_prueba": [(1.0, 2.0), (1.5, 1.6), (0.0, 3.0), (-2.0, 5.0), (1.0, 10.0)],
        "x0_prueba": [1.0, 1.5, 3.0, 0.58, 0.0, 10.0],
    },
    {
        "clave": "polinomica_doble",
        "categoria": "Polinómica (raíz doble)",
        "expresion": "f(x) = (x − 2)²",
        "f": f_doble, "df": df_doble, "d2f": d2f_doble,
        "g": g_doble, "g_expresion": "g(x) = (x² + 4) / 4",
        "a": 1.2, "b": 2.8, "x0": 1.2, "x1": 1.4,
        "rango_grafico": (0.5, 3.5),
        "raiz_doble": True,
        "raiz_exacta": 2.0,
        "intervalos_prueba": [(1.2, 2.8), (1.0, 3.0), (0.0, 5.0)],
        "x0_prueba": [1.2, 1.9, 0.0, 3.0, 5.0, 10.0],
    },
    {
        "clave": "logaritmica",
        "categoria": "Logarítmica",
        "expresion": "f(x) = ln(x) + x − 4",
        "f": f_logaritmica, "df": df_logaritmica, "d2f": d2f_logaritmica,
        "g": g_logaritmica, "g_expresion": "g(x) = 4 − ln(x)",
        "a": 2.0, "b": 3.0, "x0": 2.0, "x1": 3.0,
        "rango_grafico": (0.5, 4.5),
        "raiz_doble": False,
        "intervalos_prueba": [(2.0, 3.0), (2.9, 3.0), (1.0, 5.0), (0.5, 10.0), (1.0, 50.0)],
        "x0_prueba": [2.0, 3.0, 0.5, 0.1, 10.0, 30.0],
    },
    {
        "clave": "exponencial",
        "categoria": "Exponencial",
        "expresion": "f(x) = e^(−x) − x",
        "f": f_exponencial, "df": df_exponencial, "d2f": d2f_exponencial,
        "g": g_exponencial, "g_expresion": "g(x) = e^(−x)",
        "a": 0.0, "b": 1.0, "x0": 0.0, "x1": 1.0,
        "rango_grafico": (-0.5, 1.5),
        "raiz_doble": False,
        "intervalos_prueba": [(0.0, 1.0), (0.5, 0.6), (-2.0, 3.0), (-5.0, 10.0), (-10.0, 20.0)],
        "x0_prueba": [0.0, 1.0, -2.0, 3.0, 5.0, 10.0],
    },
    {
        "clave": "trigonometrica",
        "categoria": "Trigonométrica",
        "expresion": "f(x) = cos(x) − x",
        "f": f_trigonometrica, "df": df_trigonometrica, "d2f": d2f_trigonometrica,
        "g": g_trigonometrica, "g_expresion": "g(x) = cos(x)",
        "a": 0.0, "b": 1.0, "x0": 0.0, "x1": 1.0,
        "rango_grafico": (-0.5, 1.5),
        "raiz_doble": False,
        "intervalos_prueba": [(0.0, 1.0), (0.7, 0.8), (-2.0, 3.0), (-5.0, 10.0), (-20.0, 20.0)],
        "x0_prueba": [0.0, 1.0, -2.0, 3.0, 5.0, 10.0],
    },
    {
        "clave": "mixta",
        "categoria": "Mixta",
        "expresion": "f(x) = √x − cos(x)",
        "f": f_mixta, "df": df_mixta, "d2f": d2f_mixta,
        "g": g_mixta, "g_expresion": "g(x) = x − 0,5·(√x − cos x)",
        "a": 0.1, "b": 1.0, "x0": 0.5, "x1": 1.0,
        "rango_grafico": (0.01, 1.5),
        "raiz_doble": False,
        "intervalos_prueba": [(0.1, 1.0), (0.6, 0.7), (0.01, 3.0), (0.001, 5.0)],
        "x0_prueba": [0.5, 0.1, 1.0, 0.01, 2.0, 5.0, 10.0],
    },
]


def raiz_referencia(funcion):
    """Raíz 'verdadera' para medir el error |x_n - raíz|.
    Raíz doble: valor exacto. Resto: bisección llevada al límite de la
    precisión de máquina (200 pasos, sin tolerancia)."""
    if funcion.get("raiz_exacta") is not None:
        return funcion["raiz_exacta"]
    f = funcion["f"]
    a, b = funcion["a"], funcion["b"]
    fa = f(a)
    for _ in range(200):
        c = (a + b) / 2
        fc = f(c)
        if fc == 0 or c in (a, b):
            break
        if np.sign(fa) * np.sign(fc) < 0:
            b = c
        else:
            a, fa = c, fc
    return c