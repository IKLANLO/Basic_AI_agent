import subprocess

# Ejecutar ollama serve y guardar la salida en un archivo
with open("ollama_output.txt", "w") as f:
    # El proceso se ejecuta en primer plano y escribe la salida en el archivo
    process = subprocess.Popen(["ollama", "serve"], stdout=f, stderr=subprocess.STDOUT)