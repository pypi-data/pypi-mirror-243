import fitz
import shutil
from pathlib import Path
import os
from io import BytesIO
from pyzbar.pyzbar import decode, ZBarSymbol
from PIL import Image
import os
import re
import jwt
 
def extract_qr_cae_from_invoice_pdf_and_decode(filepath):

    base_name = Path(filepath).stem

    pdf_file = fitz.open(filepath)
    image_list = pdf_file[0].get_images()
    
    for image_index, img in enumerate(image_list):
        xref = img[0]
        base_image = pdf_file.extract_image(xref)

        image_bytes = base_image["image"]
        image_ext = base_image["ext"]

        img = Image.open(BytesIO(image_bytes))

        decoded_list = decode(img)

        if decoded_list:
            result = re.match('https:\/\/www\.afip\.gob\.ar\/fe\/qr\/\?p=(.*)', bytes.decode(decoded_list[0].data))
            jwt_qr_url = result[1]

            decoded_token = bytes.decode(jwt.utils.base64url_decode(jwt_qr_url))
            return decoded_token
        
