"""
基础组件类 - 所有组件的基类
"""
from typing import Any, Dict, Optional, Callable
from ..core.style import Style


class Widget:
    """组件基类"""

    _widget_counter = 0

    def __init__(self, **kwargs):
        """初始化组件

        通用参数:
            id: 组件唯一标识
            style: 样式对象或样式字符串
            class_: 样式类名（多个用空格分隔）
            visible: 是否可见
            enabled: 是否可用
            tooltip: 提示文本
            width: 宽度
            height: 高度
            padding: 内边距
            margin: 外边距
            flex: 弹性系数
        """
        # 分配唯一 ID
        Widget._widget_counter += 1
        self._id = kwargs.get("id", f"widget_{Widget._widget_counter}")
        self._name = kwargs.get("name", self.__class__.__name__)

        # 样式
        style_input = kwargs.get("style", "")
        if isinstance(style_input, str):
            self.style = Style.from_string(style_input)
        elif isinstance(style_input, dict):
            self.style = Style.from_dict(style_input)
        elif isinstance(style_input, Style):
            self.style = style_input
        else:
            self.style = Style()

        # 样式类
        self.classes = []
        class_str = kwargs.get("class_", "")
        if class_str:
            self.classes = class_str.split()

        # 状态
        self.visible = kwargs.get("visible", True)
        self.enabled = kwargs.get("enabled", True)
        self.tooltip = kwargs.get("tooltip", "")

        # 尺寸
        self.width = kwargs.get("width", None)
        self.height = kwargs.get("height", None)
        self.padding = kwargs.get("padding", None)
        self.margin = kwargs.get("margin", None)
        self.flex = kwargs.get("flex", None)

        # 数据绑定
        self._bind_key = kwargs.get("bind", None)
        self._on_change = kwargs.get("on_change", None)
        self._on_input = kwargs.get("oninput", None) or kwargs.get("on_input", None)

        # 回调
        self._callbacks: Dict[str, Callable] = {}

        # 标记为组件
        self._is_widget = True

        # 原生组件引用
        self._native_widget = None
        self._parent = None

    @property
    def id(self) -> str:
        return self._id

    @property
    def value(self):
        """获取组件值"""
        return self._get_value()

    @value.setter
    def value(self, val):
        """设置组件值"""
        self._set_value(val)

    def _get_value(self):
        """子类重写：获取值"""
        return None

    def _set_value(self, val):
        """子类重写：设置值"""
        pass

    def set_value(self, val):
        """设置值（公共接口）"""
        self._set_value(val)

    def get_value(self):
        """获取值（公共接口）"""
        return self._get_value()

    def bind(self, key: str, app=None):
        """绑定到数据键"""
        self._bind_key = key
        if app and hasattr(app, "data"):
            app.data.bind(key, self._on_data_change)

    def _on_data_change(self, new_value, old_value):
        """数据变化回调"""
        self._set_value(new_value)

    def on(self, event: str, callback: Callable):
        """绑定事件"""
        self._callbacks[event] = callback

    def trigger(self, event: str, *args, **kwargs):
        """触发事件"""
        if event in self._callbacks:
            return self._callbacks[event](*args, **kwargs)

    def show(self):
        """显示组件"""
        self.visible = True
        if self._native_widget:
            self._native_widget.pack()

    def hide(self):
        """隐藏组件"""
        self.visible = False
        if self._native_widget:
            self._native_widget.pack_forget()

    def enable(self):
        """启用组件"""
        self.enabled = True
        if self._native_widget:
            self._native_widget.config(state="normal")

    def disable(self):
        """禁用组件"""
        self.enabled = False
        if self._native_widget:
            self._native_widget.config(state="disabled")

    def apply_style(self, style: Style):
        """应用样式"""
        self.style = self.style.merge(style)
        if self._native_widget:
            self._update_style()

    def _update_style(self):
        """子类重写：更新样式到原生组件"""
        pass

    def _apply_tk_style(self, widget):
        """应用样式到 Tkinter 组件"""
        tk_style = self.style.to_tk_style()

        for key, val in tk_style.items():
            try:
                widget.config(**{key: val})
            except:
                pass

        # 应用尺寸
        if self.width:
            try:
                widget.config(width=self._parse_size(self.width))
            except:
                pass

        if self.height:
            try:
                widget.config(height=self._parse_size(self.height))
            except:
                pass

    def _parse_size(self, size):
        """解析尺寸"""
        if isinstance(size, str):
            if size.endswith("px"):
                return int(size[:-2])
            elif size.isdigit():
                return int(size)
        return size

    def _resolve_color(self, color):
        """解析颜色"""
        return self.style._resolve_color(color)

    def render(self, backend="tkinter", parent=None, app=None):
        """渲染组件"""
        if backend == "tkinter":
            return self._render_tk(parent, app)
        return None

    def _render_tk(self, parent, app=None):
        """子类重写：Tkinter 渲染"""
        pass

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self._id})"
