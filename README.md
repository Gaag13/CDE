# CDE Creator

Este proyecto crea automáticamente la estructura de carpetas de un Common Data Environment (CDE) para proyectos BIM siguiendo la lógica ISO 19650:

- 1.0_WIP: trabajo en curso
- 2.0_COMPARTIDO: información revisada para coordinación
- 3.0_PUBLICADO: entregas aprobadas
- 4.0_ARCHIVADO: histórico y versiones cerradas

## ¿Qué hace?

Genera una carpeta principal con:

- documentación del proyecto
- disciplinas por defecto (arquitectura, estructuras, hidráulicas, eléctricas)
- subcarpetas para Revit, CAD y documentos de apoyo
- README por cada estado para dejar claro el uso de cada zona

## Cómo ejecutarlo

Desde la terminal:

```bash
python CDE.py "Nombre del Proyecto"
```

También puedes indicar una ruta base y disciplinas:

```bash
python CDE.py "Nombre del Proyecto" --ruta "D:/Proyectos" --disciplinas "Arquitectura,Estructuras,Electricas"
```

Si se ejecuta sin argumentos, te pedirá el nombre del proyecto y creará la estructura en la misma carpeta del script.

## Resultado

Se crea una estructura como esta:

```text
Nombre_del_Proyecto/
├── 0.0_DOCUMENTACION_PROYECTO/
├── 1.0_WIP/
├── 2.0_COMPARTIDO/
├── 3.0_PUBLICADO/
├── 4.0_ARCHIVADO/
```

Es una herramienta útil para organizar proyectos BIM y mantener el flujo de trabajo ordenado.
