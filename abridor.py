import webbrowser
import time

# Nombre del archivo que contiene los enlaces
file_path = 'paginas_validas.txt'

# Leer los enlaces del archivo
with open(file_path, 'r') as file:
    # Leer cada línea del archivo y eliminar espacios en blanco
    links = [line.strip() for line in file.readlines()]

# Abrir cada enlace en el navegador con 5 segundos de espera entre cada uno
for link in links:
    if link:  # Verifica si la línea no está vacía
        webbrowser.open(link)
        time.sleep(5)  # Espera de 5 segundos entre enlaces
