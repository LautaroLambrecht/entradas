import urllib.request

def check_page(url):
    try:
        response = urllib.request.urlopen(url)
        return True
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return False
    except Exception as e:
        print(f"Error al intentar acceder a la página {url}: {e}")
        return False

def generate_and_check_urls(base_url, start, end):
    # Abre el archivo en modo de adición (append), para no sobreescribir datos anteriores
    with open("paginas_validas.txt", "a") as file:
        for i in range(start, end + 1):
            url = f"{base_url}{i}.pdf"
            if check_page(url):
                print(f"Página válida encontrada: {url}")
                file.write(f"{url}\n")  # Escribe la URL válida en el archivo

base_url = "https://admin.grupomemorable.com/back/public/entradas_" 
start_number = 40000  
end_number = 45000 

generate_and_check_urls(base_url, start_number, end_number)
