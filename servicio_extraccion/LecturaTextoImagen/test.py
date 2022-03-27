import requests

ficheros = {'file': open('images_test/cursopy.png', 'rb')}

url = "http://127.0.0.1:8000/uploadfile/"
print(requests.post(url, files=ficheros).json()['texto_imagen'])