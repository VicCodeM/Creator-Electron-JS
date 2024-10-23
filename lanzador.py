import os
import subprocess
import sys
from colorama import init, Fore, Style

# Inicializar Colorama para la salida con colores en la consola
init(autoreset=True)

class LanzadorElectron:
    """Clase para manejar el lanzamiento de proyectos Electron usando npm."""

    def __init__(self):
        """Inicializa la clase con la ruta actual del directorio donde se encuentra el ejecutable."""
        self.ruta_base = self.obtener_ruta_actual()
        self.npm_path = self.obtener_ruta_npm()

    def obtener_ruta_actual(self):
        """Obtiene la ruta del directorio donde se encuentra el ejecutable (o script)."""
        if getattr(sys, 'frozen', False):
            # Si está compilado como un .exe con PyInstaller
            return os.path.dirname(sys.executable)
        else:
            # Si está corriendo como script
            return os.getcwd()

    def obtener_ruta_npm(self):
        """Obtiene la ruta de npm desde las variables de entorno."""
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

    def listar_carpetas(self):
        """Lista las carpetas en la ruta base."""
        carpetas = [nombre for nombre in os.listdir(self.ruta_base) if os.path.isdir(os.path.join(self.ruta_base, nombre))]
        return carpetas

    def seleccionar_carpeta(self):
        """Permite al usuario seleccionar una carpeta de entre las disponibles."""
        carpetas = self.listar_carpetas()
        if not carpetas:
            print(Fore.RED + "No se encontraron proyectos en este directorio." + Style.RESET_ALL)
            input(Fore.CYAN + "Presione 'Enter' para salir..." + Style.RESET_ALL)
            sys.exit(1)

        print(Fore.CYAN + "Proyectos disponibles:" + Style.RESET_ALL)
        for idx, carpeta in enumerate(carpetas, 1):
            print(f"{idx}. {carpeta}")

        seleccion = input(Fore.CYAN + "Seleccione el número del proyecto que desea lanzar: " + Style.RESET_ALL).strip()

        try:
            seleccion = int(seleccion)
            if 1 <= seleccion <= len(carpetas):
                return carpetas[seleccion - 1]
            else:
                print(Fore.RED + "Selección inválida." + Style.RESET_ALL)
                sys.exit(1)
        except ValueError:
            print(Fore.RED + "Entrada inválida. Debe ser un número." + Style.RESET_ALL)
            sys.exit(1)

    def listar_comandos(self):
        """Lista los comandos de npm disponibles."""
        comandos = [
            "start",
            "run dev",
            "run build"
        ]
        return comandos

    def seleccionar_comando(self):
        """Permite al usuario seleccionar un comando para ejecutar."""
        comandos = self.listar_comandos()
        print(Fore.CYAN + "Comandos disponibles:" + Style.RESET_ALL)
        for idx, comando in enumerate(comandos, 1):
            print(f"{idx}. {comando}")

        seleccion = input(Fore.CYAN + "Seleccione el número del comando que desea ejecutar: " + Style.RESET_ALL).strip()

        try:
            seleccion = int(seleccion)
            if 1 <= seleccion <= len(comandos):
                return comandos[seleccion - 1]
            else:
                print(Fore.RED + "Selección inválida." + Style.RESET_ALL)
                return None
        except ValueError:
            print(Fore.RED + "Entrada inválida. Debe ser un número." + Style.RESET_ALL)
            return None

    def lanzar_proyecto(self, proyecto, comando):
        """Lanza el proyecto de Electron usando el comando seleccionado."""
        ruta_proyecto = os.path.join(self.ruta_base, proyecto)
        print(Fore.GREEN + f"Iniciando el proyecto: {proyecto}" + Style.RESET_ALL)
        try:
            process = subprocess.Popen(
                [self.npm_path] + comando,
                cwd=ruta_proyecto,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            # Leer la salida en tiempo real
            for line in iter(process.stdout.readline, ''):
                print(line.strip())

            # Capturar errores si los hay
            stderr_output = process.stderr.read()
            if stderr_output:
                print(Fore.RED + stderr_output.strip() + Style.RESET_ALL)

            # Verificar si el proceso fue exitoso
            returncode = process.wait()
            if returncode != 0:
                print(Fore.RED + f"Error al ejecutar {comando}: código de salida {returncode}" + Style.RESET_ALL)
                return False

            return True
        except Exception as e:
            print(Fore.RED + f"Error: {e}" + Style.RESET_ALL)
            return False

if __name__ == "__main__":
    # Inicializar el lanzador
    lanzador = LanzadorElectron()

    # Listar las carpetas y seleccionar el proyecto
    proyecto_seleccionado = lanzador.seleccionar_carpeta()

    # Seleccionar el comando a ejecutar
    comando_seleccionado = lanzador.seleccionar_comando()

    # Lanzar el proyecto seleccionado con el comando elegido
    if comando_seleccionado:
        lanzador.lanzar_proyecto(proyecto_seleccionado, comando_seleccionado.split())

    input(Fore.CYAN + "Presione 'Enter' para salir..." + Style.RESET_ALL)

