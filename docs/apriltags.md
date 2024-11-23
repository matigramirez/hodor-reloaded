# April Tags

En la base que debe ser alcanzada por el robot se colocarán 2 april tags, uno de mayor tamaño (120x120 mm), para ser
detectado desde distancias largas (2 a 8 metros) y uno de menor tamaño (60x60 mm) para ser detectado en distancias
cortas (0 a 2 metros).

Se elige utilizar la familia de april tags `tag36h11`, ya que esta tiene una resolución suficientemente alta como para
evitar la detección errónea de los tags cuando la imagen tiene un nivel alto de ruido. Además, cada april
tag debe tener un identificador único: `0` para el de menor tamaño y `1` para el de mayor tamaño.

## Objetivo

Se desea localizar la posición relativa de los april tag tomando como origen de coordenadas la posición de la cámara del
robot.

## Procedimiento

- Imprimir april tags: [tag36h11_id0_60mm.pdf](assets/april_tags/tag36h11_id0_60mm.pdf)
  y [tag36h11_id1_120mm](assets/april_tags/tag36h11_id1_120mm.pdf) en tamaño real (sin escalar)
- Colocar april tags alineados en el eje horizontal en la sala de pruebas con su centro a la misma altura que la cámara
