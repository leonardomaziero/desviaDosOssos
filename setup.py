import sys
from cx_Freeze import setup, Executable
from chunk import Chunk
import aifc 


# Adiciona arquivos e pastas necessárias para o jogo
include_files = [
    ("Recursos", "Recursos")  # copia a pasta Recursos inteira
]

# Opções para empacotamento
build_exe_options = {
    "packages": [
        "pygame",
        "os",
        "random",
        "datetime",
        "speech_recognition",
        "pyttsx3",
        "time",
        "aifc"
    ],
    "includes": ["aifc", "chunk", "audioop"],
    "include_files": [("Recursos", "Recursos")]
}
# Remove o terminal ao rodar o jogo
base = "Win32GUI" if sys.platform == "win32" else None

# Cria o executável
setup(
    name="Dodge The Bones!",
    version="1.0",
    description="Jogo Dodge The Bones",
    options={"build_exe": build_exe_options},
    executables=[Executable("main.py", base=base, target_name="DodgeTheBones.exe")]
)
