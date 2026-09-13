"""Minimal stand-ins for the graphics libraries so the game logic can be tested.

cmu_graphics and PIL are not available in a headless test environment, so the
drawing calls are replaced by no-ops before finalProject is imported.
"""
import sys
import types


def _noop(*args, **kwargs):
    return None


def installStubs():
    if 'cmu_graphics' not in sys.modules:
        cmuGraphics = types.ModuleType('cmu_graphics')
        for name in ('drawPolygon', 'drawLabel', 'drawImage', 'drawRect',
                     'drawLine', 'drawCircle', 'drawOval', 'drawStar',
                     'setActiveScreen', 'runApp', 'runAppWithScreens'):
            setattr(cmuGraphics, name, _noop)
        cmuGraphics.CMUImage = lambda image: image
        sys.modules['cmu_graphics'] = cmuGraphics

    if 'PIL' not in sys.modules:
        pil = types.ModuleType('PIL')
        imageModule = types.ModuleType('PIL.Image')

        class FakeImage:
            def __init__(self, size=(1, 1), mode='RGBA'):
                self.size = size
                self.mode = mode

            def convert(self, mode):
                self.mode = mode
                return self

        def openImage(path):
            import os
            if not os.path.exists(path):
                raise FileNotFoundError(path)
            return FakeImage()

        imageModule.open = openImage
        imageModule.new = lambda mode, size, color=None: FakeImage(size, mode)
        pil.Image = imageModule
        sys.modules['PIL'] = pil
        sys.modules['PIL.Image'] = imageModule
