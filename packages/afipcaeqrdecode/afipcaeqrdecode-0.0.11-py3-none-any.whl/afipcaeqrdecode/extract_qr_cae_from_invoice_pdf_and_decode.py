import fitz
from pathlib import Path
import numpy as np
import cv2
import re
import jwt
from qreader import QReader

qreader = QReader(model_size='l', min_confidence=0.5)

def extract_qr_cae_from_invoice_pdf_and_decode(filepath):

    pdf_file = fitz.open(filepath)
    image_list = pdf_file[0].get_images()

    for image_index, img in enumerate(image_list):

        xref = img[0]
        base_image = pdf_file.extract_image(xref)

        image_bytes = base_image["image"]
        image_ext = base_image["ext"]

        image_np = np.frombuffer(image_bytes, np.uint8)
        image_opencv = cv2.imdecode(image_np, cv2.IMREAD_COLOR)

        decoded_tuple = qreader.detect_and_decode(image_opencv)
        
        if decoded_tuple:
            result = re.match('https:\/\/(?:www\.)?afip\.gob\.ar\/fe\/qr\/?\?p=(.*)', decoded_tuple[0])

            if result:
                jwt_qr_url = result[1]
                decoded_token = bytes.decode(jwt.utils.base64url_decode(jwt_qr_url))
                return decoded_token.replace(' ','').replace('\r', '').replace('\n','').replace('\t', '')