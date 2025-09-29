class PATH:
    BASE = __file__.rsplit('\\', 1)[0] + '\\'
    RESOURCES = f'{BASE}resources\\'
    IMAGES = f'{RESOURCES}images\\'

    ICON_IMAGE = f'{IMAGES}icon.ico'


class COLORS:
    MAIN = '#333333'
    FONT_ENTRY_BG = '#444444'
    FONT_ENTRY_TEXT = '#AAAAAA'
    FONT_BG = '#4B4B4B'
    FONT_SEPARATOR = '#636363'
    FONT_TEXT = '#C3C3C3'
    FONT_SELECTED = '#2D2D2D'
    SETTINGS_TEXT = '#EEEEEE'
    DISABLED = FONT_ENTRY_TEXT
    BORDER_LEAVE = MAIN
    BORDER_ENTER = FONT_ENTRY_TEXT
