# Cámara

## Introducción

El robot cuenta con una cámara `Logitech C505` cuya mayor resolución es `1280 x 720` pixeles con una tasa de refresco de
`5 fps`.  
Para poder hacer uso adecuado de la misma, se debe realizar un proceso de calibración y así poder obtener los parámetros
intrínsecos.

## Calibración

La calibración consiste en 4 pasos:

- Generación de tablero de calibración ("tablero de ajedrez")  
[![Tablero de calibración](assets/calibration/calibration_pattern.png "https://github.com/opencv/opencv/blob/4.x/doc/pattern.png")](assets/calibration/calibration_pattern.png)
- Adquisición de dataset donde esté el tablero presente
- Ejecución de la calibración mediante `opencv`
- Persistir calibración en un archivo para su posterior utilización

## Adquisición del dataset

Las imágenes tomadas para la calibración deben incluir una vista clara del tablero y este debe ser posicionado
de tal forma que siempre visto de frente (su rotación en el eje de altura debe ser nula).

## Procedimiento

El procedimiento de calibración requiere de un entorno de escritorio para poder visualizar los pasos de la calibración
y validar su correcto funcionamiento.

- Imprimir [tablero de calibración](assets/calibration/calibration_pattern.pdf) en tamaño real (sin escalar)
- Ejecutar el script [`calibrate.py`](../src/calibrate.py)
- Seguir las instrucciones indicadas por la terminal

Si el proceso de calibración se realiza con éxito, la calibración resultante será guardada
en un archivo de texto llamado `calibration.json`.