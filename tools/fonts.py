import matplotlib.font_manager
from PIL import ImageFont


def get_fonts():
    """
    Function that returns system fonts.
    :return: Dict with fonts {font_name1: {font_style1: font_path,
                                           font_style2: font_path},
                              font_name2: {font_style1: font_path,
                                           font_style2: font_path}}
    """
    fonts = dict()
    for font_path in matplotlib.font_manager.findSystemFonts():
        font = ImageFont.FreeTypeFont(font_path)
        name, weight = font.getname()
        if name in fonts.keys():
            fonts[name][weight] = font_path
        else:
            fonts[name] = {weight: font_path}
    return fonts
