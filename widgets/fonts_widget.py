from tkinter import Frame, Canvas, Scrollbar, Label, Entry
from tkinter import X, Y, BOTH, W, NW, RIGHT, LEFT
from tools import get_fonts
from constants import COLORS


class FontItem(Frame):
    def __init__(self, parent, font: dict, command=None, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)

        self._font = font
        self._command = command
        self._selected = False

        self._create_widget()

    def get_name(self):
        return list(self._font.keys())[0]

    def get_styles(self):
        return [style for style in self._font[self.get_name()]]

    def get_path(self, style):
        return self._font[self.get_name()][style]

    def select(self):
        self._selected = True
        self._change_color()

    def deselect(self):
        self._selected = False
        self._change_color()

    def _create_widget(self):
        self.configure(width=220,
                       height=20,
                       bg=COLORS.FONT_BG)

        self.pack_propagate(False)

        self._font_name = Label(self,
                                bg=COLORS.FONT_BG,
                                fg=COLORS.FONT_TEXT,
                                text=self.get_name(),
                                font=(self.get_name(), 10),
                                anchor=W)
        self._separator = Frame(self,
                                bg=COLORS.FONT_SEPARATOR,
                                width=220)

        self.bind_config('<Enter>', self._change_color, COLORS.FONT_SEPARATOR)
        self.bind_config('<Leave>', self._change_color, COLORS.FONT_BG)
        self.bind_config('<Button-1>', self._command, self)

        self._font_name.pack(fill=X, padx=5)
        self._separator.place(x=0, y=19)

    def bind_config(self, event, func, data=None, call=True):
        self.bind(event,
                  lambda e: func(data) if data else func(e) if not call else func())
        self._font_name.bind(event, lambda e: func(data) if data else func(
            e) if not call else func())
        self._separator.bind(event, lambda e: func(data) if data else func(
            e) if not call else func())

    def _change_color(self, bg=COLORS.FONT_BG):
        if self._selected:
            bg = COLORS.FONT_SELECTED
        self.configure(bg=bg)
        self._font_name.configure(bg=bg)


class FontsContainer(Frame):
    def __init__(self, parent, command=None, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)

        self._command = command
        self._fonts = get_fonts()
        self._font_names = sorted(self._fonts.keys())
        self._selected_item = None

        self._create_widget()
        self._add_fonts()

    def _create_widget(self):
        self._search_entry = Entry(self,
                                   bg=COLORS.FONT_ENTRY_BG,
                                   fg=COLORS.FONT_ENTRY_TEXT)
        self._canvas = Canvas(self,
                              width=220,
                              highlightthickness=0,
                              bg=COLORS.MAIN)
        self._scrollbar = Scrollbar(self,
                                    command=self._canvas.yview)
        self._items_frame = Frame(self._canvas,
                                  bg=COLORS.MAIN)

        self._canvas.configure(yscrollcommand=self._scrollbar.set)
        self._canvas.create_window((0, 0),
                                   window=self._items_frame,
                                   anchor=NW)

        self._canvas.pack_propagate(False)

        self._search_entry.pack(fill=X)
        self._canvas.pack(side=LEFT,
                          fill=BOTH,
                          expand=True)
        self._scrollbar.pack(side=RIGHT,
                             fill=Y)

        self._search_entry.bind('<KeyRelease>',
                                lambda e: self._search_typing())
        self._items_frame.bind("<Configure>",
                               lambda e: self._configure_canvas())
        self._canvas.bind("<Configure>",
                          lambda e: self._configure_canvas())
        self._canvas.bind("<MouseWheel>", self._on_mousewheel)
        self._items_frame.bind("<MouseWheel>", self._on_mousewheel)

    def _configure_canvas(self):
        self._canvas.configure(scrollregion=self._canvas.bbox("all"))

    def _on_mousewheel(self, event):
        c_h = self._canvas.winfo_height()
        i_fr_h = self._items_frame.winfo_height()
        if c_h <= i_fr_h:
            self._canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _add_fonts(self):
        for font_name in self._font_names:
            item = FontItem(self._items_frame,
                            font={font_name: self._fonts[font_name]},
                            command=self._click)
            item.pack()
            item.bind_config("<MouseWheel>", self._on_mousewheel, call=False)

    def _search_typing(self):
        search_text = self._search_entry.get().lower()
        if search_text:
            items = [f for f in self._font_names if search_text in f.lower()]
        else:
            items = self._font_names

        for item in self._items_frame.winfo_children():
            item.destroy()

        self._selected_item = None

        for item in items:
            it = FontItem(self._items_frame,
                          font={item: self._fonts[item]},
                          command=self._click)
            it.pack()
            it.bind_config("<MouseWheel>", self._on_mousewheel, call=False)
        self._canvas.yview_moveto(0)

    def _click(self, font: FontItem = None):
        if self._selected_item:
            self._selected_item.deselect()
        self._selected_item = font
        font.select()
        if self._command:
            self._command(font)
