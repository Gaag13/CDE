#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
crear_cde_iso19650.py
----------------------
Genera la estructura de carpetas de un Common Data Environment (CDE)
siguiendo la lógica de estados de la ISO 19650-1 / 19650-2:

    WIP (Trabajo en curso) -> SHARED (Compartido) -> PUBLISHED (Publicado) -> ARCHIVED (Archivado)

Referencias usadas para la estructura:
- ISO 19650-1:2018 / ISO 19650-2:2018 (estados del contenedor informativo)
- BS 1192:2007 (origen del flujo WIP -> Shared -> Published -> Archived)
- Guías de implantación BIM (buildingSMART Spain, Espacio BIM, BibLus, 12d Synergy)

Reglas de oro que sigue la estructura:
  * 1.0_WIP    -> Solo el equipo interno (autores) trabaja y edita aquí.
                  Nada de lo que hay en WIP se comparte directamente con
                  terceros ni con el cliente. Aquí vive Revit: central,
                  vínculos, familias, vistas de trabajo, etc.
  * 2.0_COMPARTIDO -> Información ya revisada internamente (check) que se
                  entrega para coordinación entre disciplinas o con
                  consultores externos. No es la entrega oficial.
  * 3.0_PUBLICADO  -> Información aprobada/autorizada formalmente (CRA:
                  Check, Review, Approve). Es lo que se entrega al
                  cliente/comitente. Acceso de escritura restringido.
  * 4.0_ARCHIVADO  -> Histórico de referencia, solo lectura. Guarda
                  versiones superadas y entregas cerradas por hito.

Uso:
    python crear_cde_iso19650.py "Nombre del Proyecto"
    python crear_cde_iso19650.py "Nombre del Proyecto" --ruta "D:/Proyectos"
    python crear_cde_iso19650.py "Nombre del Proyecto" --disciplinas "Arquitectura,Estructuras,Electricas"

Tambien se puede ejecutar sin argumentos (doble clic al .py, o al .exe si se
compila con PyInstaller): en ese caso pedira el nombre del proyecto por
consola y creara la estructura EN LA MISMA CARPETA donde esta alojado el
script/ejecutable (no en la carpeta desde donde se llame).

