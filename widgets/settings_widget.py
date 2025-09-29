from tkinter import Frame, Label, Entry, Scale, Button, colorchooser
from tkinter.filedialog import askdirectory
from tkinter.ttk import Combobox
from tkinter import E, SE, HORIZONTAL, NORMAL, DISABLED
from PIL import ImageTk
from widgets.fonts_widget import FontItem

from constants import COLORS
from converters.converter_1bit import Converter1Bit
from converters.converter_rgb565 import ConverterRGB565

CONVERTERS = [Converter1Bit, ConverterRGB565]


class SettingsContainer(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)

        self._data = {
            'font': None,
            'font_path': None,
            'symbols_range': ' -~, А-я, Ё, ё, Ґ, ґ, І, і, Ї, ї, Є, є',
            'styles': ['Default'],
            'style': 'Default',
            'size': 20,
            'converters': [c().get_name() for c in CONVERTERS],
            'converter': CONVERTERS[0](),
            'scatter': 127,
            'fg': '#FFFFFF',
            'bg': '#000000',
            'preview_text': 'Lorem ipsum...',
            'original': Label(self, border=0),
            'preview': Label(self, border=0),
            'o_img': None,
            'p_img': None}

        self._labels = dict()
        self._labels_position_x = 10
        self._labels_position_y = 10
        self._labels_distance = 30

        self._create_widgets()
        self._configure_bind()
        self._pack_widgets()

    def _create_widgets(self):
        self.configure(bg=COLORS.MAIN)
        self.pack_propagate(False)

        self._create_label('Symbols')
        self._create_label('Style')
        self._create_label('Size')
        self._create_label('Converter')
        self._create_label('Scatter')
        self._create_label('Text color', state=DISABLED)
        self._create_label('Background', state=DISABLED)
        self._create_label('Preview text')
        self._create_label('Original')
        self._create_label('Preview', y=300)

        self._symbols_entry = Entry(self,
                                    width=38)
        self._symbols_entry.insert(0, self._data['symbols_range'])

        self._style_entry = Combobox(self,
                                     width=16,
                                     state='readonly',
                                     values=self._data['styles'])
        self._style_entry.current(0)

        self._size_entry = Entry(self,
                                 width=6)
        self._size_entry.insert(0, str(self._data['size']))

        self._converters = Combobox(self,
                                    width=16,
                                    state='readonly',
                                    values=self._data['converters'])
        self._converters.current(0)

        self._scatter_entry = Scale(self,
                                    from_=0,
                                    to=255,
                                    orient=HORIZONTAL,
                                    length=120,
                                    bg=COLORS.MAIN,
                                    fg=COLORS.FONT_TEXT,
                                    highlightthickness=0,
                                    command=self._scatter_entry_update)
        self._scatter_entry.set(self._data['scatter'])

        self._text_color_entry = Frame(self,
                                       width=20,
                                       height=20,
                                       bg=COLORS.DISABLED,
                                       highlightthickness=2,
                                       highlightbackground=COLORS.DISABLED)

        self._background_entry = Frame(self,
                                       width=20,
                                       height=20,
                                       bg=COLORS.DISABLED,
                                       highlightthickness=2,
                                       highlightbackground=COLORS.DISABLED)

        self._p_entry = Entry(self,
                              width=38)
        self._p_entry.insert(0, self._data['preview_text'])

        self._show_original()
        self._show_preview()

        self._convert_button = Button(self,
                                      text='Convert',
                                      width=20,
                                      command=self._save)

    def _configure_bind(self):
        self._symbols_entry.bind('<KeyRelease>', self._symbols_entry_update)
        self._size_entry.bind('<KeyRelease>', self._size_entry_update)
        self._style_entry.bind('<<ComboboxSelected>>',
                               self._style_entry_update)
        self._scatter_entry.bind('<MouseWheel>', self._scatter_mouse_wheel)
        self._p_entry.bind('<KeyRelease>',
                           self._preview_entry_update)
        self._converters.bind('<<ComboboxSelected>>',
                              self._converters_entry_update)

    def _pack_widgets(self):
        self._symbols_entry.place(x=110, y=10)
        self._style_entry.place(x=110, y=40)
        self._size_entry.place(x=110, y=70)
        self._converters.place(x=110, y=100)
        self._scatter_entry.place(x=110, y=120)
        self._text_color_entry.place(x=110, y=160)
        self._background_entry.place(x=110, y=190)
        self._p_entry.place(x=110, y=220)
        self._data['original'].place(x=110, y=250)
        self._data['preview'].place(x=110, y=300)
        self._convert_button.pack(anchor=SE, expand=True)

    def _create_label(self, text, y=None, state=None):
        label_name = '_'.join(text.lower().split(' ')) + '_lbl'
        label = Label(self,
                      text=text + ':',
                      width=12,
                      anchor=E,
                      bg=COLORS.MAIN,
                      fg=COLORS.SETTINGS_TEXT)
        state = NORMAL if not state else DISABLED
        label.configure(state=state)
        x = self._labels_position_x
        if not y:
            y = self._labels_position_y + len(
                self._labels) * self._labels_distance
        label.place(x=x, y=y)
        self._labels[label_name] = label

    def _show_original(self):
        converter = self._data['converter']
        font_path = self._data.get('font_path')
        text = self._data.get('preview_text')
        scatter = self._data.get('scatter')
        size = self._data.get('size')
        if converter.get_name() == '1-Bit':
            fg = '#FFFFFF'
            bg = '#000000'
        else:
            bg = self._data.get('bg')
            fg = self._data.get('fg')
        img = converter.get_original(font_path=font_path,
                                     text=text,
                                     scatter=scatter,
                                     bg=bg,
                                     fg=fg,
                                     size=size)
        self._data['o_img'] = ImageTk.PhotoImage(img)
        self._data['original'].configure(image=self._data['o_img'])

    def _show_preview(self):
        converter = self._data['converter']
        font_path = self._data.get('font_path')
        text = self._data.get('preview_text')
        scatter = self._data.get('scatter')
        size = self._data.get('size')
        if converter.get_name() == '1-Bit':
            fg = '#FFFFFF'
            bg = '#000000'
        else:
            bg = self._data.get('bg')
            fg = self._data.get('fg')
        img = converter.get_preview(font_path=font_path,
                                    text=text,
                                    scatter=scatter,
                                    bg=bg,
                                    fg=fg,
                                    size=size)
        self._data['p_img'] = ImageTk.PhotoImage(img)
        self._data['preview'].configure(image=self._data['p_img'])

    def _update_styles(self):
        self._data['styles'] = self._data['font'].get_styles()
        self._data['style'] = self._data['styles'][0]
        self._style_entry.configure(values=self._data['styles'])
        self._style_entry.current(0)

    def customize_font(self, font: FontItem):
        """
        Function that customize font
        :param font: FontItem
        :return: None
        """
        self._data['font'] = font

        self._update_styles()
        self._data['font_path'] = font.get_path(self._data.get('style'))

        self._show_original()
        self._show_preview()

    def _style_entry_update(self, event):
        font = self._data.get('font')
        self._data['style'] = self._style_entry.get()
        if font:
            self._data['font_path'] = font.get_path(self._data.get('style'))
        self.focus_force()
        self._show_original()
        self._show_preview()

    def _update_colors(self, entry):
        if entry == 'fg':
            self._data['fg'] = colorchooser.askcolor(title='Text color')[1]
            self._text_color_entry.configure(bg=self._data['fg'])
        elif entry == 'bg':
            self._data['bg'] = colorchooser.askcolor(title='Background color')[1]
            self._background_entry.configure(bg=self._data['bg'])

        self._show_original()
        self._show_preview()

    def _converters_entry_update(self, event):
        converter = self._converters.get()
        self._data['converter'] = CONVERTERS[self._converters.current()]()
        if converter == '1-Bit':
            self._labels['scatter_lbl'].configure(state=NORMAL)
            self._labels['text_color_lbl'].configure(state=DISABLED)
            self._text_color_entry.configure(bg=COLORS.DISABLED,
                                             highlightbackground=COLORS.DISABLED)
            self._labels['background_lbl'].configure(state=DISABLED)
            self._background_entry.configure(bg=COLORS.DISABLED,
                                             highlightbackground=COLORS.DISABLED)
            self._scatter_entry.configure(state=NORMAL)
            self._scatter_entry.set(self._data.get('scatter', 127))
            self._text_color_entry.unbind('<Enter>')
            self._text_color_entry.unbind('<Leave>')
            self._background_entry.unbind('<Enter>')
            self._background_entry.unbind('<Leave>')
        else:
            self._labels['scatter_lbl'].configure(state=DISABLED)
            self._labels['text_color_lbl'].configure(state=NORMAL)
            self._text_color_entry.configure(bg=self._data['fg'],
                                             highlightbackground=COLORS.BORDER_LEAVE)
            self._labels['background_lbl'].configure(state=NORMAL)
            self._background_entry.configure(bg=self._data['bg'],
                                             highlightbackground=COLORS.BORDER_LEAVE)
            self._scatter_entry.set(0)
            self._scatter_entry.configure(state=DISABLED)
            self._text_color_entry.bind(
                '<Enter>', lambda e: self._text_color_entry.configure(
                    highlightbackground=COLORS.BORDER_ENTER))
            self._text_color_entry.bind(
                '<Leave>', lambda e: self._text_color_entry.configure(
                    highlightbackground=COLORS.BORDER_LEAVE))
            self._text_color_entry.bind('<Button-1>',
                                        lambda e: self._update_colors('fg'))
            self._background_entry.bind(
                '<Enter>', lambda e: self._background_entry.configure(
                    highlightbackground=COLORS.BORDER_ENTER))
            self._background_entry.bind(
                '<Leave>', lambda e: self._background_entry.configure(
                    highlightbackground=COLORS.BORDER_LEAVE))
            self._background_entry.bind('<Button-1>',
                                        lambda e: self._update_colors('bg'))

        self._show_original()
        self._show_preview()
        self.focus_force()

    def _scatter_entry_update(self, event):
        converter = self._data.get('converter').get_name()
        if converter == '1-Bit':
            self._data['scatter'] = self._scatter_entry.get()
        self._show_preview()

    def _scatter_mouse_wheel(self, event):
        change = 1 if event.delta > 1 else -1
        new_value = self._scatter_entry.get() + change
        if change < new_value >= 0:
            self._scatter_entry.set(new_value)
        elif new_value <= 255:
            self._scatter_entry.set(new_value)

    def _preview_entry_update(self, event):
        self._data['preview_text'] = self._p_entry.get()
        self._show_original()
        self._show_preview()

    def _symbols_entry_update(self, event):
        self._data['symbols_range'] = self._symbols_entry.get()

    def _size_entry_update(self, event):
        size = self._size_entry.get()
        self._data['size'] = int(size) if size else 1
        self._show_original()
        self._show_preview()

    @staticmethod
    def _get_symbols(symbols):
        result = []
        if symbols:
            print(symbols)
            symbols = symbols.split(', ')
            print(symbols)
            for symbols_range in symbols:
                symbols = sorted(symbols_range.split('-'))
                symbols = [chr(idx) for idx in range(ord(symbols[0]),
                                                     ord(symbols[-1]) + 1)]
                result += symbols
        return ''.join(sorted(result))

    def _save(self):
        if self._data.get('font'):
            self._data['symbols'] = self._get_symbols(self._data.get('symbols_range'))
            data = self._data['converter'].get_array(**self._data)
            file_name = data['h'].split('\n')[0].split(' ')[-1][2:-2]
            path = askdirectory()
            if path:
                with open(f'{path}/{file_name}.h', 'w', encoding='utf-8') as file:
                    file.write(data['h'])
                with open(f'{path}/{file_name}.c', 'w', encoding='utf-8') as file:
                    file.write(data['c'])
