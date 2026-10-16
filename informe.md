# Informe: La raíz que se esconde

**Evaluación 2: búsqueda de raíces y análisis de convergencia**
Universidad Católica del Maule Integrante: Belén Marcela Parra Fierro

> Todos los números de este informe salen de `src/data/resumen_convergencia.csv` y `src/data/sensibilidad.csv`, y todos los gráficos de `src/assets/`. Se regeneran con `python src/scripts/main.py`.

---

## 1. Ambiente controlado

Para todas las funciones: **tolerancia = 1e-6**, **tope = 100 iteraciones**, criterio de parada `|f(xₙ)| < tol` o `|xₙ − xₙ₋₁| < tol`. El error se mide como `|xₙ − raíz|`, usando como raíz de referencia la bisección llevada al límite de la precisión de máquina (o `x = 2` exacto en la raíz doble).

| Función       | [a, b]     | f(a)·f(b)        | x0  | x1  | g(x) punto fijo        | Raíz de referencia | Demostración                         |
| -------------- | ---------- | ----------------- | --- | --- | ---------------------- | ------------------- | ------------------------------------- |
| x³ − x − 2  | [1, 2]     | −8,000           | 1   | 2   | ∛(x+2)                | 1,521379706805      | Bolzano ✔                            |
| (x − 2)²     | [1,2; 2,8] | **+0,4096** | 1,2 | 1,4 | (x²+4)/4              | 2                   | Tangencia ✔: f(2)=0, f'(2)=0, f ≥ 0 |
| ln(x) + x − 4 | [2, 3]     | −0,1289          | 2   | 3   | 4 − ln x              | 2,926271062443      | Bolzano ✔                            |
| e^(−x) − x   | [0, 1]     | −0,6321          | 0   | 1   | e^(−x)                | 0,567143290410      | Bolzano ✔                            |
| cos(x) − x    | [0, 1]     | −0,4597          | 0   | 1   | cos x                  | 0,739085133215      | Bolzano ✔                            |
| √x − cos(x)  | [0,1; 1]   | −0,3120          | 0,5 | 1   | x − 0,5(√x − cos x) | 0,641714370873      | Bolzano ✔                            |

---

## 2. Resultados

Iteraciones hasta cumplir tol = 1e-6 (N/A = no aplica; X = no convergió en 100 iteraciones):

| Función       | Bisección | Falsa posición | Punto fijo | Secante | Newton | Newton mejorado |
| -------------- | ---------- | --------------- | ---------- | ------- | ------ | --------------- |
| x³ − x − 2  | 20         | 12              | 8          | 6       | 5      | 5               |
| (x − 2)²     | N/A        | N/A             | 100 X      | 14      | 10     | **1**     |
| ln(x) + x − 4 | 19         | 4               | 14         | 3       | 3      | 3               |
| e^(−x) − x   | 20         | 7               | 25         | 4       | 3      | 3               |
| cos(x) − x    | 20         | 5               | 34         | 4       | 4      | 4               |
| √x − cos(x)  | 20         | 4               | 13         | 3       | 2      | 2               |

![Resumen Iteraciones](scr\assets\resumen_iteraciones.png)

Orden de convergencia estimado (pendiente de la recta ajustada a ln eₙ₊₁ vs ln eₙ, `estimar_orden()` en `metodos.py`):

| Función       | Bisección | Falsa posición | Punto fijo | Secante        | Newton         | Newton mejorado  |
| -------------- | ---------- | --------------- | ---------- | -------------- | -------------- | ---------------- |
| x³ − x − 2  | 0,96       | 1,00            | 1,00       | 1,63           | 1,96           | 2,01             |
| (x − 2)²     | —         | —              | 0,96       | **1,00** | **1,00** | exacta en 1 paso |
| ln(x) + x − 4 | 0,86       | 1,00            | 1,00       | 1,52           | 2,00           | 1,99             |
| e^(−x) − x   | 0,96       | 1,00            | 1,00       | 1,63           | 2,01           | 1,98             |
| cos(x) − x    | 0,98       | 1,00            | 1,00       | 1,61           | 1,97           | 2,03             |
| √x − cos(x)  | 1,03       | 1,00            | 1,00       | 2,32*          | —*            | —*              |

\* En la mixta, Newton y Newton mejorado llegaron en 2 iteraciones y la secante en 3. Con tan pocos puntos el orden no se puede estimar o queda poco confiable.

![Convergencia de todas las funciones](scr\assets\convergencia_todas.png)

---

## 3. Preguntas de convergencia

### 3.1 ¿Qué método convergió en menos iteraciones en cada función? ¿Por qué?

