import subprocess
import shlex
from typing import List, Union


def ejecutar_comando(comando: Union[str, List[str]]) -> str:
    """
    Ejecuta un comando de forma segura utilizando subprocess.
    Se asegura de no usar shell=True y valida los argumentos adecuadamente.
    """
    if isinstance(comando, str):
        args = shlex.split(comando)
    else:
        args = [str(arg) for arg in comando]

    if not args:
        raise ValueError("El comando a ejecutar está vacío.")

    try:
        resultado = subprocess.run(
            args, shell=False, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        return resultado.stdout
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"El comando falló con código {e.returncode}: {e.stderr}") from e
