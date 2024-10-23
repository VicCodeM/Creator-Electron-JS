import os
import subprocess
from colorama import init, Fore, Style

# Inicializar Colorama para la salida con colores en la consola
init(autoreset=True)

class LanzadorElectronSimple:
    """Clase para ejecutar 'npm start' en la carpeta actual."""

    def __init__(self):
        """Inicializa la clase con la ruta actual del directorio."""
        self.ruta_actual = os.getcwd()
        self.npm_path = self.obtener_ruta_npm()

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

    def lanzar_proyecto(self):
        """Lanza el proyecto de Electron usando 'npm start' en la carpeta actual."""
        print(Fore.GREEN + f"Iniciando el proyecto en: {self.ruta_actual}" + Style.RESET_ALL)
        try:
            process = subprocess.Popen(
                [self.npm_path, 'start'],
                cwd=self.ruta_actual,
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
                print(Fore.RED + f"Error al ejecutar npm start: código de salida {returncode}" + Style.RESET_ALL)
                return False

            return True
        except Exception as e:
            print(Fore.RED + f"Error: {e}" + Style.RESET_ALL)
            return False

if __name__ == "__main__":
    # Inicializar el lanzador
    lanzador = LanzadorElectronSimple()

    # Ejecutar el proyecto
    lanzador.lanzar_proyecto()

    input(Fore.CYAN + "Presione 'Enter' para salir..." + Style.RESET_ALL)
