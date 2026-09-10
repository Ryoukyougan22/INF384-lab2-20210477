# Diagnóstico

## 1.1 Los cuatro defectos

### Defecto 1 — El job de publicación no depende de la validación

Archivo: `.github/workflows/pipeline.yml`  
Líneas: 42-68.

El job `publicar` no tiene `needs: validar`. Esto significa que GitHub puede ejecutar `validar` y `publicar` de forma independiente, incluso en paralelo. Por lo que esto causa que se puede construir y publicar el artefacto aunque las pruebas o el análisis de calidad fallen. 

### Defecto 2 — Se publica ante cualquier push

Archivo: `.github/workflows/pipeline.yml`  
Líneas: 3-6 y 42-43.

El trigger `push` no tiene filtro de rama y el job `publicar` se ejecuta para cualquier evento `push`. Por lo que se pierde la garantía de que únicamente el código de una rama autorizada, como `main`, sea publicado.

### Defecto 3 — El pipeline no espera el resultado del Quality Gate

Archivo: `.github/workflows/pipeline.yml`  
Líneas: 32-40.

El workflow ejecuta el análisis de SonarQube Cloud, pero no se observa una configuración que obligue al pipeline a esperar y verificar el resultado del Quality Gate. En consecuencia, el análisis puede enviarse correctamente a SonarQube Cloud y el job terminar exitosamente aunque posteriormente el Quality Gate determine que el código no cumple las condiciones de calidad.

### Defecto 4 — Se repite la preparación e instalación de dependencias

Archivo: `.github/workflows/pipeline.yml`  
Líneas: 19-27 y 50-58.

Los jobs `validar` y `publicar` configuran Python e instalan nuevamente las dependencias. Esto resulta en que se aumenta innecesariamente la duración del workflow y el tiempo que el desarrollador debe esperar para recibir el resultado.

## 1.2 El defecto que explica la duración

El defecto que principalmente explica la duración observada es el Defecto 4: la preparación e instalación repetida de dependencias.
Los jobs `validar` y `publicar` utilizan runners independientes y ambos vuelven a configurar Python e instalar las dependencias. Esto genera trabajo repetido y aumenta el tiempo total del pipeline.

## 1.3 Vínculo con el caso transversal

El defecto que más ataca la restricción de nuestro caso transversal, Seguros Pacífico Sur, es el Defecto 3: el pipeline no espera ni hace cumplir el resultado del Quality Gate.

En el Value Stream Map del caso se observa un alto nivel de retrabajo: 45 de cada 100 elementos que llegan a pruebas funcionales regresan a desarrollo con defectos, y 76 de 94 historias fueron devueltas al menos una vez a una etapa anterior.

Por ello, hacer que el Quality Gate bloquee el pipeline cuando no se cumplen las condiciones de calidad ayuda a detectar problemas antes y evita que código con problemas siga avanzando, reduciendo parte del retrabajo que alarga el flujo.


## 1.4 Métrica DORA

La métrica DORA que esperamos mejorar es Lead Time for Changes, porque la intervención busca reducir el tiempo necesario para obtener feedback sobre un cambio.

Sin un despliegue real, las dos métricas que pueden aproximarse mediante el pipeline son Lead Time for Changes y Change Failure Rate.

Elegimos Lead Time for Changes porque podemos utilizar la duración del workflow como proxy del tiempo de feedback de un cambio.

## 1.5 Proxy

Se utiliza el proxy como la mediana de la duración total de tres ejecuciones consecutivas del workflow.

Línea base:
- Ejecución 1: 72 segundos (1m 12 s)
- Ejecución 2: 59 segundos.
- Ejecución 3: 55 segundos.

Mediana de línea base: 59 segundos.

Después de la intervención se ejecutará nuevamente el workflow tres veces y se comparará la nueva mediana contra los 59 segundos iniciales.
