"""
sensibilidad.py
Mide cómo cambian las iteraciones (y si el método converge) al mover:
  - el intervalo [a, b]   -> bisección y falsa posición
  - la estimación x0      -> punto fijo, secante (x0, x0 + 0,5), Newton y Newton mejorado
  - el despeje g(x)       -> punto fijo en la función mixta
Genera src/data/sensibilidad.csv y los gráficos sensibilidad_intervalo.png,
sensibilidad_x0.png en src/assets/.
"""
import csv

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from funciones import FUNCIONES, g_mixta_alternativa
from metodos import (NOMBRES_METODOS, biseccion, falsa_posicion, newton,
                     newton_mejorado, punto_fijo, secante)
from rutas import CARPETA_ASSETS, CARPETA_DATA

DESPLAZAMIENTO_SECANTE = 0.5
METODOS_CERRADOS = ["biseccion", "falsa_posicion"]
METODOS_ABIERTOS = ["punto_fijo", "secante", "newton", "newton_mejorado"]
COLORES = {
    "biseccion": "#1f77b4", "falsa_posicion": "#ff7f0e", "punto_fijo": "#2ca02c",
    "secante": "#d62728", "newton": "#9467bd", "newton_mejorado": "#8c564b",
}


def calcular_sensibilidad():
    filas = []
    for funcion in FUNCIONES:
        f, df, d2f, g = funcion["f"], funcion["df"], funcion["d2f"], funcion["g"]
        for a, b in funcion["intervalos_prueba"]:
            for metodo, resultado in (
                ("biseccion", biseccion(f, a, b)),
                ("falsa_posicion", falsa_posicion(f, a, b)),
            ):
                filas.append(_fila(funcion, metodo, "intervalo", f"[{a:g}, {b:g}]", resultado))
        for x0 in funcion["x0_prueba"]:
            for metodo, resultado in (
                ("punto_fijo", punto_fijo(f, g, x0)),
                ("secante", secante(f, x0, x0 + DESPLAZAMIENTO_SECANTE)),
                ("newton", newton(f, df, x0)),
                ("newton_mejorado", newton_mejorado(f, df, d2f, x0)),
            ):
                filas.append(_fila(funcion, metodo, "x0", f"{x0:g}", resultado))
        if funcion["clave"] == "mixta":
            for x0 in funcion["x0_prueba"]:
                resultado = punto_fijo(f, g_mixta_alternativa, x0)
                fila = _fila(funcion, "punto_fijo", "despeje g(x) = cos²(x)", f"{x0:g}", resultado)
                filas.append(fila)
    return filas


def _fila(funcion, metodo, variable, valor, resultado):
    return {
        "funcion": funcion["categoria"],
        "clave": funcion["clave"],
        "metodo": NOMBRES_METODOS[metodo],
        "metodo_clave": metodo,
        "variable": variable,
        "valor_inicial": valor,
        "iteraciones": resultado["iteraciones"],
        "raiz": "" if np.isnan(resultado["raiz"]) else f"{resultado['raiz']:.10f}",
        "convergio": resultado["convergio"],
        "estado": resultado["estado"],
    }


def guardar_csv(filas):
    ruta = CARPETA_DATA / "sensibilidad.csv"
    columnas = ["funcion", "metodo", "variable", "valor_inicial", "iteraciones", "raiz", "convergio", "estado"]
    with open(ruta, "w", newline="", encoding="utf-8") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=columnas, extrasaction="ignore")
        escritor.writeheader()
        escritor.writerows(filas)
    print(f"  CSV generado: {ruta.name}")


def _grafico_barras(filas, variable, metodos, titulo, etiqueta_x, nombre_archivo):
    fig, ejes = plt.subplots(2, 3, figsize=(17, 9.5))
    for eje, funcion in zip(ejes.flat, FUNCIONES):
        datos = [fila for fila in filas if fila["clave"] == funcion["clave"] and fila["variable"] == variable]
        valores = list(dict.fromkeys(fila["valor_inicial"] for fila in datos))
        posiciones = np.arange(len(valores))
        ancho = 0.8 / len(metodos)
        for i, metodo in enumerate(metodos):
            for j, valor in enumerate(valores):
                fila = next(f for f in datos if f["metodo_clave"] == metodo and f["valor_inicial"] == valor)
                x = posiciones[j] + (i - (len(metodos) - 1) / 2) * ancho
                if fila["convergio"]:
                    eje.bar(x, fila["iteraciones"], ancho, color=COLORES[metodo])
                    eje.text(x, fila["iteraciones"] + 1, str(fila["iteraciones"]),
                             ha="center", va="bottom", fontsize=7)
                else:
                    eje.bar(x, 0.6, ancho, color="none", edgecolor=COLORES[metodo], hatch="//")
                    eje.text(x, 1.5, "✗", ha="center", va="bottom", fontsize=10, color="red")
        eje.set_xticks(posiciones)
        eje.set_xticklabels(valores, fontsize=8)
        eje.set_title(f"{funcion['categoria']}\n{funcion['expresion']}", fontsize=10)
        eje.set_xlabel(etiqueta_x)
        eje.set_ylabel("Iteraciones")
        eje.grid(axis="y", alpha=0.3)
        eje.set_ylim(top=max(eje.get_ylim()[1] * 1.12, 10))
    manejadores = [plt.Rectangle((0, 0), 1, 1, color=COLORES[m]) for m in metodos]
    manejadores.append(plt.Rectangle((0, 0), 1, 1, fill=False, hatch="//", edgecolor="gray"))
    etiquetas = [NOMBRES_METODOS[m] for m in metodos] + ["✗ no converge / no aplica"]
    fig.legend(manejadores, etiquetas, loc="lower center", ncol=len(etiquetas), fontsize=10)
    fig.suptitle(titulo, fontsize=14)
    fig.tight_layout(rect=(0, 0.05, 1, 0.95))
    ruta = CARPETA_ASSETS / nombre_archivo
    fig.savefig(ruta, dpi=130)
    plt.close(fig)
    print(f"  Gráfico generado: {ruta.name}")


def graficar(filas):
    _grafico_barras(filas, "intervalo", METODOS_CERRADOS,
                    "Sensibilidad al intervalo inicial [a, b] (tol = 1e-6, máx. 100 iteraciones)",
                    "Intervalo [a, b]", "sensibilidad_intervalo.png")
    _grafico_barras(filas, "x0", METODOS_ABIERTOS,
                    "Sensibilidad a la estimación inicial x0 (secante usa x1 = x0 + 0,5)",
                    "Estimación inicial x0", "sensibilidad_x0.png")


def imprimir(filas):
    print(f"\n{'Función':<26}{'Método':<17}{'Variable':<24}{'Inicio':>12}{'Iter':>6}  Estado")
    print("-" * 110)
    for fila in filas:
        print(f"{fila['funcion']:<26}{fila['metodo']:<17}{fila['variable']:<24}"
              f"{fila['valor_inicial']:>12}{fila['iteraciones']:>6}  {fila['estado']}")


if __name__ == "__main__":
    filas = calcular_sensibilidad()
    guardar_csv(filas)
    graficar(filas)
    imprimir(filas)