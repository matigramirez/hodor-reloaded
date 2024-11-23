# Hodor ft. Vehiculos Inteligentes 23

## Introducción

Este repositorio contiene la documentación y el código fuente del proyecto final propuesto para la materia Introducción
a los Vehículos Inteligentes en el cual se hace uso del robot Hodor.

## Autores:

- Marin Roth, Darío Alejandro
- Ramirez Pelegrina, Matías Gonzalo
- Valenti Cristallini, Giuliana

## Dependencias

### Debian

Debe instalarse el paquete `python3-opencv` mediante `apt`:

- `sudo apt install python3-opencv`

### Python

Deben instalarse los siguientes paquetes mediante `pip`:

- pyserial
- python-opencv
- pyapriltags
- numpy

Ejemplo: `pip install nombre_del_paquete`

## Hipótesis Simplificativas

- El robot siempre tendrá visión directa de la base para alguna dirección a partir de su posición inicial
- El robot puede no tener visión directa de la base en su posición inicial
- No se consideran obstáculos

## Procedimiento

### 1. Calibración de la cámara

Debe realizarse la calibración de la cámara para poder obtener sus parámetros intrínsecos, lo cual
permite formar una matriz de transformación que mapee puntos de la imagen `(px, py)` en puntos del espacio
tridimensional `(x, y, z)`. Los pasos a seguir están indicados en el documento [`camara.md`](docs/camara.md).

### 2. Indicación de la base

Debe indicarse la ubicación de la base mediante la utilización de april tags. Los pasos para su generación y disposición
se encuentran en el documento [`apriltags.md`](docs/apriltags.md).

### 3. Rutina de movimiento

La rutina de movimiento propuesta tiene como objetivo lograr que el robot Hodor pueda detectar y dirigirse hacia la base
indicada mediante los april tags.  
El procedimiento consiste en 3 acciones principales:

- Detección de la base
- Alineación con la base
- Movimiento hacia la base

#### Diagrama de flujo - Rutina de movimiento

[![Diagrama de flujo](docs/assets/alcanzar-objetivo_diagrama-de-flujo.svg) ""](docs/assets/alcanzar-objetivo_diagrama-de-flujo.svg)