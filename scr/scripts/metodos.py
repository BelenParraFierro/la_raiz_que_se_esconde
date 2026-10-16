"""
metodos.py
Implementación con numpy de los seis métodos de búsqueda de raíces.

Todos devuelven un diccionario:
    raiz         -> última aproximación (np.nan si no aplica)
    iteraciones  -> número de iteraciones realizadas
    historial    -> np.array con x_1, x_2, ..., x_n
    convergio    -> True / False
    estado       -> texto que explica cómo terminó

Criterio de parada (igual para todos): |f(x_n)| < tol  o  |x_n - x_(n-1)| < tol
"""
import numpy as np

from funciones import TOL, MAX_ITER

LIMITE_DIVERGENCIA = 1e10
CERO_DERIVADA = 1e-14

NOMBRES_METODOS = {
    "biseccion": "Bisección",
    "falsa_posicion": "Falsa posición",
    "punto_fijo": "Punto fijo",
    "secante": "Secante",
    "newton": "Newton-Raphson",
    "newton_mejorado": "Newton mejorado",
}


def _resultado(historial, convergio, estado):
    raiz = historial[-1] if historial else np.nan
    return {
        "raiz": float(raiz),
        "iteraciones": len(historial),
        "historial": np.array(historial, dtype=float),
        "convergio": convergio,
        "estado": estado,
    }


def _debe_parar(f_x, x_nuevo, x_anterior, tol):
    if abs(f_x) < tol:
        return True
    if x_anterior is not None and abs(x_nuevo - x_anterior) < tol:
        return True
    return False


def _invalido(x, f_x):
    return not np.isfinite(x) or not np.isfinite(f_x)


# Métodos cerrados
def biseccion(f, a, b, tol=TOL, max_iter=MAX_ITER):
    with np.errstate(all="ignore"):
        fa, fb = f(a), f(b)
        if _invalido(a, fa) or _invalido(b, fb):
            return _resultado([], False, "no aplica: extremo fuera del dominio")
        if np.sign(fa) * np.sign(fb) > 0:
            return _resultado([], False, "no aplica: f(a)·f(b) > 0 (sin cambio de signo)")
        historial = []
        x_anterior = None
        while True:
            c = (a + b) / 2
            fc = f(c)
            historial.append(c)
            if _debe_parar(fc, c, x_anterior, tol):
                return _resultado(historial, True, "convergió")
            if len(historial) >= max_iter:
                return _resultado(historial, False, "alcanzó el máximo de iteraciones")
            if np.sign(fa) * np.sign(fc) < 0:
                b, fb = c, fc
            else:
                a, fa = c, fc
            x_anterior = c


def falsa_posicion(f, a, b, tol=TOL, max_iter=MAX_ITER):
    with np.errstate(all="ignore"):
        fa, fb = f(a), f(b)
        if _invalido(a, fa) or _invalido(b, fb):
            return _resultado([], False, "no aplica: extremo fuera del dominio")
        if np.sign(fa) * np.sign(fb) > 0:
            return _resultado([], False, "no aplica: f(a)·f(b) > 0 (sin cambio de signo)")
        historial = []
        x_anterior = None
        while True:
            c = b - fb * (b - a) / (fb - fa)
            fc = f(c)
            historial.append(c)
            if _debe_parar(fc, c, x_anterior, tol):
                return _resultado(historial, True, "convergió")
            if len(historial) >= max_iter:
                return _resultado(historial, False, "alcanzó el máximo de iteraciones")
            if np.sign(fa) * np.sign(fc) < 0:
                b, fb = c, fc
            else:
                a, fa = c, fc
            x_anterior = c


# Métodos abiertos
def punto_fijo(f, g, x0, tol=TOL, max_iter=MAX_ITER):
    with np.errstate(all="ignore"):
        historial = []
        x = x0
        while True:
            x_nuevo = g(x)
            f_nuevo = f(x_nuevo)
            if _invalido(x_nuevo, f_nuevo):
                return _resultado(historial, False, "falló: g(x) salió del dominio")
            historial.append(x_nuevo)
            if abs(x_nuevo) > LIMITE_DIVERGENCIA:
                return _resultado(historial, False, "divergió")
            if _debe_parar(f_nuevo, x_nuevo, x, tol):
                return _resultado(historial, True, "convergió")
            if len(historial) >= max_iter:
                return _resultado(historial, False, "alcanzó el máximo de iteraciones")
            x = x_nuevo


