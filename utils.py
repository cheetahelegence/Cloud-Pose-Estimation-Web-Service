import base64
from io import BytesIO
from PIL import Image

def decode_base64_image(base64_string):
    """
    Decodes a base64 string into a PIL image.
    """
    try:
        # Remove header if present (e.g. "data:image/jpeg;base64,...")
        if "," in base64_string:
            base64_string = base64_string.split(",")[1]

        image_data = base64.b64decode(base64_string)
        image = Image.open(BytesIO(image_data)).convert("RGB")
        return image
    except Exception as e:
        raise ValueError(f"Failed to decode base64 image: {str(e)}")

def encode_image_to_base64(image_path):
    """
    Read an image file and return it as a base64-encoded string.
    """
    try:
        with open(image_path, "rb") as img_file:
            encoded = base64.b64encode(img_file.read()).decode("utf-8")
            return encoded
    except FileNotFoundError:
        raise FileNotFoundError(f"Image file not found: {image_path}")
    except Exception as e:
        raise ValueError(f"Failed to encode image to base64: {str(e)}")

