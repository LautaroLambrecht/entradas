import requests
import time
import fitz  # PyMuPDF
import pyzbar.pyzbar as pyzbar
from PIL import Image
import io
import re

def check_page(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Lanza un error si la respuesta no es 200
        return response.content  # Devolver el contenido del PDF
    except requests.HTTPError as e:
        if e.response.status_code == 404:
            return None
    except Exception:
        return None

def decode_qr_from_image(image):
    try:
        decoded_objects = pyzbar.decode(image)
        qr_codes = []
        for obj in decoded_objects:
            if obj.type == "QRCODE":
                qr_codes.append(obj.data.decode("utf-8"))
        return qr_codes
    except Exception as e:
        return []

def extract_images_from_pdf(pdf_content):
    images = []
    pdf_document = fitz.open(stream=pdf_content, filetype="pdf")
    for page_num in range(len(pdf_document)):
        page = pdf_document[page_num]
        image_list = page.get_images(full=True)
        for img_index, img in enumerate(image_list):
            xref = img[0]
            base_image = pdf_document.extract_image(xref)
            image_bytes = base_image["image"]
            images.append(Image.open(io.BytesIO(image_bytes)))
    return images

def get_name_from_qr(qr_data):
    match = re.search(r"NOMBRE: '([^']+)'", qr_data)
    return match.group(1) if match else ""

def generate_and_check_urls(base_url, start, end):
    with open("paginas_validas.txt", "a") as output_file:
        for i in range(start, end + 1):
            url = f"{base_url}{i}.pdf"
            print(f"Verificando PDF número: {i}")  # Muestra por consola el número de PDF actual
            pdf_content = check_page(url)

            if pdf_content:
                # Extraer imágenes del PDF
                images = extract_images_from_pdf(pdf_content)

                # Verificar los códigos QR en las imágenes extraídas
                for image in images:
                    qr_codes = decode_qr_from_image(image)
                    for qr in qr_codes:
                        # Verificar si el QR contiene alguno de los productos
                        if any(product in qr for product in ["PRODUCTO: 870", "PRODUCTO: 857", "PRODUCTO: 865", "PRODUCTO: 8858", "PRODUCTO: 869"]):
                            name = get_name_from_qr(qr)  # Obtener el nombre del QR
                            if len(name) <= 3:  # Verificar si el nombre tiene 3 o menos caracteres
                                time.sleep(5)  # Esperar 5 segundos después de encontrar el QR
                                output_file.write(f"{url} - NOMBRE tiene {len(name)} caracteres: {name}\n")
                            break  # Salir del bucle al encontrar un producto válido

base_url = "https://admin.grupomemorable.com/back/public/entradas_"
start_number = 44760
end_number = 70000

generate_and_check_urls(base_url, start_number, end_number)