def secante(f, x0, x1, tol=TOL, max_iter=MAX_ITER):
    with np.errstate(all="ignore"):
        f0, f1 = f(x0), f(x1)
        if _invalido(x0, f0) or _invalido(x1, f1):
            return _resultado([], False, "no aplica: estimación fuera del dominio")
        historial = []
        while True:
            if f1 == f0:
                return _resultado(historial, False, "falló: f(x1) = f(x0) (división por cero)")
            x2 = x1 - f1 * (x1 - x0) / (f1 - f0)
            f2 = f(x2)
            if _invalido(x2, f2):
                return _resultado(historial, False, "falló: salió del dominio")
            historial.append(x2)
            if abs(x2) > LIMITE_DIVERGENCIA:
                return _resultado(historial, False, "divergió")
            if _debe_parar(f2, x2, x1, tol):
                return _resultado(historial, True, "convergió")
            if len(historial) >= max_iter:
                return _resultado(historial, False, "alcanzó el máximo de iteraciones")
            x0, f0 = x1, f1
            x1, f1 = x2, f2


def newton(f, df, x0, tol=TOL, max_iter=MAX_ITER):
    with np.errstate(all="ignore"):
        historial = []
        x = x0
        while True:
            fx, dfx = f(x), df(x)
            if _invalido(x, fx):
                return _resultado(historial, False, "falló: salió del dominio")
            if abs(dfx) < CERO_DERIVADA:
                return _resultado(historial, False, "falló: f'(x) = 0")
            x_nuevo = x - fx / dfx
            f_nuevo = f(x_nuevo)
            if _invalido(x_nuevo, f_nuevo):
                return _resultado(historial, False, "falló: salió del dominio")
            historial.append(x_nuevo)
            if abs(x_nuevo) > LIMITE_DIVERGENCIA:
                return _resultado(historial, False, "divergió")
            if _debe_parar(f_nuevo, x_nuevo, x, tol):
                return _resultado(historial, True, "convergió")
            if len(historial) >= max_iter:
                return _resultado(historial, False, "alcanzó el máximo de iteraciones")
            x = x_nuevo


def newton_mejorado(f, df, d2f, x0, tol=TOL, max_iter=MAX_ITER):
    """Newton-Raphson modificado para raíces múltiples:
    x_(n+1) = x_n - f·f' / (f'^2 - f·f'')"""
    with np.errstate(all="ignore"):
        historial = []
        x = x0
        while True:
            fx, dfx, d2fx = f(x), df(x), d2f(x)
            if _invalido(x, fx):
                return _resultado(historial, False, "falló: salió del dominio")
            denominador = dfx**2 - fx * d2fx
            if abs(denominador) < CERO_DERIVADA:
                return _resultado(historial, False, "falló: denominador = 0")
            x_nuevo = x - fx * dfx / denominador
            f_nuevo = f(x_nuevo)
            if _invalido(x_nuevo, f_nuevo):
                return _resultado(historial, False, "falló: salió del dominio")
            historial.append(x_nuevo)
            if abs(x_nuevo) > LIMITE_DIVERGENCIA:
                return _resultado(historial, False, "divergió")
            if _debe_parar(f_nuevo, x_nuevo, x, tol):
                return _resultado(historial, True, "convergió")
            if len(historial) >= max_iter:
                return _resultado(historial, False, "alcanzó el máximo de iteraciones")
            x = x_nuevo


# Utilidades
def ejecutar_metodos(funcion, a=None, b=None, x0=None, x1=None, tol=TOL, max_iter=MAX_ITER):
    """Aplica los seis métodos a una función con su ambiente controlado
    (o con el intervalo / estimación que se pase como argumento)."""
    a = funcion["a"] if a is None else a
    b = funcion["b"] if b is None else b
    x0 = funcion["x0"] if x0 is None else x0
    x1 = funcion["x1"] if x1 is None else x1
    f, df, d2f, g = funcion["f"], funcion["df"], funcion["d2f"], funcion["g"]
    return {
        "biseccion": biseccion(f, a, b, tol, max_iter),
        "falsa_posicion": falsa_posicion(f, a, b, tol, max_iter),
        "punto_fijo": punto_fijo(f, g, x0, tol, max_iter),
        "secante": secante(f, x0, x1, tol, max_iter),
        "newton": newton(f, df, x0, tol, max_iter),
        "newton_mejorado": newton_mejorado(f, df, d2f, x0, tol, max_iter),
    }


def estimar_orden(errores):
    """Orden de convergencia estimado p a partir de e_(n+1) ≈ C · e_n^p.
    Tomando logaritmos: ln e_(n+1) = p · ln e_n + ln C, así que p es la
    pendiente de la recta ajustada (np.polyfit) entre ln e_n y ln e_(n+1).
    Se usan solo errores > 1e-13 (antes del ruido de redondeo)."""
    e = []
    for valor in errores:
        if valor <= 1e-13:
            break
        e.append(valor)
    e = np.array(e)
    if len(e) < 3:
        return np.nan
    pendiente, _ = np.polyfit(np.log(e[:-1]), np.log(e[1:]), 1)
    return float(pendiente)