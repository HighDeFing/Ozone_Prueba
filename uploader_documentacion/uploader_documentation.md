### Resumen de ejecución:
Es un uploader (cargador) de archivos, los tipos de archivos que uno puede utilizar tienen que ser archivos zip, con una carpeta adentro que tenga archivos de tres tipos:

- gltf: Si son gltf este contiene un archivo `.png` o `.jpg`, un archivo gltf y un binario.
- fbx: Este es un archivo que solo tiene un `.fbx`.
- obj: Es un zip como todos, que tiene una carpeta adentro, que contiene `.obj`, `.mlt` y una carpeta texturas con imágenes.

Todos estos archivos son convertidos a `.glb`.

Estos archivos son guardados en upload_files es su formato original (gltf, fbx, obj) y luego de ser convertidos a `.glb` se guardan en converted_files, estas carpetas son creadas cuando se ejecuta el programa por primera vez. 

En converted_files se guardan los .glb con una id de usuario y luego se guarda con una id de objeto 3d, estos se encuentran estáticos por motivos de la prueba, pero pueden ser cambiados.

Para subir los archivos solo tenemos que especificar el tipo de archivo que estamos subiendo (gltf, fbx, obj), y luego de esto arrastrar o seleccionar el archivo.

Si le damos click download en el template de galería (que es a donde nos navega el programa luego de subir un archivo), nos encontramos con la dirección del archivo dentro del servidor.

Especificaciones técnicas:
- El programa se ejecuta con yarn.
- Se utiliza **Flask**, **HTML** y **node.js**.
- Flask sirve como servidor.
- HTML es para la interfaz de subir archivos, en static se encuentra una plantilla generica con archivos CSS para darle estilo.
- node.js se utiliza porque todos los script convertidores de archivos son programas de node.
- El lenguaje de programación utilizado como base es Python.