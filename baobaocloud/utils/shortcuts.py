import random
import string
import time
from datetime import datetime
from StringIO import StringIO

from django.contrib.sessions.models import Session
from PIL import Image, ImageDraw, ImageFont

from baobaocloud.utils.const import msg_code


VERIFY_CODE_CHARS = string.ascii_letters + string.digits

def get_random_string(length=1, allowed_chars=VERIFY_CODE_CHARS):
    chars = ''
    for i in range(length):
        chars += random.choice(allowed_chars)
    return chars

def get_string_imageflow(chars, image_width=80, image_height=32):
    chars_length = len(chars)
    font_size = int(min(image_width / chars_length, image_height) * 0.9)
    image_bgcolor = (random.randint(200, 255), random.randint(200, 255), random.randint(200, 255))
    image = Image.new('RGB', (image_width, image_height), image_bgcolor)
    font = ImageFont.truetype('consola.ttf', font_size)
    draw = ImageDraw.Draw(image)
    for i, char in enumerate(chars):
        char_color = (random.randint(0, 150), random.randint(0, 150), random.randint(0, 150))
        offset_left = (image_width / chars_length * i) + (image_width / chars_length - font_size) / 2
        offset_top = (image_height - font_size) / 2
        coordinate = (offset_left, offset_top)
        draw.text(coordinate, char, char_color, font)
    for i in range(10):
        asterisk_color = (255, 255, 255)
        offset_left = random.randint(0, image_width)
        offset_top = random.randint(0, image_height)
        coordinate = (offset_left, offset_top)
        draw.text(coordinate, '*', asterisk_color, font)
    for i in range(3):
        line_color = (random.randint(0, 150), random.randint(0, 150), random.randint(0, 150))
        coordinate = (
            random.randint(0, image_width), random.randint(0, image_height),
            random.randint(0, image_width), random.randint(0, image_height),
        )
        draw.line(coordinate ,line_color)
    mstream = StringIO()
    image.save(mstream, 'jpeg')
    string_imageflow = mstream.getvalue()
    return string_imageflow

def get_rest_session_time(session):
    try:
        s = Session.objects.get(session_key=session.session_key)
        expire_date = s.expire_date.replace(tzinfo=None)
        now = datetime.utcnow()
        rest_session_timedelta = expire_date - now
        rest_session_time = rest_session_timedelta.seconds
        return rest_session_time
    except Exception:
        return 0

def get_msg_code(code):
    return msg_code[code]
