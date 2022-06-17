#%%
import os, io
from google.cloud import vision_v1 as vision
from google.cloud.vision_v1 import types

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'VisionAPIDemo\google_cloud_sa.json'
client = vision.ImageAnnotatorClient()
#%%

# Folder with images
FOLDER_PATH = r'sample_images'
# Imagen de prueba
IMAGE_FILE = r'img_3.png'
# Unimos ambos paths
FILE_PATH = os.path.join(FOLDER_PATH, IMAGE_FILE)

#%%

# Guardo el contenido binario de la imagen
with io.open(FILE_PATH, 'rb') as image_file:
    content = image_file.read()

image = vision.types.Image(content=content)
response = client.document_text_detection(image=image, image_context={'language_hints':['en']})
docText = response.full_text_annotation.text

# Reemplazamos los saltos de pagina por un espacio en blanco
doc = docText.replace('\n', " ")

# Hacemos un loop para analizar la confianza de los distintos simbolos y parrafos
pages = response.full_text_annotation.pages
for page in pages:
    for block in page.blocks:
        print('block confidence:', block.confidence)

        for paragraph in block.paragraphs:
            print('paragraph confidence:', paragraph.confidence)

            for word in paragraph.words:
                word_text = ''.join([symbol.text for symbol in word.symbols])

                print(f'Word text: {word_text} (confidence: {word.confidence}')

                for symbol in word.symbols:
                    print(f'\tSymbol: {symbol.text} (confidence: {symbol.confidence}')

#%%
