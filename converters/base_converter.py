import pprint
from typing import Union

from PIL import Image, ImageFont, ImageDraw


class BaseConverter:
    def __init__(self):
        if not self.__dict__.get('_name'):
            raise NotImplementedError(
                'Please implement self._name = "converter name" in "__init__.py" block!')

    def get_name(self):
        return self.__dict__.get('_name')

    @staticmethod
    def get_original(*args, **kwargs):
        font_path = kwargs.get('font_path')
        text = kwargs.get('text', 'Original')
        text = text if text else 'Original'
        bg = kwargs.get('bg', '#FFFFFF')
        fg = kwargs.get('fg', '#000000')
        size = kwargs.get('size', 24)
        size = size if size <= 24 else 24
        image = Image.new("RGB", (233, 40), bg)
        if font_path:
            image_font = ImageFont.truetype(font_path, size, encoding='utf-8')
            l, t, lw, th = image_font.getbbox(text)
            draw = ImageDraw.Draw(image)
            draw.text((5, (40 - th) // 2), text, fg, font=image_font)
        return image

    def get_preview(self, *args, **kwargs):
        kwargs['text'] = kwargs['text'] if kwargs.get('text') else 'Preview'
        scatter = kwargs.get('scatter', 127)
        image = self.get_original(**kwargs).copy()
        pixels = list(image.getdata())
        preview_pixels = []
        preview_image = Image.new('RGB', (233, 40))
        for pixel in pixels:
            preview_pixels.append(self._convert(pixel, scatter=scatter))
        preview_image.putdata(preview_pixels)
        return preview_image

    def get_array(self, *args, **kwargs):
        result = {'c': '',
                  'h': ''}
        data = list()
        array_length = 0
        font_name = '_'.join(kwargs['font'].get_name().lower().split(' '))
        style = '_'.join(kwargs['style'].lower().split(' '))
        size = str(kwargs['size'])
        name = '_'.join([font_name, style, size])
        symbols = kwargs.get('symbols', '') + '█'
        symbols_count = f'0x{len(symbols) >> 8:>02X}, 0x{len(symbols) & 0x00ff:>02X}'
        converter_name = kwargs.get('converter').get_name()
        converter = 1
        if converter_name == '1-Bit':
            converter = 1
        elif converter_name == 'RGB565':
            converter = 565
        converter = f'0x{converter >> 8:>02X}, 0x{converter & 0x00ff:>02X}'

        for symbol in symbols:
            symbol_array = self._symbol_to_array(*args, **kwargs, symbol=symbol)
            array_length += len(symbol_array)
            data.append(self._format_symbol_array(symbol_array))

        result['h'] = f'#ifndef __{name}_H\n'
        result['h'] += f'#define __{name}_H\n\n'
        result['h'] += f'extern char {name}[{array_length + 4}];\n\n'
        result['h'] += f'#endif\n'

        result['c'] = f'const char {name}[{array_length + 4}] =\n\t{{\n'
        result['c'] += f"\t\t{converter}, // Type: '{converter_name}'\n"
        result['c'] += f"\t\t{symbols_count}, // Symbols count: '{len(symbols)}'\n\n"
        for item in data[:-1]:
            result['c'] += f'{item},\n'
            result['c'] += f'\t\t// {"".ljust(68, "*")}\n\n'
        result['c'] += f'{data[-1]}\n'
        result['c'] += f'\t\t// {"".ljust(68, "*")}\n'
        result['c'] += f'\t}};\n\n'

        return result

    @staticmethod
    def _get_symbols_height(*args, **kwargs):
        image_font = ImageFont.truetype(kwargs.get('font_path'),
                                        kwargs.get('size'),
                                        encoding='utf-8')
        l, t, lw, th = image_font.getbbox(kwargs.get('symbols'))
        return th

    def _create_symbol_image(self, *args, **kwargs):
        image_font = ImageFont.truetype(kwargs.get('font_path'),
                                        kwargs.get('size'),
                                        encoding='utf-8')
        l, t, lw, th = image_font.getbbox(kwargs.get('symbol'))
        image = Image.new("RGB",
                          (lw, self._get_symbols_height(*args, **kwargs)),
                          kwargs.get('bg'))
        draw = ImageDraw.Draw(image)
        draw.text((0, 0),
                  kwargs.get('symbol'),
                  kwargs.get('fg'),
                  font=image_font)
        return image

    @staticmethod
    def _to_uint(data):
        """

        :param data:
        :return:
        """
        result = []
        diff = 8 - (len(data) % 8) if len(data) % 8 else 0
        data += '0' * diff
        for idx in range(0, len(data), 8):
            result.append(f"0x{int(data[idx: idx + 8], 2):>02X}")
        return result

    def _symbol_to_array(self, *args, **kwargs):
        symbol_image = self._create_symbol_image(*args, **kwargs)
        w, h = symbol_image.size
        bits = list(
            map(lambda pixel: self._convert(pixel,
                                            type='bits',
                                            scatter=kwargs.get('scatter', 127)),
                list(symbol_image.getdata())))
        bits = ''.join(bits)
        bytes_array = self._to_uint(bits)

        symbol = kwargs.get("symbol")
        bytes_count = len(bytes_array)

        bytes_array.insert(0, f'0x{ord(symbol) >> 8:>02X}')
        bytes_array.insert(1, f'0x{ord(symbol) & 0xFF:>02X}')
        bytes_array.insert(2, f'0x{w >> 8:>02X}')
        bytes_array.insert(3, f'0x{w & 0xFF:>02X}')
        bytes_array.insert(4, f'0x{h >> 8:>02X}')
        bytes_array.insert(5, f'0x{h & 0xFF:>02X}')
        bytes_array.insert(6, f'0x{bytes_count >> 8:02X}')
        bytes_array.insert(7, f'0x{bytes_count & 0xFF:02X}')

        return bytes_array

    @staticmethod
    def _format_symbol_array(arr):
        result = f'\t\t{arr[0]}, {arr[1]}, // Alias: '
        result += f"'{chr(int(f'0x{arr[0][2:]}{arr[1][2:]}', 16))}'\n"

        result += f'\t\t{arr[2]}, {arr[3]}, // Symbol width: '
        result += f'{int(f"0x{arr[2][2:]}{arr[3][2:]}", 16)}\n'

        result += f'\t\t{arr[4]}, {arr[5]}, // Symbol height: '
        result += f'{int(f"0x{arr[4][2:]}{arr[5][2:]}", 16)}\n'

        result += f'\t\t{arr[6]}, {arr[7]}, // Bytes count: '
        result += f'{int(f"0x{arr[6][2:]}{arr[7][2:]}", 16)}\n'

        result += f'\t\t// {"Data ".ljust(68, "*")}\n'

        lines = ''
        line = f'\t\t{arr[8]}'
        for item in arr[9:]:

            if len(f'{line}, {item}') <= 72:
                line = f'{line}, {item}'
            else:
                lines += f'{line},\n'
                line = f'\t\t{item}'
        lines += f'{line}'

        result += lines
        return result

    def _convert(self, pixel, *args, **kwargs):
        """
        Method that converts RGB pixel.
        The method must be able to handle the <type = 'bits']> value
        For <type = None> it must return tuple with three converted values (R, G, B)
        For <type = 'bits'> it must return string with converted bits of pixel

        Example for <type = None> RGB565 converter:
            input: (255, 13, 255) => R to 5 bits, G to 6 bits, B to 5 bits
            output: (248, 12, 248)

        Example for <type = 'bits'> RGB565 converter:
            input: (255, 13, 255) => R to 5 bits, G to 6 bits, B to 5 bits
            output: '1111100001111111'

        :param pixel: pixel RGB values (int, int, int)
        :return: <tuple(R, G, B)>
                 for <type = 'bits'> string '100100'
        """
        raise NotImplementedError(
            'You must implement method <def _convert(self, pixel, *args, **kwargs):>')
