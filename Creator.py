import os
import json
import subprocess
import sys
from colorama import init, Fore, Style

# Inicializar Colorama para la salida con colores en la consola
init(autoreset=True)

class CrearProyecto:
    """Clase para manejar la creación de proyectos de Electron."""

    def __init__(self):
        """Inicializa la clase obteniendo el nombre del proyecto, la ruta de npm y las bases de datos seleccionadas."""
        self.nombre_proyecto = self.obtener_nombre_proyecto()
        self.npm_path = self.obtener_ruta_npm()
        self.tipos_db_seleccionados = self.obtener_seleccion_bases_datos()

    def obtener_nombre_proyecto(self):
        """Solicita al usuario el nombre del proyecto y verifica si ya existe."""
        while True:
            nombre_proyecto = input(Fore.CYAN + "Ingrese el nombre del proyecto: " + Style.RESET_ALL).strip()
            if not nombre_proyecto:
                print(Fore.RED + "El nombre del proyecto no puede estar vacío." + Style.RESET_ALL)
                continue
            if self.verificar_proyecto_existente(nombre_proyecto):
                print(Fore.RED + f"Un proyecto llamado '{nombre_proyecto}' ya existe." + Style.RESET_ALL)
                continue
            return nombre_proyecto

    def verificar_proyecto_existente(self, nombre_proyecto):
        """Verifica si un proyecto con el nombre dado ya existe."""
        proyecto_dir = os.path.join(os.getcwd(), nombre_proyecto)
        return os.path.exists(proyecto_dir)

    def obtener_ruta_npm(self):
        """Obtiene la ruta de npm desde las variables de entorno. 
        Si no está definida, busca en la ruta del sistema y 
        finalmente usa 'npm' como valor por defecto."""

        npm_path = os.environ.get('NPM_PATH')  # Buscar en variables de usuario y del sistema

        if npm_path is None:
            # Si no se encuentra en la variable de entorno, buscar en la ruta del sistema
            for path in os.environ["PATH"].split(os.pathsep):
                posible_ruta_npm = os.path.join(path, "npm.cmd")
                if os.path.exists(posible_ruta_npm):
                    npm_path = posible_ruta_npm
                    break

        if npm_path is None:
            print(Fore.YELLOW + "ADVERTENCIA: No se encontró 'npm' en las variables de entorno ni en la ruta del sistema. Se usará 'npm' como comando, asegúrese de que esté instalado y accesible globalmente." + Style.RESET_ALL)
            npm_path = "npm"

        return npm_path

    def obtener_seleccion_bases_datos(self):
        """Solicita al usuario que seleccione las bases de datos a incluir."""
        print(Fore.CYAN + "\nSeleccione las bases de datos para incluir en el proyecto:" + Style.RESET_ALL)
        print(Fore.YELLOW + "1 - SQLite" + Style.RESET_ALL)
        print(Fore.YELLOW + "2 - MySQL" + Style.RESET_ALL)
        print(Fore.YELLOW + "3 - SQL Server" + Style.RESET_ALL)
        print(Fore.YELLOW + "4 - Ninguna base de datos (crear un proyecto simple)" + Style.RESET_ALL)

        tipos_db_seleccionados = []
        while True:
            opcion = input(Fore.CYAN + "Ingrese el número de su elección (1-4): " + Style.RESET_ALL)

            if opcion == "1":
                tipos_db_seleccionados.append("sqlite")
                print(Fore.GREEN + "Incluido SQLite." + Style.RESET_ALL)
                break
            elif opcion == "2":
                tipos_db_seleccionados.append("mysql")
                print(Fore.GREEN + "Incluido MySQL." + Style.RESET_ALL)
                break
            elif opcion == "3":
                tipos_db_seleccionados.append("mssql")
                print(Fore.GREEN + "Incluido SQL Server." + Style.RESET_ALL)
                break
            elif opcion == "4":
                print(Fore.GREEN + "No se incluirá ninguna base de datos, creando un proyecto simple." + Style.RESET_ALL)
                break
            else:
                print(Fore.RED + "Opción inválida. Por favor, intente nuevamente." + Style.RESET_ALL)

        return tipos_db_seleccionados

    def crear_directorio_proyecto(self):
        """Crea el directorio principal del proyecto."""
        proyecto_dir = os.path.join(os.getcwd(), self.nombre_proyecto)
        os.makedirs(proyecto_dir, exist_ok=True)
        return proyecto_dir

    def generar_package_json(self, proyecto_dir):
        """Genera el archivo package.json con las dependencias."""
        package_json = {
            "name": self.nombre_proyecto,
            "version": "1.0.0",
            "description": "Proyecto de Electron {self.nombre_proyecto}",  # Agregar descripción
            "author": "Victor Maldonado",  # Agregar autor
            "main": "main.js",
            "scripts": {
                "start": "electron .",
                "build": "electron-builder --win",
                "dev": "electron .",
                "test": "jest"  
            },
            "devDependencies": {
                "electron": "*",  # Cambia aquí para usar una versión específica
                "electron-builder": "*",  # Cambia aquí para usar una versión específica
                "electron-devtools-installer": "*",
                "jest": "^27.0.0" 

            },
            "jest": {
                "testEnvironment": "node"
            },
            "dependencies": {}
        }

        if "sqlite" in self.tipos_db_seleccionados:
            package_json["dependencies"]["sqlite3"] = "latest"
        if "mysql" in self.tipos_db_seleccionados:
            package_json["dependencies"]["mysql"] = "latest"
        if "mssql" in self.tipos_db_seleccionados:
            package_json["dependencies"]["mssql"] = "latest"

        with open(os.path.join(proyecto_dir, 'package.json'), 'w', encoding='utf-8') as f:
            json.dump(package_json, f, ensure_ascii=False, indent=4)



    def generar_main_js(self, proyecto_dir):
        """Genera el archivo main.js del proyecto Electron."""
        with open(os.path.join(proyecto_dir, 'main.js'), 'w') as f:
            f.write('''const { app, BrowserWindow } = require('electron');
const path = require('path');

function createWindow() {
  const win = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false,
      preload: path.join(__dirname, 'preload.js') // Preload script for security
    }
  });

  win.loadFile('index.html');
}

// App lifecycle events
app.whenReady().then(() => {
  createWindow();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});
''')

    def generar_index_html(self, proyecto_dir):
        """Genera el archivo index.html del proyecto."""
        with open(os.path.join(proyecto_dir, 'index.html'), 'w',encoding='utf-8') as f:
            f.write('''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{}</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <header>
        <h1>Bienvenido a {}</h1>
    </header>
    <main>
        <p>Este es un proyecto básico creado con el asistente de creación de proyectos.</p>
    </main>
    <footer>
        <p>&copy; 2024 Su Nombre. Todos los derechos reservados.</p>
    </footer>
</body>
</html>
'''.format(self.nombre_proyecto, self.nombre_proyecto))

    def generar_styles_css(self, proyecto_dir):
        """Genera un archivo styles.css básico para el estilo del proyecto."""
        with open(os.path.join(proyecto_dir, 'styles.css'), 'w') as f:
            f.write('''body {
    font-family: Arial, sans-serif;
    margin: 0;
    padding: 0;
    background-color: #f4f4f4;
    color: #333;
}

header {
    background: #35424a;
    color: #ffffff;
    padding: 10px 0;
    text-align: center;
}

main {
    padding: 20px;
}

footer {
    text-align: center;
    padding: 10px 0;
    background: #35424a;
    color: #ffffff;
    position: absolute;
    bottom: 0;
    width: 100%;
}
''')

    def instalar_dependencias(self, proyecto_dir):
        """Instala las dependencias del proyecto usando npm."""
        print(Fore.YELLOW + "Instalando dependencias..." + Style.RESET_ALL)

        try:
            process = subprocess.Popen(
                [self.npm_path, 'install'],
                cwd=proyecto_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            for line in iter(process.stdout.readline, ''):
                print(line.strip())

            stderr_output = process.stderr.read()
            if stderr_output:
                print(Fore.BLUE + stderr_output.strip() + Style.RESET_ALL)

            returncode = process.wait()
            if returncode != 0:
                print(Fore.RED + f"Error al instalar dependencias: código de salida {returncode}" + Style.RESET_ALL)
                return False

            return True
        except Exception as e:
            print(Fore.RED + f"Error: {e}" + Style.RESET_ALL)
            return False

    def crear_proyecto(self):
        """Crea el proyecto de Electron."""
        print(Fore.GREEN + f"Creando el proyecto de Electron: '{self.nombre_proyecto}'..." + Style.RESET_ALL)
        proyecto_dir = self.crear_directorio_proyecto()
        self.generar_package_json(proyecto_dir)
        self.generar_main_js(proyecto_dir)
        self.generar_index_html(proyecto_dir)
        self.generar_styles_css(proyecto_dir)

        if self.instalar_dependencias(proyecto_dir):
            print(Fore.GREEN + f"Proyecto '{self.nombre_proyecto}' creado con éxito." + Style.RESET_ALL)
            print(Fore.GREEN + "Ejecute 'npm start' para iniciar su aplicación Electron." + Style.RESET_ALL)
        else:
            print(Fore.RED + "Hubo un problema al crear el proyecto." + Style.RESET_ALL)

if __name__ == "__main__":
    proyecto = CrearProyecto()
    proyecto.crear_proyecto()
    input(Fore.CYAN + "Presione 'Enter' para salir..." + Style.RESET_ALL)  # Permitir salir presionando Enter
