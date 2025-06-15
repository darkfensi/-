from PIL import Image
import numpy as np
import hashlib

def extract_icon_from_image(path):
    try:
        img = Image.open(path)
        return img.crop((0, 0, 128, 128))
    except:
        return None

def phash(img):
    img = img.convert("L").resize((8, 8), Image.ANTIALIAS)
    pixels = np.array(img).flatten()
    avg = pixels.mean()
    bits = "".join(['1' if p > avg else '0' for p in pixels])
    return hex(int(bits, 2))

def extract_features(img_or_path):
    if isinstance(img_or_path, str):
        img = Image.open(img_or_path)
    else:
        img = img_or_path
    return {
        "phash": phash(img),
        "clip": get_clip_vector(img)
    }

def get_clip_vector(img):
    h = hashlib.sha256(img.tobytes()).hexdigest()
    return h

def compare_features_clip(vec1, vec2):
    return 1.0 if vec1 == vec2 else 0.0