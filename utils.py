import base64
from io import BytesIO


def base64_to_img(img):
    return BytesIO(base64.b64decode(img.split(',')[1]))


def pil_to_base64(pil_image):
    # 将PIL对象保存为BytesIO流
    byte_arr = BytesIO()
    pil_image.save(byte_arr, format='PNG')
    byte_arr = byte_arr.getvalue()

    # 将二进制数据编码为Base64格式
    base64_str = base64.b64encode(byte_arr).decode('utf-8')

    return base64_str
