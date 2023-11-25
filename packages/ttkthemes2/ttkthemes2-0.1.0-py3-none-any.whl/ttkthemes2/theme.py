class TtkThemes2(object):
    def __init__(self, theme_name: str = None):
        from tkinter import ttk, _default_root
        self.root = _default_root

        from tksvg import load
        load(self.root)

        self.style = ttk.Style(self.root)

        if theme_name:
            from ttkthemes2.core import load
            load(theme_name)
            self.style.theme_use(theme_name)

    def use_theme_name(self, theme_name: str):
        from ttkthemes2.core import load
        load(theme_name)
        self.style.theme_use(theme_name)

    def theme_names(self):
        return [
            "awthemes", "colorutils", "awarc", "awblack", "awbreeze",
            "awbreezedark", "awclearlooks", "awdark", "awlight",
            "awtemplate", "awwinxpblue"
        ]


from tkinter import Tk


class Themed2Tk(Tk):
    def __init__(self, *args, theme_name=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.theme = TtkThemes2(theme_name=theme_name)

    def use_theme_name(self, theme_name: str):
        self.theme.use_theme_name(theme_name=theme_name)


if __name__ == '__main__':
    from tkinter import Tk, ttk, StringVar

    root = Themed2Tk(theme_name="awbreezedark")

    window = ttk.Frame(root)

    button = ttk.Button(window, text="TtkButton")
    button.pack(padx=10, pady=10, fill="x")

    entry_var = StringVar(value="TtkEntry")

    entry = ttk.Entry(window, textvariable=entry_var)
    entry.pack(padx=10, pady=10, fill="x")

    window.pack(fill="both", expand="yes")

    root.mainloop()