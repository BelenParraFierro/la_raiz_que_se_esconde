"""
graficos.py
Genera en src/assets/:
  - funcion_<clave>.png       cada función con su raíz marcada (Bolzano o tangencia)
  - convergencia_<clave>.png  |error| vs iteración (escala log) comparando métodos
  - convergencia_todas.png    las seis curvas de convergencia en una sola figura
  - resumen_iteraciones.png   iteraciones por método y función
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from convergencia import calcular_resultados
from funciones import FUNCIONES, MAX_ITER, TOL
from metodos import NOMBRES_METODOS
from rutas import CARPETA_ASSETS
from sensibilidad import COLORES

MARCADORES = {
    "biseccion": "o", "falsa_posicion": "s", "punto_fijo": "^",
    "secante": "D", "newton": "v", "newton_mejorado": "P",
}
PISO_ERROR = 1e-17  # para poder dibujar error = 0 en escala log


def graficar_funcion(funcion, raiz):
    f = funcion["f"]
    x = np.linspace(*funcion["rango_grafico"], 400)
    y = f(x)
    a, b = funcion["a"], funcion["b"]

    fig, eje = plt.subplots(figsize=(8, 5))
    eje.plot(x, y, color="#1f77b4", linewidth=2, label=funcion["expresion"])
    eje.axhline(0, color="black", linewidth=0.8)

    if funcion["raiz_doble"]:
        eje.plot(x, np.zeros_like(x), "--", color="orange", linewidth=1.5,
                 label=f"Recta tangente en x = {raiz:g}:  y = 0  (f'({raiz:g}) = 0)")
        eje.plot(raiz, 0, "r*", markersize=16, label=f"Raíz doble x = {raiz:g} (toca el eje, no cruza)")
        eje.plot([a, b], [f(a), f(b)], "o", color="gray")
        eje.annotate(f"f({a:g}) = {f(a):.2f} > 0", (a, f(a)), textcoords="offset points", xytext=(5, 8))
        eje.annotate(f"f({b:g}) = {f(b):.2f} > 0", (b, f(b)), textcoords="offset points", xytext=(-90, 8))
        eje.set_title(f"{funcion['categoria']} — sin cambio de signo: f(a)·f(b) = {f(a) * f(b):.4f} > 0")
    else:
        eje.axvspan(a, b, color="green", alpha=0.08, label=f"Intervalo [{a:g}, {b:g}]")
        eje.plot([a, b], [f(a), f(b)], "o", color="green")
        eje.annotate(f"f({a:g}) = {f(a):.3f}", (a, f(a)), textcoords="offset points", xytext=(5, -15))
        eje.annotate(f"f({b:g}) = {f(b):.3f}", (b, f(b)), textcoords="offset points", xytext=(-80, 8))
        eje.plot(raiz, 0, "r*", markersize=16, label=f"Raíz x ≈ {raiz:.6f}")
        eje.set_title(f"{funcion['categoria']} — Bolzano: f(a)·f(b) = {f(a) * f(b):.4f} < 0")

    eje.set_xlabel("x")
    eje.set_ylabel("f(x)")
    eje.grid(alpha=0.3)
    eje.legend(loc="best", fontsize=9)
    fig.tight_layout()
    ruta = CARPETA_ASSETS / f"funcion_{funcion['clave']}.png"
    fig.savefig(ruta, dpi=130)
    plt.close(fig)
    print(f"  Gráfico generado: {ruta.name}")


def _dibujar_convergencia(eje, funcion, metodos):
    sin_curva = []
    for metodo, r in metodos.items():
        if r["iteraciones"] == 0:
            sin_curva.append(f"{NOMBRES_METODOS[metodo]}: {r['estado']}")
            continue
        iteraciones = np.arange(1, r["iteraciones"] + 1)
        errores = np.maximum(r["errores"], PISO_ERROR)
        etiqueta = f"{NOMBRES_METODOS[metodo]} ({r['iteraciones']} it.)"
        if not r["convergio"]:
            etiqueta += " ✗"
        eje.semilogy(iteraciones, errores, marker=MARCADORES[metodo], markersize=4,
                     color=COLORES[metodo], label=etiqueta)
    eje.axhline(TOL, color="gray", linestyle=":", label="tol = 1e-6")
    eje.set_xlabel("Iteración n")
    eje.set_ylabel("|error| = |xₙ − raíz|")
    eje.set_title(f"{funcion['categoria']}: {funcion['expresion']}", fontsize=10)
    eje.grid(alpha=0.3, which="both")
    eje.legend(fontsize=7, loc="best")
    if sin_curva:
        eje.text(0.02, 0.02, "\n".join(sin_curva), transform=eje.transAxes,
                 fontsize=7, color="red", va="bottom")


def graficar_convergencia(resultados):
    for funcion in FUNCIONES:
        metodos = resultados[funcion["clave"]]["metodos"]
        fig, eje = plt.subplots(figsize=(8, 5))
        _dibujar_convergencia(eje, funcion, metodos)
        eje.set_title(f"Convergencia |error| vs iteración — {funcion['categoria']}\n{funcion['expresion']}")
        fig.tight_layout()
        ruta = CARPETA_ASSETS / f"convergencia_{funcion['clave']}.png"
        fig.savefig(ruta, dpi=130)
        plt.close(fig)
        print(f"  Gráfico generado: {ruta.name}")

    fig, ejes = plt.subplots(2, 3, figsize=(18, 10))
    for eje, funcion in zip(ejes.flat, FUNCIONES):
        _dibujar_convergencia(eje, funcion, resultados[funcion["clave"]]["metodos"])
    fig.suptitle("Convergencia |error| vs iteración (escala log) — todas las funciones", fontsize=14)
    fig.tight_layout(rect=(0, 0, 1, 0.96))
    ruta = CARPETA_ASSETS / "convergencia_todas.png"
    fig.savefig(ruta, dpi=130)
    plt.close(fig)
    print(f"  Gráfico generado: {ruta.name}")


def graficar_resumen(resultados):
    metodos = list(NOMBRES_METODOS)
    posiciones = np.arange(len(FUNCIONES))
    ancho = 0.8 / len(metodos)
    fig, eje = plt.subplots(figsize=(15, 6.5))
    for i, metodo in enumerate(metodos):
        for j, funcion in enumerate(FUNCIONES):
            r = resultados[funcion["clave"]]["metodos"][metodo]
            x = posiciones[j] + (i - (len(metodos) - 1) / 2) * ancho
            if r["convergio"]:
                eje.bar(x, r["iteraciones"], ancho, color=COLORES[metodo],
                        label=NOMBRES_METODOS[metodo] if j == 0 else None)
                eje.text(x, r["iteraciones"] * 1.08, str(r["iteraciones"]), ha="center", fontsize=8)
            elif r["iteraciones"] == 0:
                eje.text(x, 1.05, "N/A", ha="center", fontsize=7, color="red", rotation=90, va="bottom")
            else:
                eje.bar(x, r["iteraciones"], ancho, color="none", edgecolor=COLORES[metodo], hatch="//")
                eje.text(x, r["iteraciones"] * 1.08, f"{r['iteraciones']}✗", ha="center", fontsize=8, color="red")
    eje.set_yscale("log")
    eje.set_ylim(0.8, MAX_ITER * 2.5)
    eje.set_xticks(posiciones)
    eje.set_xticklabels([f["categoria"] for f in FUNCIONES], fontsize=9)
    eje.set_ylabel("Iteraciones hasta tol = 1e-6 (escala log)")
    eje.set_title("Resumen de iteraciones por método y función   (N/A = no aplica, ✗ = no convergió en 100 it.)")
    eje.grid(axis="y", alpha=0.3, which="both")
    eje.legend(ncol=6, loc="upper center", fontsize=9)
    fig.tight_layout()
    ruta = CARPETA_ASSETS / "resumen_iteraciones.png"
    fig.savefig(ruta, dpi=130)
    plt.close(fig)
    print(f"  Gráfico generado: {ruta.name}")


if __name__ == "__main__":
    resultados = calcular_resultados()
    for funcion in FUNCIONES:
        graficar_funcion(funcion, resultados[funcion["clave"]]["raiz_ref"])
    graficar_convergencia(resultados)
    graficar_resumen(resultados)