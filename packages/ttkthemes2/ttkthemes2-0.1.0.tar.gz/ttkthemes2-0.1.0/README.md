# TtkTheme2
受`ttkthemes`灵感而发，目的只是为了补充`ttkthemes`的主题。

> 维护者：[XiangQinxi](mailto:XiangQinxi@outlook.com)

---

## TtkThemes2
*依赖`tksvg`库，有些主题是使用tksvg构建的，需要安装`tksvg`
```Bash
pip install tksvg
```

使用：

```Python
from ttkthemes2 import TtkThemes2
theme = TtkThemes2(theme_name=...)
```

简单示例

```Python
from tkinter import Tk, ttk, StringVar
from ttkthemes2 import TtkThemes2

root = Tk()

theme = TtkThemes2(theme_name="awdark")

window = ttk.Frame(root)

button = ttk.Button(window, text="TtkButton")
button.pack(padx=10, pady=10, fill="x")

window.pack(fill="both", expand="yes")

root.mainloop()
```

## Themed2Tk
简易包装`TtkThemes2`

*依赖`tksvg`库，有些主题是使用tksvg构建的，需要安装`tksvg`
```Bash
pip install tksvg
```

使用：

```Python
from ttkthemes2 import Themed2Tk
root = Themed2Tk(theme_name=...)
```

简单示例

```Python
from tkinter import Tk, ttk, StringVar
from ttkthemes2 import Themed2Tk

root = Themed2Tk(theme_name="awdark")

window = ttk.Frame(root)

button = ttk.Button(window, text="TtkButton")
button.pack(padx=10, pady=10, fill="x")

window.pack(fill="both", expand="yes")

root.mainloop()
```