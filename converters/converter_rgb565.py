from converters.base_converter import BaseConverter


class ConverterRGB565(BaseConverter):
    def __init__(self):
        self._name = 'RGB565'
        super(ConverterRGB565, self).__init__()

    def _convert(self, pixel, *args, **kwargs):
        output_type = kwargs.get('type')

        if output_type == 'bits':
            return f'{format(pixel[0], "08b")[:5]}' \
                   f'{format(pixel[1], "08b")[:6]}' \
                   f'{format(pixel[2], "08b")[:5]}'

        pixel = (pixel[0] & 0xF8, pixel[1] & 0xFC, pixel[2] & 0xF8)

        return pixel


if __name__ == '__main__':
    _converter = ConverterRGB565()
    print(_converter.get_name())
    print(_converter._convert((255, 13, 127), type='pixel'))
    print(_converter._convert((255, 13, 127), type='bits'))
    _converter.get_array(font_path='C:\\Windows\\Fonts\\BOD_BLAR.TTF',
                         size=48,
                         # symbols_range=' -/, 0-9, A-Z, a-z, А-Я, а-я, Ґ, ґ, Ї, ї, Є, є',
                         symbols_range='H',
                         bg='#FFFFFF',
                         fg='#000000')