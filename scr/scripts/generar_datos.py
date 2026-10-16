"""
generar_datos.py
1) Genera un CSV por función con columnas (x, f(x)) en src/data/.
2) Demuestra el ambiente controlado: Bolzano f(a)·f(b) < 0 para las raíces
   simples y tangencia al eje (f(r) = 0, f'(r) = 0, f >= 0) para la raíz doble.
   Guarda el resultado en src/data/ambiente.csv.
"""
import csv

import numpy as np

from funciones import FUNCIONES, TOL, MAX_ITER, raiz_referencia
from rutas import CARPETA_DATA

PUNTOS = 400


def generar_csv_funciones():
    for funcion in FUNCIONES:
        x = np.linspace(*funcion["rango_grafico"], PUNTOS)
        y = funcion["f"](x)
        datos = np.column_stack((x, y))
        ruta = CARPETA_DATA / f"{funcion['clave']}.csv"
        np.savetxt(ruta, datos, delimiter=",", header="x,f(x)", comments="", fmt="%.10f")
        print(f"  CSV generado: {ruta.name}")


def verificar_ambiente():
    filas = []
    for funcion in FUNCIONES:
        f, df = funcion["f"], funcion["df"]
        a, b = funcion["a"], funcion["b"]
        fa, fb = f(a), f(b)
        raiz = raiz_referencia(funcion)

        if funcion["raiz_doble"]:
            x = np.linspace(*funcion["rango_grafico"], PUNTOS)
            minimo = float(np.min(f(x)))
            demostrado = abs(f(raiz)) < 1e-12 and abs(df(raiz)) < 1e-12 and minimo >= 0
            demostracion = (
                f"Tangencia: f({raiz:g}) = {f(raiz):g}, f'({raiz:g}) = {df(raiz):g}, "
                f"min f(x) en el rango = {minimo:g} >= 0 (no cruza el eje)"
            )
        else:
            demostrado = fa * fb < 0
            demostracion = f"Bolzano: f(a)·f(b) = {fa * fb:.6f} < 0"

        filas.append({
            "funcion": funcion["categoria"],
            "expresion": funcion["expresion"],
            "a": a, "b": b,
            "f(a)": round(float(fa), 8), "f(b)": round(float(fb), 8),
            "f(a)*f(b)": round(float(fa * fb), 8),
            "x0": funcion["x0"], "x1": funcion["x1"],
            "g(x) punto fijo": funcion["g_expresion"],
            "tolerancia": TOL, "max_iter": MAX_ITER,
            "raiz_referencia": f"{raiz:.12f}",
            "demostracion": demostracion,
            "raiz_en_rango": demostrado,
        })
        print(f"  {funcion['categoria']:<26} {demostracion}  -> {'OK' if demostrado else 'FALLA'}")

    ruta = CARPETA_DATA / "ambiente.csv"
    with open(ruta, "w", newline="", encoding="utf-8") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=list(filas[0].keys()))
        escritor.writeheader()
        escritor.writerows(filas)
    print(f"  CSV generado: {ruta.name}")


if __name__ == "__main__":
    print("Generando CSV (x, f(x))...")
    generar_csv_funciones()
    print("Verificando ambiente controlado...")
    verificar_ambiente()
