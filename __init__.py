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
    """简写组件访问器"""

    @staticmethod
    def B(text="", **kwargs):
        """Button 简写"""
        from .widgets.controls import Button
        return Button(text, **kwargs)

    @staticmethod
    def I(placeholder="", **kwargs):
        """Input 简写"""
        from .widgets.controls import Input
        return Input(placeholder=placeholder, **kwargs)

    @staticmethod
    def L(text="", **kwargs):
        """Label 简写"""
        from .widgets.controls import Label
        return Label(text, **kwargs)

    @staticmethod
    def C(text="", **kwargs):
        """Checkbox 简写"""
        from .widgets.controls import Checkbox
        return Checkbox(text, **kwargs)

    @staticmethod
    def R(options=None, **kwargs):
        """Radio 简写"""
        from .widgets.controls import Radio
        return Radio(options=options, **kwargs)

    @staticmethod
    def D(options=None, **kwargs):
        """Dropdown 简写"""
        from .widgets.controls import Dropdown
        return Dropdown(options=options, **kwargs)

    @staticmethod
    def S(**kwargs):
        """Slider 简写"""
        from .widgets.controls import Slider
        return Slider(**kwargs)

    @staticmethod
    def H(*children, **kwargs):
        """HBox 简写"""
        from .widgets.containers import HBox
        return HBox(list(children), **kwargs)

    @staticmethod
    def V(*children, **kwargs):
        """VBox 简写"""
        from .widgets.containers import VBox
        return VBox(list(children), **kwargs)

    @staticmethod
    def G(*children, **kwargs):
        """Grid 简写"""
        from .widgets.containers import Grid
        return Grid(list(children), **kwargs)

    @staticmethod
    def T(*tabs, **kwargs):
        """Tabs 简写"""
        from .widgets.containers import Tabs
        return Tabs(list(tabs), **kwargs)

    @staticmethod
    def F(*fields, **kwargs):
        """Form 简写"""
        from .widgets.containers import Form
        return Form(list(fields), **kwargs)

    @staticmethod
    def CARD(*children, **kwargs):
        """Card 简写"""
        from .widgets.containers import Card
        return Card(list(children), **kwargs)

    @staticmethod
    def IMG(src="", **kwargs):
        """Image 简写"""
        from .widgets.controls import Image
        return Image(src, **kwargs)

    @staticmethod
    def HR(**kwargs):
        """Divider 简写"""
        from .widgets.controls import Divider
        return Divider(**kwargs)

    @staticmethod
    def PROG(value=0, **kwargs):
        """Progress 简写"""
        from .widgets.controls import Progress
        return Progress(value, **kwargs)

    @staticmethod
    def DATE(**kwargs):
        """DatePicker 简写"""
        from .widgets.controls import DatePicker
        return DatePicker(**kwargs)

    @staticmethod
    def COLOR(**kwargs):
        """ColorPicker 简写"""
        from .widgets.controls import ColorPicker
        return ColorPicker(**kwargs)

# 创建单例实例供直接使用
B = _ShorthandWidgets.B
I = _ShorthandWidgets.I
L = _ShorthandWidgets.L
C = _ShorthandWidgets.C
R = _ShorthandWidgets.R
D = _ShorthandWidgets.D
S = _ShorthandWidgets.S
H = _ShorthandWidgets.H
V = _ShorthandWidgets.V
G = _ShorthandWidgets.G
T = _ShorthandWidgets.T
F = _ShorthandWidgets.F
CARD = _ShorthandWidgets.CARD
IMG = _ShorthandWidgets.IMG
HR = _ShorthandWidgets.HR
PROG = _ShorthandWidgets.PROG
DATE = _ShorthandWidgets.DATE
COLOR = _ShorthandWidgets.COLOR

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
