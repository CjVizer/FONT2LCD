from converters.base_converter import BaseConverter


class Converter1Bit(BaseConverter):
    def __init__(self):
        self._name = '1-Bit'
        super(Converter1Bit, self).__init__()

    def _convert(self, pixel, *args, **kwargs):
        output_type = kwargs.get('type')
        scatter = 255 - kwargs.get('scatter', 127)

        color_value = 255 if sum(pixel) // 3 > scatter else 0
        pixel = (color_value, color_value, color_value)

        if output_type == 'bits':
            return '1' if color_value else '0'
        else:
            return pixel
