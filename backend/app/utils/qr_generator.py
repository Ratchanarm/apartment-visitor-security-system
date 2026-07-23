import qrcode
import io
import base64
import secrets
from typing import Tuple


def generate_qr_code(data: str) -> Tuple[str, str]:
    """Generate QR code and return base64 encoded image and token."""
    token = secrets.token_urlsafe(32)
    qr_data = f"{data}|{token}"
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_data)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    
    base64_image = base64.b64encode(buffer.getvalue()).decode()
    return f"data:image/png;base64,{base64_image}", token