| Función       | Ganador(es)                       | Iteraciones |
| -------------- | --------------------------------- | ----------- |
| x³ − x − 2  | Newton y Newton mejorado          | 5           |
| (x − 2)²     | Newton mejorado                   | 1           |
| ln(x) + x − 4 | Secante, Newton y Newton mejorado | 3           |
| e^(−x) − x   | Newton y Newton mejorado          | 3           |
| cos(x) − x    | Secante, Newton y Newton mejorado | 4           |
| √x − cos(x)  | Newton y Newton mejorado          | 2           |

En las raíces simples ganan los métodos que usan información de la **pendiente**. Newton usa f'(x) exacta y converge cuadráticamente: el número de cifras correctas aproximadamente se duplica en cada paso. En `convergencia_polinomica_simple.png` el error de Newton pasa de ~1e-4 a ~3e-9 en una sola iteración. La secante aproxima la derivada con dos puntos, por eso queda pegada a Newton (1 iteración más en promedio) sin necesitar f'.

En la raíz doble gana Newton mejorado por lejos (1 iteración contra 10 de Newton). Su fórmula `x − f·f' / (f'² − f·f'')` está pensada para raíces múltiples, y para (x − 2)² el paso es exactamente `x − 2`, así que llega a la raíz en un solo salto.

### 3.2 ¿Qué orden de convergencia tiene cada método y cómo se refleja en el gráfico |error| vs iteración?

| Método         | Orden teórico                                  | Orden medido (raíces simples) | Cómo se ve en el gráfico (escala log)                                                                                                                          |
| --------------- | ----------------------------------------------- | ------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Bisección      | lineal (el intervalo se reduce a la mitad)      | 0,86 – 1,03                   | Bajada general recta con **dientes de sierra**: el punto medio a veces queda más lejos de la raíz que el anterior aunque el intervalo siempre se achica. |
| Falsa posición | lineal                                          | 1,00                           | **Línea recta** con pendiente constante. Un extremo del intervalo queda fijo y el error se reduce por un factor constante.                                |
| Punto fijo      | lineal, con razón \|g'(r)\|                    | 1,00                           | **Recta** cuya pendiente depende de \|g'(r)\|. En cos(x) − x, \|g'(r)\| = sin(0,739) ≈ 0,674 y el error baja solo ~33 % por paso (34 iteraciones).       |
| Secante         | superlineal, φ ≈ 1,618                        | 1,52 – 1,63                   | Curva que **se dobla hacia abajo**, cada vez más empinada, pero menos abrupta que Newton.                                                                 |
| Newton          | cuadrático (2)                                 | 1,96 – 2,01                   | **Caída en picada**: en log el error se duplica en exponente (1e-2 → 1e-4 → 1e-9).                                                                      |
| Newton mejorado | cuadrático (2), también en raíces múltiples | 1,98 – 2,03                   | Igual que Newton en raíces simples. En la doble llega en 1 paso.                                                                                                |

Las mediciones calzan con la teoría: secante entre 1,52 y 1,63 (teórico 1,618) y Newton entre 1,96 y 2,01 (teórico 2).

### 3.3 ¿Qué métodos requieren un intervalo con cambio de signo y cuáles no?

