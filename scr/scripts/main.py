# Belén M. Parra Fierro

"""
main.py — ejecuta todo el flujo en orden:
  1. CSV (x, f(x)) y verificación del ambiente controlado
  2. Métodos sobre cada función + resumen de convergencia
  3. Gráficos de funciones, convergencia y resumen
  4. Análisis de sensibilidad (intervalo / x0 / despeje g)
"""
import convergencia
import generar_datos
import graficos
import sensibilidad
from funciones import FUNCIONES

print("1. Datos y ambiente controlado")
generar_datos.generar_csv_funciones()
generar_datos.verificar_ambiente()

print("\n2. Convergencia de los métodos")
resultados = convergencia.calcular_resultados()
convergencia.guardar_resumen(resultados)
convergencia.guardar_historiales(resultados)
convergencia.imprimir_tabla(resultados)

print("3. Gráficos")
for funcion in FUNCIONES:
    graficos.graficar_funcion(funcion, resultados[funcion["clave"]]["raiz_ref"])
graficos.graficar_convergencia(resultados)
graficos.graficar_resumen(resultados)

print("\n4. Sensibilidad")
filas = sensibilidad.calcular_sensibilidad()
sensibilidad.guardar_csv(filas)
sensibilidad.graficar(filas)
sensibilidad.imprimir(filas)

print("\nDatos listos para revisar en src/data/ y src/assets/. :)")