from typing import Optional
from fastapi import FastAPI, File, UploadFile
from PIL import Image
import pytesseract
import os

# Inicializamos el objeto app que viene de la clase FastAPI y es lo que nos
# permitira generar todo a traves de su framework
app = FastAPI()

# Ejemplo extraido de la doc oficial para saber como funciona.
@app.get("/")
def read_root():
    return {"Hello": "World"}

# Ejemplo extraido de la doc oficial para saber como funciona pasando un parammetro
@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}

# Nuestro metodo. Primero de todo destacar que se trata de un metodo POST
# se accede mediante la ruta uploadfile pudiendo cambiarlo a la ruta que queramos
# Basicamente recibe una imagen, la almacena en la carpeta de imagenes y devuelve su texto
@app.post("/uploadfile/")
def create_upload_file(file: UploadFile):
    if os.environ.get('DOCKER', '') == "yes":
        with open(f"/usr/src/app/images/{file.filename}", 'wb+') as f:
            f.write(file.file.read())
            f.close()
        ima = Image.open(f"/usr/src/app/images//{file.filename}")
        # Parasamos a la libreria Pytesseract la imagen y con su metodo nos extrae el texto
        text = pytesseract.image_to_string(ima, "spa")
        # Finalmente devolvemos el texto JSON con el nombre del archivo y el texto extraido
        return {
            "filename": file.filename,
            "texto_imagen": text
        }
    else:
        # Abrimos lo que recibimos por request , lo guardamos en la carpeta correspondiente
        with open(f"images/{file.filename}",'wb+') as f:
            f.write(file.file.read())
            f.close()

        # Con la libreria Pillow cogemos la clase Image y cargamos la imagen guardada
        ima = Image.open(f"images/{file.filename}")
        # Parasamos a la libreria Pytesseract la imagen y con su metodo nos extrae el texto
        text = pytesseract.image_to_string(ima, "spa")
        # Finalmente devolvemos el texto JSON con el nombre del archivo y el texto extraido
        return {
            "filename": file.filename,
            "texto_imagen": text
        }
        