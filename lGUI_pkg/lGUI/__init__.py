"""
lGUI - 轻量级声明式 GUI 库
Lightweight Declarative GUI Library

支持简写语法、主题系统、数据绑定和多后端
"""

__version__ = "0.1.0"
__author__ = "lGUI Team"

# 核心类
from .core.app import App
from .core.layout import Layout
from .core.style import Style, Theme
from .core.bind import bind, reactive
from .core.shorthand import parse_shorthand

# 主题
from .themes.default import default_theme
from .themes.dark import dark_theme

# 便捷函数
from .core.utils import component, For, If

# 设置全局主题
def set_theme(theme_name_or_obj):
    """设置全局主题

    Args:
        theme_name_or_obj: 主题名称字符串或 Theme 对象
    """
    from .core.style import Theme
    Theme.set_global(theme_name_or_obj)

def get_theme():
    """获取当前全局主题"""
    from .core.style import Theme
    return Theme.get_global()

# 简写组件快捷导入
class _ShorthandWidgets:
    """简写组件访问器 - 延迟导入避免循环依赖"""
    pass

def _make_shorthand(widget_type):
    """动态创建简写函数"""
    def shorthand(*args, **kwargs):
        from .core.shorthand import ShorthandParser
        if widget_type == "B":
            from .widgets.controls import Button
            text = args[0] if args else kwargs.pop("text", "")
            return Button(text, **kwargs)
        elif widget_type == "I":
            from .widgets.controls import Input
            placeholder = args[0] if args else kwargs.pop("placeholder", "")
            return Input(placeholder=placeholder, **kwargs)
        elif widget_type == "L":
            from .widgets.controls import Label
            text = args[0] if args else kwargs.pop("text", "")
            return Label(text, **kwargs)
        elif widget_type == "C":
            from .widgets.controls import Checkbox
            text = args[0] if args else kwargs.pop("text", "")
            return Checkbox(text, **kwargs)
        elif widget_type == "R":
            from .widgets.controls import Radio
            return Radio(*args, **kwargs)
        elif widget_type == "D":
            from .widgets.controls import Dropdown
            return Dropdown(*args, **kwargs)
        elif widget_type == "S":
            from .widgets.controls import Slider
            return Slider(**kwargs)
        elif widget_type == "H":
            from .widgets.containers import HBox
            return HBox(list(args) if args else kwargs.pop("children", []), **kwargs)
        elif widget_type == "V":
            from .widgets.containers import VBox
            return VBox(list(args) if args else kwargs.pop("children", []), **kwargs)
        elif widget_type == "G":
            from .widgets.containers import Grid
            return Grid(list(args) if args else kwargs.pop("children", []), **kwargs)
        elif widget_type == "T":
            from .widgets.containers import Tabs
            return Tabs(list(args) if args else kwargs.pop("children", []), **kwargs)
        elif widget_type == "F":
            from .widgets.containers import Form
            return Form(list(args) if args else kwargs.pop("children", []), **kwargs)
        elif widget_type == "CARD":
            from .widgets.containers import Card
            return Card(list(args) if args else kwargs.pop("children", []), **kwargs)
        elif widget_type == "IMG":
            from .widgets.controls import Image
            src = args[0] if args else kwargs.pop("src", "")
            return Image(src, **kwargs)
        elif widget_type == "HR":
            from .widgets.controls import Divider
            return Divider(**kwargs)
        elif widget_type == "PROG":
            from .widgets.controls import Progress
            value = args[0] if args else kwargs.pop("value", 0)
            return Progress(value, **kwargs)
        elif widget_type == "DATE":
            from .widgets.controls import DatePicker
            return DatePicker(**kwargs)
        elif widget_type == "COLOR":
            from .widgets.controls import ColorPicker
            return ColorPicker(**kwargs)
        return None
    return shorthand

# 创建简写函数
B = _make_shorthand("B")
I = _make_shorthand("I")
L = _make_shorthand("L")
C = _make_shorthand("C")
R = _make_shorthand("R")
D = _make_shorthand("D")
S = _make_shorthand("S")
H = _make_shorthand("H")
V = _make_shorthand("V")
G = _make_shorthand("G")
T = _make_shorthand("T")
F = _make_shorthand("F")
CARD = _make_shorthand("CARD")
IMG = _make_shorthand("IMG")
HR = _make_shorthand("HR")
PROG = _make_shorthand("PROG")
DATE = _make_shorthand("DATE")
COLOR = _make_shorthand("COLOR")

# 导出所有公共 API
__all__ = [
    # 核心
    "App",
    "Layout", 
    "Style",
    "Theme",
    "bind",
    "reactive",
    "parse_shorthand",
    "component",
    "For",
    "If",

    # 主题
    "default_theme",
    "dark_theme",
    "set_theme",
    "get_theme",

    # 简写组件
    "B", "I", "L", "C", "R", "D", "S",
    "H", "V", "G", "T", "F", "CARD",
    "IMG", "HR", "PROG", "DATE", "COLOR",
]