- **Requieren cambio de signo (cerrados):** bisección y falsa posición. En el código, si `f(a)·f(b) > 0` devuelven `"no aplica"` sin iterar, que es exactamente lo que pasó en (x − 2)² con [1,2; 2,8], [1, 3] y [0, 5] (`sensibilidad.csv`).
- **No lo requieren (abiertos):** punto fijo (necesita x0 y un despeje con |g'(r)| < 1), secante (necesita x0 y x1, no tienen que encerrar la raíz), Newton y Newton mejorado (necesitan x0 y las derivadas).

### 3.4 En la función que toca el eje x (raíz doble): ¿qué métodos fallan o no aplican y cuál se comporta mejor? ¿Por qué?

![Convergencia raíz doble](scr\assets\convergencia_polinomica_doble.png)

| Método                   | Resultado                                                   | Explicación                                                                                                                                                                                                                       |
| ------------------------- | ----------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Bisección                | **No aplica**                                         | f(1,2)·f(2,8) = 0,4096 > 0. Como f(x) = (x−2)² ≥ 0 en todo ℝ, **no existe ningún intervalo** con cambio de signo.                                                                                                      |
| Falsa posición           | **No aplica**                                         | Misma razón.                                                                                                                                                                                                                      |
| Punto fijo                | **Falla**: 100 iteraciones y el error sigue en 3,7e-2 | g(x) = (x²+4)/4 tiene g'(2) = 1, justo en el límite: el error baja de 0,25 (it. 10) a 0,069 (it. 50) a 0,037 (it. 100), sublineal. Desde x0 ≥ 3 diverge (`sensibilidad.csv`).                                                 |
| Secante                   | Converge en 14 it., pero **pierde su orden**: 1,00    | El error se multiplica por ≈ 0,618 en cada paso (4,6e-3 → 2,8e-3 → 1,8e-3 → 1,1e-3 → 6,7e-4).                                                                                                                                 |
| Newton                    | Converge en 10 it., pero **pierde su orden**: 1,00    | El error se divide exactamente por 2 en cada paso (0,1 → 0,05 → 0,025 → … → 7,8e-4). En una raíz de multiplicidad m, Newton es lineal con razón (m−1)/m = 1/2.                                                             |
| **Newton mejorado** | **1 iteración, error 0**                             | Con f = (x−2)², f' = 2(x−2) y f'' = 2, el paso f·f'/(f'² − f·f'') = (x−2), así que x₁ = 2 exacto. La fórmula equivale a aplicar Newton a u(x) = f/f', que tiene una raíz **simple** donde f tiene una múltiple. |

Hay otro detalle en los datos. Secante y Newton "convergieron" con errores de **6,7e-4 y 7,8e-4**, casi mil veces más grandes que la tolerancia. Pararon porque `|f(x)| < 1e-6`, pero en una raíz doble f(x) = (x−2)², así que |f| < 1e-6 solo garantiza |x − 2| < 1e-3. Cerca de una tangencia la curva es tan plana que **un |f| pequeño no significa estar cerca de la raíz**. Por eso conviene usar un criterio sobre |xₙ − xₙ₋₁| (o ambos) cuando se sospecha una raíz múltiple.

### 3.5 ¿Cómo influyen el intervalo inicial y la estimación inicial en la cantidad de iteraciones y en si el método converge?

![Sensibilidad al intervalo](scr\assets\sensibilidad_intervalo.png)

**Intervalo (métodos cerrados):**

- **Bisección es muy predecible.** Sus iteraciones dependen casi solo del ancho, ≈ log₂((b−a)/tol). En x³ − x − 2: [1,5; 1,6] → 17, [1, 2] → 20, [−2, 5] → 23, [1, 10] → 23. Multiplicar el ancho por 9 solo suma 3 iteraciones.
- **Falsa posición es muy sensible a la forma de la curva.** En x³ − x − 2 pasó de 5 iteraciones ([1,5; 1,6]) a 30 ([0, 3]), 91 ([−2, 5]) y **no convergió** en [1, 10] (100 it.), mientras la bisección necesitó 23. En e^(−x) − x pasó lo mismo con [−5, 10] y [−10, 20]. La causa es la convexidad: un extremo queda "pegado" y la recta secante se acerca a la raíz por un solo lado con pasos cada vez más chicos. Con intervalos chicos, en cambio, es la más rápida de los cerrados (2–5 iteraciones).

![Sensibilidad a x0](scr\assets\sensibilidad_x0.png)

**Estimación inicial (métodos abiertos):**

- **Cerca de un punto con f'(x) ≈ 0, Newton se pierde.** En x³ − x − 2, f'(x) = 0 en x ≈ 0,577. Con x0 = 0,58 Newton tardó 18 iteraciones y con x0 = 0 tardó **30** (contra 2 con x0 = 1,5): el primer paso lo manda lejos y vaga antes de engancharse.
- **Lejos de la raíz Newton puede no converger.** En cos(x) − x con x0 = 10 Newton **no convergió** en 100 iteraciones (f'(10) = −sin 10 − 1 ≈ −0,46, salta y oscila), mientras la secante desde el mismo punto llegó en 7.
- **Los problemas de dominio también cuentan.** En √x − cos(x), desde x0 = 5 y x0 = 10 secante, Newton y Newton mejorado **fallaron** en los seis casos: o una iteración cayó en x < 0, donde √x no existe, o se quedaron oscilando hasta las 100 iteraciones. Newton mejorado además salió del dominio en ln(x) + x − 4 (x0 = 0,5 y 0,1) y en la mixta (x0 = 0,1 y 0,01): cerca de 0, f'' es enorme y el paso resulta demasiado largo. Punto fijo, en cambio, convergió desde **todos** los x0 de la mixta, porque g(x) = x − 0,5·f(x) da pasos cortos.
- **Punto fijo depende más del despeje que del x0.** En la mixta, el despeje "natural" g(x) = cos²(x) **no convergió en ningún x0** (7 de 7 llegaron a 100 iteraciones) porque |g'(r)| = |sin 2r| ≈ 0,96. El despeje relajado g(x) = x − 0,5·(√x − cos x) tiene |g'(r)| ≈ 0,39 y convergió en 13–22 iteraciones desde cualquier punto. En cos(x) − x y e^(−x) − x, el número de iteraciones casi no cambió con x0 (32–35 y 24–27), porque lo que manda es |g'(r)|.

### 3.6 ¿Qué método recomiendan según el tipo de función?

| Tipo de función                          | Recomendación                                                                    | Justificación con datos                                                                                                                        |
| ----------------------------------------- | --------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| Polinómica con raíz simple              | **Newton** (o Newton mejorado) partiendo dentro de un intervalo con Bolzano | 5 iteraciones contra 20 de bisección. Usar Bolzano para elegir x0 evita los x0 cercanos a f' = 0, que lo llevaron a 18–30 iteraciones.        |
| Raíz doble / múltiple (toca el eje)     | **Newton mejorado**                                                         | Único con orden cuadrático: 1 iteración. Bisección y falsa posición no aplican, Newton y secante bajan a orden 1 y punto fijo no converge. |
| Logarítmica                              | **Secante**                                                                 | 3 iteraciones, igual que Newton, sin derivar. Newton mejorado falló cerca de x = 0 por el dominio de ln.                                       |
| Exponencial                               | **Newton**                                                                  | 3–5 iteraciones desde cualquier x0 probado (−2 a 10). La derivada es fácil y nunca se anula.                                                 |
| Trigonométrica                           | **Secante** si x0 puede quedar lejos; Newton si x0 está cerca              | Ambos 4 it. desde [0, 1], pero desde x0 = 10 Newton no convergió y la secante sí (7 it.).                                                     |
| Mixta con dominio restringido (√x, ln x) | **Bisección o falsa posición** para acercarse, después secante o Newton  | Los abiertos salieron del dominio desde x0 grandes. Falsa posición convergió en todos los intervalos (3–9 it.).                              |
| Cuando no se sabe nada de la función     | **Bisección**                                                              | Nunca falló con un intervalo válido (≈ 20 it. siempre). Es la más lenta, pero la más segura.                                               |

---

## 4. Conclusión

**¿Qué método elegiríamos para cada tipo de función y por qué?** El compromiso entre velocidad y robustez se ve directo en los datos. Newton y Newton mejorado son los más rápidos (2–5 iteraciones, orden ≈ 2 medido), pero fueron también los que más fallaron en `sensibilidad.csv`: x0 lejano en cos(x) − x, f' ≈ 0 en x³ − x − 2 y salidas del dominio en √x − cos x y ln x + x − 4. La bisección es el extremo opuesto: siempre ~20 iteraciones, nunca falló con Bolzano, pero es de 4 a 10 veces más lenta. La secante quedó como el mejor equilibrio: orden ≈ 1,6, sin derivadas, y convergió en casos donde Newton no (cos x − x desde x0 = 10). Nuestra elección práctica es **usar Bolzano o bisección para ubicar la raíz y luego Newton o secante para refinarla**. Para raíces múltiples, **Newton mejorado**. Punto fijo solo lo usaríamos si se puede garantizar un despeje con |g'(r)| claramente menor que 1.

**¿Qué ocurrió en la raíz doble y qué dice eso sobre "tener raíz" frente a "cambiar de signo"?** La función (x − 2)² **tiene raíz** en x = 2, pero **no cambia de signo** en ningún intervalo: f(a)·f(b) = 0,4096 > 0. Bolzano es una condición *suficiente* para que exista una raíz, no *necesaria*. Por eso bisección y falsa posición ni siquiera pudieron partir, aunque la raíz estaba ahí. Además, Newton y secante bajaron de orden 2 y 1,6 a orden 1 (razones 0,5 y 0,618), y la tolerancia en |f| se volvió engañosa: pararon con errores de ~7e-4 aunque |f| < 1e-6. Solo Newton mejorado, que trata la multiplicidad, la encontró exacta en 1 iteración.

**¿Cómo cambió el número de iteraciones al mover el intervalo o la estimación inicial?** En la bisección casi nada: de 17 a 23 iteraciones al pasar de un intervalo de ancho 0,1 a uno de ancho 9, porque crece con el logaritmo del ancho. En la falsa posición mucho: de 5 a 100 (sin converger) en x³ − x − 2 al ensanchar el intervalo. En Newton la estimación inicial lo es todo: de 2 iteraciones (x0 = 1,5) a 30 (x0 = 0) en x³ − x − 2, y de 4 a no converger en cos(x) − x. En punto fijo el x0 casi no influyó (variaciones de ±2 iteraciones). Lo que decidió si convergía o no fue el despeje g(x): cos²(x) falló en 7 de 7 casos y x − 0,5·f(x) funcionó en 7 de 7.
