"""rutas.py: carpetas de salida del proyecto, aparte se crean si no llegaran a existir."""
from pathlib import Path

CARPETA_SRC = Path(__file__).resolve().parents[1]
CARPETA_DATA = CARPETA_SRC / "data"
CARPETA_HISTORIALES = CARPETA_DATA / "historiales"
CARPETA_ASSETS = CARPETA_SRC / "assets"

for carpeta in (CARPETA_DATA, CARPETA_HISTORIALES, CARPETA_ASSETS):
    carpeta.mkdir(parents=True, exist_ok=True)