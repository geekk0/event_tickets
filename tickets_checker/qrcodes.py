from PIL import Image
import qrcode

class QRCode:
    def __init__(self, qr_data):
        self.data = qr_data
        self.image = None

    def create_qr_code_image(self):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(self.data)
        qr.make(fit=True)

        # Generate PIL image from the QR code
        self.image = qr.make_image(fill_color="black", back_color="white")


def paste_qr_code(background_image_path, qr_data, output_image_path, qr_position):
    # Open the background image
    background = Image.open(background_image_path)

    # Create QR code instance
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_data)
    qr.make(fit=True)

    # Create QR code image
    qr_image = qr.make_image(fill_color="black", back_color="white")

    # Calculate the position to paste the QR code
    qr_position_x, qr_position_y = qr_position

    # Paste the QR code onto the background image
    background.paste(qr_image, (qr_position_x, qr_position_y))

    # Save the resulting image
    background.save(output_image_path)

# Example usage
# background_image_path = "background_image.png"
# qr_data = "https://example.com"
# output_image_path = "output_image.png"
# qr_position = (100, 100)  # Example position, adjust as needed
#
# paste_qr_code(background_image_path, qr_data, output_image_path, qr_position)

# Create an instance of QRCode
# qr_code = QRCode("https://example.com")
#
# # Generate the QR code image
# qr_code.create_qr_code_image()
#
# # Show the resulting QR code image
# if qr_code.image:
#     qr_code.image.show()
# else:
#     print("QR code image has not been generated yet.")