No requiere librerías externas (solo librería estándar de Python).
"""

import argparse
import os
import sys
from datetime import date

# ---------------------------------------------------------------------------
# Disciplinas por defecto (ajustables desde la línea de comandos con --disciplinas)
# ---------------------------------------------------------------------------
DISCIPLINAS_DEFAULT = [
    "01_ARQUITECTURA",
    "02_ESTRUCTURAS",
    "03_HIDROSANITARIAS",
    "04_ELECTRICAS",
]

# Subcarpetas típicas de trabajo en Revit dentro de cada disciplina en WIP
SUBCARPETAS_REVIT = [
    "00_Modelo_Central",
    "01_Vinculados",       # otros modelos/CAD vinculados a este archivo
    "02_Familias",
    "03_Plantillas",
    "04_Vistas_Laminas",
    "05_Exportaciones",    # IFC, DWG, PDF de trabajo
]

# Contenido de READMEs por estado (para que el equipo sepa la regla del área)
README_TEXTS = {
    "1.0_WIP": (
        "ESTADO: WIP (Work In Progress / Trabajo en curso)\n"
        "----------------------------------------------------\n"
        "- Acceso: SOLO el equipo interno autor de cada disciplina.\n"
        "- Aqui se modela, se prueban opciones y se avanza el trabajo diario.\n"
        "- NUNCA se comparte esta carpeta directamente con clientes,\n"
        "  consultores externos o terceros.\n"
        "- Antes de pasar algo a 2.0_COMPARTIDO debe pasar un chequeo\n"
        "  interno (Check) por el responsable de la disciplina.\n"
        "- Aqui viven los modelos Revit centrales, vinculos, familias y\n"
        "  plantillas de trabajo (ver subcarpetas dentro de cada disciplina).\n"
    ),
    "2.0_COMPARTIDO": (
        "ESTADO: SHARED (Compartido)\n"
        "----------------------------------------------------\n"
        "- Acceso: equipo de proyecto y consultores/disciplinas coordinadas.\n"
        "- Aqui llega informacion ya revisada internamente, lista para\n"
        "  coordinacion entre disciplinas (deteccion de interferencias,\n"
        "  revision cruzada, comentarios).\n"
        "- NO es la entrega oficial al cliente. Es material 'en transito'.\n"
        "- Los archivos deben llevar codigo de revision (ej. P01, P02...).\n"
    ),
    "3.0_PUBLICADO": (
        "ESTADO: PUBLISHED (Publicado)\n"
        "----------------------------------------------------\n"
        "- Acceso de escritura: SOLO roles autorizados (Gestor de\n"
        "  Informacion / BIM Manager).\n"
        "- Contiene informacion que ya paso el proceso CRA\n"
        "  (Check, Review, Approve) y fue autorizada formalmente.\n"
        "- Es lo que se entrega oficialmente al cliente/comitente.\n"
        "- No se edita aqui directamente: toda modificacion nace en WIP.\n"
    ),
    "4.0_ARCHIVADO": (
        "ESTADO: ARCHIVED (Archivado)\n"
        "----------------------------------------------------\n"
        "- Acceso: solo lectura.\n"
        "- Guarda versiones superadas y entregas cerradas por hito.\n"
        "- Sirve como historico/trazabilidad del proyecto (audit trail).\n"
    ),
}


def crear_carpeta(ruta):
    """Crea una carpeta si no existe y devuelve True si se creo, False si ya existia."""
    if os.path.exists(ruta):
        return False
    os.makedirs(ruta)
    return True


def crear_readme(ruta_estado, nombre_estado):
    """Crea un README.md dentro de la carpeta de cada estado del CDE."""
    ruta_readme = os.path.join(ruta_estado, "README.txt")
    if not os.path.exists(ruta_readme):
        with open(ruta_readme, "w", encoding="utf-8") as f:
            f.write(README_TEXTS.get(nombre_estado, ""))


def construir_cde(nombre_proyecto, ruta_base, disciplinas):
    """
    Construye el arbol completo del CDE dentro de ruta_base/nombre_proyecto,
    siguiendo la logica de estados de la ISO 19650.
    """
    raiz_proyecto = os.path.join(ruta_base, nombre_proyecto)
    creadas = []

    def registrar(ruta):
        if crear_carpeta(ruta):
            creadas.append(ruta)

    registrar(raiz_proyecto)

    # --- 0.0 Documentacion de proyecto (BEP, EIR, contratos) ---
    doc_proyecto = os.path.join(raiz_proyecto, "0.0_DOCUMENTACION_PROYECTO")
    registrar(doc_proyecto)
    for sub in ["EIR", "BEP", "Contratos", "Actas_Reunion"]:
        registrar(os.path.join(doc_proyecto, sub))

    # --- 1.0 WIP ---
    wip = os.path.join(raiz_proyecto, "1.0_WIP")
    registrar(wip)
    crear_readme(wip, "1.0_WIP")

    for disciplina in disciplinas:
        carpeta_disc = os.path.join(wip, disciplina)
        registrar(carpeta_disc)

        # Carpeta Revit con sus subcarpetas tipicas
        carpeta_revit = os.path.join(carpeta_disc, "Revit")
        registrar(carpeta_revit)
        for sub in SUBCARPETAS_REVIT:
            registrar(os.path.join(carpeta_revit, sub))

        # Carpeta para CAD / documentos base de la disciplina
        registrar(os.path.join(carpeta_disc, "CAD"))
        registrar(os.path.join(carpeta_disc, "Documentos_Soporte"))

    # Coordinacion BIM (modelo federado, clashes, IFC)
    coordinacion = os.path.join(wip, "05_COORDINACION_BIM")
    registrar(coordinacion)
    for sub in ["Modelo_Federado", "Navisworks_Clashes", "IFC_Coordinacion"]:
        registrar(os.path.join(coordinacion, sub))

    # --- 2.0 COMPARTIDO ---
    compartido = os.path.join(raiz_proyecto, "2.0_COMPARTIDO")
    registrar(compartido)
    crear_readme(compartido, "2.0_COMPARTIDO")
    for disciplina in disciplinas:
        registrar(os.path.join(compartido, disciplina))
    registrar(os.path.join(compartido, "05_COORDINACION"))

    # --- 3.0 PUBLICADO ---
    publicado = os.path.join(raiz_proyecto, "3.0_PUBLICADO")
    registrar(publicado)
    crear_readme(publicado, "3.0_PUBLICADO")
    for sub in ["Planos_Entregados", "Modelos_IFC_Entregados", "Informes"]:
        registrar(os.path.join(publicado, sub))

    # --- 4.0 ARCHIVADO ---
    archivado = os.path.join(raiz_proyecto, "4.0_ARCHIVADO")
    registrar(archivado)
    crear_readme(archivado, "4.0_ARCHIVADO")
    registrar(os.path.join(archivado, "Versiones_Superadas"))
    registrar(os.path.join(archivado, "Entregas_Por_Hito"))

    return raiz_proyecto, creadas


def ruta_del_ejecutable():
    """
    Devuelve la carpeta donde esta alojado el script (o el .exe si se
    compilo con PyInstaller). Asi, al compilar/ejecutar, el CDE se crea
    junto al programa y no en la carpeta desde donde se lo invoque.
    """
    if getattr(sys, "frozen", False):
        # Ejecutable compilado (ej. PyInstaller)
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))


def main():
    parser = argparse.ArgumentParser(
        description="Crea la estructura de carpetas de un CDE segun ISO 19650 (WIP/Compartido/Publicado/Archivado)."
    )
    parser.add_argument(
        "proyecto", nargs="?", default=None,
        help="Nombre del proyecto (nombre de la carpeta raiz). Si se omite, se pide por consola."
    )
    parser.add_argument(
        "--ruta", default=None,
        help="Ruta base donde se creara la carpeta del proyecto (por defecto, la carpeta donde "
             "esta alojado este script/ejecutable)."
    )
    parser.add_argument(
        "--disciplinas", default=None,
        help="Lista de disciplinas separadas por coma, ej: 'Arquitectura,Estructuras,Electricas'. "
             "Si no se indica, se usan las disciplinas por defecto."
    )

    args = parser.parse_args()

    nombre_proyecto = args.proyecto
    if not nombre_proyecto:
        nombre_proyecto = input("Nombre del proyecto: ").strip()
        while not nombre_proyecto:
            nombre_proyecto = input("El nombre no puede estar vacio. Nombre del proyecto: ").strip()

    ruta_base = args.ruta if args.ruta else ruta_del_ejecutable()

    if args.disciplinas:
        # El usuario da nombres simples; se numeran automaticamente 01_, 02_, ...
        nombres = [d.strip() for d in args.disciplinas.split(",") if d.strip()]
        disciplinas = [f"{i:02d}_{n.upper().replace(' ', '_')}" for i, n in enumerate(nombres, start=1)]
    else:
        disciplinas = DISCIPLINAS_DEFAULT

    raiz, creadas = construir_cde(nombre_proyecto, ruta_base, disciplinas)

    print(f"CDE generado en: {raiz}")
    print(f"Fecha: {date.today().isoformat()}")
    print(f"Carpetas nuevas creadas: {len(creadas)}")
    if not creadas:
        print("(La estructura ya existia; no se creo nada nuevo.)")

    if getattr(sys, "frozen", False) or args.proyecto is None:
        # Si se ejecuto por doble clic (o sin argumentos), dejar la ventana
        # abierta para que se pueda leer el resultado.
        input("\nPresiona ENTER para salir...")


if __name__ == "__main__":
    sys.exit(main())