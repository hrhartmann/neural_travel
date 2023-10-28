# neural_travel: Documentación

Hans Hartmann

## Introducción

Este repositorio tiene por objetivo responder a las preguntas del desafío de NeuralWorks.

## Instrucciones para levantar API

Es necesario abrir la aplicación con docker-compose.

Windows:

Es necesario tener un archivo .env con la clave de la base de datos. Este archivo solo requiere el la constante: DB_PASSWORD

```PS or CMD
docker-compose up --build
```




## Respuestas 

Notar que todos los parámetros son modificables y se encuentran en el archivo params. Una mejora sería hacer endpoint que puedan recibir parámetros.

### 1.a

La respuesta a esta pregunta se encuentra en el endpoint /group.

Lo primero, el enfoque que se utilizó fue separar primero los viajes po región, que es lo más rápido y directo para posteriormente separar por zona. Las zonas son simplemente cuadrantes en un plano. Para poder determinar la cantidad de zonas es necesario ir al archivo params.py y modificar la variable GRID_BY_REGION=x donde x^2 es la cantidad de zonas.

Por último, los grupos se forman por cercanía de fechas, para esto, simplemente se ordenan por fecha y se separan por cantidad por grupo. la variable PER_GROUP.

### 2.a

La respuesta a esta pregunta se encuentra en el endpoint: /weekly_avg

El bounding box se define con dos puntos. Estos puntos se pueden establecer como parámetros.

### 2.b

Se pueden utilizar logs pero no está implementado.

### 3

Para que la solución sea escalable se utiliza una API que permite recibir y entregar resultados bajo demanda. Para escalar horizontalmente se pueden levantar diferentes instancias de la API. Para escalar verticalmente se puede realizar diferentes mejoras de eficiencia, balance de carga y otros, se dejan como mejora.

### 4 

La solución está escrita en Flask (Python) con base de datos MySQL.

### 5

La solución se encuentra en un contenedor Docker.
El dibujo solicitado se encuentra en la carpeta diagram.


## Supuestos

1. Se asume que todos los puntos tienen coordenadas positivas, sin embargo, es fácil adaptar el código para otros casos.

## Aclaraciones

Si bien existe una base de datos, y funciona, dado errores técnicos y falta de tiempo se decide usar directamente el archivo csv, pero preparado para que pueda guardar directo a base de datos y leer esos datos.

Existen muchas mejoras posibles para este proyecto, se trata simplemente de una maqueta que tiene diferentes oportunidades de mejora, desde la paginación, la exposición de diferentes tipos nuevos de enpoints, personalización de parámetros, entre otros.

Muchas gracias por su tiempo.