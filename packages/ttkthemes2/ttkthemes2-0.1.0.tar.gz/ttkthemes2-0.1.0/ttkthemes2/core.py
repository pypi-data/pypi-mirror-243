import contextlib
import os


@contextlib.contextmanager
def chdir(target: str):
    """Context-managed chdir, original implementation by GitHub @Akuli"""
    current = os.getcwd()
    try:
        os.chdir(target)
        yield
    finally:
        os.chdir(current)


def load(module):
    global _load_scrollutil
    from tkinter import _default_root
    local = os.path.abspath(os.path.dirname(__file__))
    awthemes = os.path.join(local, "awthemes-10.4.0")
    with chdir(awthemes):
        _default_root.tk.eval("set dir [file dirname [info script]]")
        _default_root.tk.call("source", "pkgIndex.tcl")
        _default_root.tk.call("package", "require", module)


if __name__ == '__main__':
    from tkinter import Tk, ttk

    root = Tk()
    root.setvar("::nosvg", True)

    load("awthemes")
    load("awdark")
    load("awlight")

    style = ttk.Style(root)
    style.theme_use("awlight")

    window = ttk.Frame(root)

    button = ttk.Button(window, text="Hello World")
    button.pack()

    window.pack(fill="both", expand="yes")

    root.mainloop()
