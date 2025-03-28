from flask import Flask, render_template, request
import qrcode
from io import BytesIO
import base64

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    qr_code_base64 = None  # Initialize variable to hold the QR code image
    
    if request.method == "POST":
        # Get user input
        data = request.form.get("data")
        version = int(request.form.get("version", 1))
        box_size = int(request.form.get("box_size", 10))
        border = int(request.form.get("border", 4))

        # Map error correction input to qrcode constants
        error_correction_levels = {
            "L": qrcode.constants.ERROR_CORRECT_L,
            "M": qrcode.constants.ERROR_CORRECT_M,
            "Q": qrcode.constants.ERROR_CORRECT_Q,
            "H": qrcode.constants.ERROR_CORRECT_H,
        }
        error_correction = error_correction_levels.get(request.form.get("error_correction", "M"))

        # Generate QR Code with user settings
        qr = qrcode.QRCode(
            version=version,
            error_correction=error_correction,
            box_size=box_size,
            border=border,
        )
        qr.add_data(data)
        qr.make(fit=True)

        # Convert QR code image to Base64
        img = qr.make_image(fill="black", back_color="white")
        img_io = BytesIO()
        img.save(img_io, format="PNG")
        img_io.seek(0)

        qr_code_base64 = base64.b64encode(img_io.getvalue()).decode()

    return render_template("index.html", qr_code_base64=qr_code_base64)

if __name__ == "__main__":
    app.run(debug=True)
