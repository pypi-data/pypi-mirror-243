from pdf2image import convert_from_path
import numpy as np
import cv2
import tempfile
from qreader import QReader
import re
import jwt

qreader = QReader(model_size='l', min_confidence=0.5)

def convert_pdf_to_image_and_detect_and_decode_qrs(filepath):

    with tempfile.TemporaryDirectory() as path:
        
        images_from_path = convert_from_path(filepath, output_folder=path)
        numpy_array = np.array(images_from_path[0])
        
        opencv_image = cv2.cvtColor(numpy_array, cv2.COLOR_RGB2BGR)
        
        decoded_qrs = qreader.detect_and_decode(opencv_image)

        for decoded_qr in decoded_qrs:
            if decoded_qr:
                result = re.match('https:\/\/(?:www\.)?afip\.gob\.ar\/fe\/qr\/\?p=(.*)', decoded_qr)

                if result:
                    jwt_qr_url = result[1]
                    decoded_token = bytes.decode(jwt.utils.base64url_decode(jwt_qr_url))
                    return decoded_token.replace(' ','').replace('\r', '').replace('\n','').replace('\t', '')