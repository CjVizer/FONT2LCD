from tkinter import Tk
from tkinter import LEFT, Y, BOTH, W
from constants import PATH, COLORS
from widgets import FontsContainer, SettingsContainer


class App(Tk):
    def __init__(self):
        super(App, self).__init__()

        self.geometry('594x374')
        self.title('FONT2LCD')
        self.configure(bg=COLORS.MAIN)
        self.resizable(False, False)
        self.iconbitmap(PATH.ICON_IMAGE)

        self._create_app()

    def _create_app(self):
        self.pack_propagate(False)

        self._font_container = FontsContainer(self, self._font_click)
        self._font_container.pack(fill=Y,
                                  expand=True,
                                  side=LEFT,
                                  anchor=W)

        self._settings_container = SettingsContainer(self,
                                                     width=354,
                                                     height=364)
        self._settings_container.pack(fill=BOTH,
                                      side=LEFT,
                                      expand=True)

    def _font_click(self, font):
        self._settings_container.customize_font(font)


if __name__ == '__main__':
    app = App()
    app.mainloop()
