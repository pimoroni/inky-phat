__version__ = "1.0.0"

from . import il91874
from . import fonts
from PIL import Image, ImageFont, ImageDraw

BLACK = 0
WHITE = 1
RED = 2

WIDTH = 212
HEIGHT = 104

_image = Image.new('P', (WIDTH, HEIGHT))

_draw = ImageDraw.Draw(_image)

_panel = il91874.IL91874(resolution=(HEIGHT, WIDTH), h_flip=False, v_flip=True)

_panel.set_palette((il91874.BLACK, il91874.WHITE, il91874.RED))

# Export drawing methods into the module namespace
for method in dir(_draw):
    if not method.startswith("_"):
        globals()[method] = getattr(_draw, method)

def set_image(image):
    global _image
    if hasattr(image, 'getpixel'):
        _image = image

def get_image():
    return _image

def show():
    for y in range(WIDTH):
        for x in range(HEIGHT):
            _panel.set_pixel(x, y, _image.getpixel((y, x)))

    _panel.update()


