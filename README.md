# Pasos para iniciación automática del agente IA en Windows:

## 1º - Iniciar 'Programador de tareas' y seleccionar 'Crear tarea básica', rellenar los siguientes datos:

<p align="center">
  <img src="image-1.png" alt="Pantallazo 1" width="45%"/>
  <img src="image-2.png" alt="Pantallazo 2" width="45%"/>
</p>
<p align="center">
  <img src="image-3.png" alt="Pantallazo 1" width="45%"/>
  <img src="image-4.png" alt="Pantallazo 2" width="45%"/>
</p>

### En 'Agregar argumentos' indicar (rellenando los datos de la ruta):

    /c start /min "" "D:\Ruta_completa_a_init.bat\init.bat"

## 2º Finalizar, seleccionar la tarea, ir a 'Propiedades' y marcar lo siguiente:

<p align="center">
  <img src="image-5.png" alt="Pantallazo 5" width="31%"/>
  <img src="image-7.png" alt="Pantallazo 7" width="31%"/>
  <img src="image-8.png" alt="Pantallazo 8" width="31%"/>
</p>

## 3º Aceptar y reiniciar el PC.

Se iniciará un terminal iniciando init.bat, y una pestaña del navegador predeterminado con el agente IA tras unos segundos de cargar el modelo.
