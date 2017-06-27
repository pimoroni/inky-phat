.. role:: python(code)
   :language: python

.. toctree::
   :titlesonly:
   :maxdepth: 0

Welcome
-------

This documentation will guide you through the methods available in the Inky pHAT python library.

* More information - https://shop.pimoroni.com/products/inky-phat
* Get the code - https://github.com/pimoroni/inky-phat
* Get started - https://learn.pimoroni.com/tutorial/sandyj/getting-started-with-inky-phat
* Get help - http://forums.pimoroni.com/c/support

Note
----

Inky pHAT is based heavily upon the PIL/Pillow Python Imaging Library. It uses PIL drawing methods,
fonts and images in indexed-palette mode with the colours 0, 1 and 2 corresponding to White, Black and Red.

Some documentation is missing for PIL methods below. For general documentation about PIL/Pillow please visit: https://pillow.readthedocs.io

At A Glance
-----------

.. automoduleoutline:: inkyphat
   :members:

.. automethod:: inkyphat._image.paste
.. automethod:: inkyphat._image.getpixel
.. automethod:: inkyphat._image.putpixel
.. automethod:: inkyphat._draw.point
.. automethod:: inkyphat._draw.arc
.. automethod:: inkyphat._draw.pieslice
.. automethod:: inkyphat._draw.ellipse
.. automethod:: inkyphat._draw.line
.. automethod:: inkyphat._draw.rectangle
.. automethod:: inkyphat._draw.polygon
.. automethod:: inkyphat._draw.text

Paste An Image
--------------

.. automethod:: inkyphat._image.paste

Get A Pixel
-----------

.. automethod:: inkyphat._image.getpixel

Put A Pixel
-----------

From PIL.Image

.. automethod:: inkyphat._image.putpixel


From PIL.ImageDraw

.. automethod:: inkyphat._draw.point

Draw An Arc
-----------

From PIL.ImageDraw

.. automethod:: inkyphat._draw.arc
.. automethod:: inkyphat._draw.pieslice

Draw An Ellipse
---------------

From PIL.ImageDraw

.. automethod:: inkyphat._draw.ellipse

Draw A Line
-----------

From PIL.ImageDraw

.. automethod:: inkyphat._draw.line

Draw A Rectangle
----------------

From PIL.ImageDraw

.. automethod:: inkyphat._draw.rectangle

Draw A Polygon
--------------

From PIL.ImageDraw

.. automethod:: inkyphat._draw.polygon

Draw Some Text
--------------

From PIL.ImageDraw

.. automethod:: inkyphat._draw.text

Note: You can use :python:`inkyphat.ImageFont(inkyphat.fonts.FONTNAME, FONTSIZE)` to supply a font.

Fonts
-----

Inky pHAT ships with some built-in OFL fonts for your convenience. You can list them by importing `inkyphat` and typing `dir(inkyphat.fonts)`

* :python:`inkyphat.fonts.AmaticSCBold`
* :python:`inkyphat.fonts.AmaticSC`
* :python:`inkyphat.fonts.FredokaOne`
* :python:`inkyphat.fonts.PressStart2P`

Constants
---------

* :python:`inkyphat.WHITE = 0`
* :python:`inkyphat.BLACK = 1`
* :python:`inkyphat.RED = 2`
