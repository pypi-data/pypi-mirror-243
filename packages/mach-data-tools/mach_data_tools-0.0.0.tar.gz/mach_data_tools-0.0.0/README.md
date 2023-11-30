## <img src="./images/mach_logo.png" width="40" height="40" /> MACH-Data-Tools: Herramientas para el Equipo de D&A de MACH

MACH-Data-Tools es una librería enfocada en la democratización del conocimiento y herramientas para el modelamiento y procesamiento de datos. Dentro de los recursos que ofrece la librería se encuentra análisis de estabilidad de las variables, selección de variables, métricas de evaluación y generación de intervalos en base a árboles de decisión.

## Instalación

MACH-Data-Tools puede ser instalado utilizando [Pypi](https://pypi.org/project/mach-data-tools/) mediante el siguiente comando:

**Shell:**
En una consola con **pip** instalado usar

```shell
pip install mach_data_tools
```

## ¿ Como puedo actualizar la librería en Pypi?

Para actualizar la versión de la librería usted deberá actualizar la versión de la librería en el archivo `setup.py` y luego ejecutar el siguiente script en la raíz del archivo utilizando el terminal:

```shell
python setup.py sdist
twine upload dist/*
```