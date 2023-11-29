from .extract_qr_cae_from_invoice_pdf_and_decode import extract_qr_cae_from_invoice_pdf_and_decode
from .convert_pdf_to_image_and_detect_and_decode_qrs import convert_pdf_to_image_and_detect_and_decode_qrs


def get_cae_metadata(filepath):
    
    cae_metadata = extract_qr_cae_from_invoice_pdf_and_decode(filepath)
    
    if not cae_metadata:
        cae_metadata = convert_pdf_to_image_and_detect_and_decode_qrs(filepath)
    
    return cae_metadata