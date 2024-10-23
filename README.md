# Asistente para Crear Proyectos de Electron

Este proyecto es un asistente de línea de comandos para crear fácilmente proyectos de Electron. Permite a los usuarios especificar el nombre del proyecto, la base de datos a utilizar (si la hay), y genera los archivos necesarios para iniciar el desarrollo de aplicaciones de escritorio con Electron.

## Características

- Crea un proyecto de Electron con un solo comando.
- Soporta múltiples tipos de bases de datos: SQLite, MySQL, y SQL Server.
- Genera archivos esenciales como `package.json`, `main.js`, `index.html`, y `styles.css`.
- Maneja la instalación automática de dependencias a través de npm.
- Interfaz de usuario en la consola con mensajes coloridos y advertencias.

## Requisitos

- [Python 3.6 o superior](https://www.python.org/downloads/)
- [Node.js y npm](https://nodejs.org/en/download/) (npm debe estar en la variable de entorno PATH)
- Dependencias de Python:
  - `colorama`

Puedes instalar las dependencias de Python necesarias ejecutando:

```bash
pip install colorama
