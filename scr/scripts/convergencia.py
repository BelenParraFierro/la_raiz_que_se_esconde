"""
convergencia.py
Aplica los seis métodos a cada función con su ambiente controlado y guarda:
  - src/data/resumen_convergencia.csv  (iteraciones, raíz, error, orden estimado)
  - src/data/historiales/<funcion>.csv (x_n, f(x_n), |error| por iteración)
"""
import csv

import numpy as np

from funciones import FUNCIONES, raiz_referencia
from metodos import NOMBRES_METODOS, ejecutar_metodos, estimar_orden
from rutas import CARPETA_DATA, CARPETA_HISTORIALES


def calcular_resultados():
    """Devuelve {clave_funcion: {"raiz_ref": r, "metodos": {metodo: resultado}}}"""
    resultados = {}
    for funcion in FUNCIONES:
        raiz = raiz_referencia(funcion)
        metodos = ejecutar_metodos(funcion)
        for resultado in metodos.values():
            resultado["errores"] = np.abs(resultado["historial"] - raiz)
            resultado["orden"] = estimar_orden(resultado["errores"])
        resultados[funcion["clave"]] = {"raiz_ref": raiz, "metodos": metodos}
    return resultados


def guardar_resumen(resultados):
    ruta = CARPETA_DATA / "resumen_convergencia.csv"
    with open(ruta, "w", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow([
            "funcion", "metodo", "iteraciones", "raiz", "error_absoluto",
            "f(raiz)", "orden_estimado", "convergio", "estado",
        ])
        for funcion in FUNCIONES:
            datos = resultados[funcion["clave"]]
            for metodo, r in datos["metodos"].items():
                if r["iteraciones"] > 0:
                    raiz = f"{r['raiz']:.10f}"
                    error = f"{r['errores'][-1]:.3e}"
                    f_raiz = f"{funcion['f'](r['raiz']):.3e}"
                else:
                    raiz = error = f_raiz = ""
                orden = "" if np.isnan(r["orden"]) else f"{r['orden']:.3f}"
                escritor.writerow([
                    funcion["categoria"], NOMBRES_METODOS[metodo], r["iteraciones"],
                    raiz, error, f_raiz, orden, r["convergio"], r["estado"],
                ])
    print(f"  CSV generado: {ruta.name}")


def guardar_historiales(resultados):
    for funcion in FUNCIONES:
        datos = resultados[funcion["clave"]]
        ruta = CARPETA_HISTORIALES / f"{funcion['clave']}.csv"
        with open(ruta, "w", newline="", encoding="utf-8") as archivo:
            escritor = csv.writer(archivo)
            escritor.writerow(["metodo", "iteracion", "x_n", "f(x_n)", "error_absoluto", "|x_n - x_(n-1)|"])
            for metodo, r in datos["metodos"].items():
                anterior = None
                for i, x in enumerate(r["historial"], start=1):
                    paso = "" if anterior is None else f"{abs(x - anterior):.3e}"
                    escritor.writerow([
                        NOMBRES_METODOS[metodo], i, f"{x:.12f}",
                        f"{funcion['f'](x):.3e}", f"{r['errores'][i - 1]:.3e}", paso,
                    ])
                    anterior = x
        print(f"  Historial generado: historiales/{ruta.name}")


def imprimir_tabla(resultados):
    print(f"\n{'Función':<26}{'Método':<17}{'Iter':>5}  {'Raíz':>14}  {'Error':>10}  Estado")
    print("-" * 100)
    for funcion in FUNCIONES:
        for metodo, r in resultados[funcion["clave"]]["metodos"].items():
            raiz = f"{r['raiz']:.10f}" if r["iteraciones"] else "-"
            error = f"{r['errores'][-1]:.2e}" if r["iteraciones"] else "-"
            print(f"{funcion['categoria']:<26}{NOMBRES_METODOS[metodo]:<17}{r['iteraciones']:>5}  "
                  f"{raiz:>14}  {error:>10}  {r['estado']}")
        print()


if __name__ == "__main__":
    resultados = calcular_resultados()
    guardar_resumen(resultados)
    guardar_historiales(resultados)
    imprimir_tabla(resultados)