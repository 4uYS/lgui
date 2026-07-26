"""
应用主类 - 窗口管理和应用生命周期
"""
import tkinter as tk
from tkinter import ttk
from typing import Any, List, Dict, Optional, Callable, Tuple
from .layout import Layout
from .style import Theme
from .bind import ReactiveDict
from .shorthand import parse_shorthand


class App:
    """lGUI 应用主类"""

    def __init__(self, title: str = "lGUI Application", 
                 size: Tuple[int, int] = (800, 600),
                 resizable: bool = True,
                 theme: str = "default",
                 backend: str = "tkinter"):
        """初始化应用

        Args:
            title: 窗口标题
            size: 窗口大小 (宽, 高)
            resizable: 是否可调整大小
            theme: 主题名称
            backend: 后端名称（目前仅支持 tkinter）
        """
        self.title = title
        self.size = size
        self.resizable = resizable
        self.backend_name = backend

        # 主题
        self.theme = Theme.get_preset(theme) or Theme.get_global()

        # 数据绑定
        self.data = ReactiveDict()
        self._bindings: Dict[str, Any] = {}

        # 布局
        self.layout = Layout()
        self._widget_map: Dict[str, Any] = {}  # id -> widget

        # 回调
        self._callbacks: Dict[str, Callable] = {}

        # Tkinter 后端
        self.root = None
        self._tk_widgets = []

        # 状态
        self._running = False

    def set_layout(self, definition: List):
        """设置布局定义

        Args:
            definition: 布局定义列表
        """
        self.layout.set_definition(definition)

        # 如果窗口已创建，重新渲染
        if self.root is not None:
            self._render_layout()

    def bind_data(self, data: Dict[str, Any]):
        """绑定数据源

        Args:
            data: 数据字典
        """
        for key, value in data.items():
            self.data[key] = value

    def get(self, widget_id: str):
        """获取组件实例

        Args:
            widget_id: 组件 ID

        Returns:
            组件对象或 None
        """
        return self._widget_map.get(widget_id)

    def update(self, widget_id: str, value: Any):
        """更新组件值

        Args:
            widget_id: 组件 ID
            value: 新值
        """
        widget = self._widget_map.get(widget_id)
        if widget and hasattr(widget, "set_value"):
            widget.set_value(value)

    def register_callback(self, name: str, callback: Callable):
        """注册回调函数

        Args:
            name: 回调名称
            callback: 回调函数
        """
        self._callbacks[name] = callback

    def _create_window(self):
        """创建 Tkinter 窗口"""
        self.root = tk.Tk()
        self.root.title(self.title)
        self.root.geometry(f"{self.size[0]}x{self.size[1]}")

        if not self.resizable:
            self.root.resizable(False, False)

        # 应用主题样式
        self._apply_theme()

        # 创建主容器
        self._main_frame = ttk.Frame(self.root)
        self._main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def _apply_theme(self):
        """应用主题到 Tkinter"""
        style = ttk.Style()

        # 获取主题颜色
        bg = self.theme.get_color("background", "#ffffff")
        surface = self.theme.get_color("surface", "#f8f9fa")
        text = self.theme.get_color("text", "#212529")
        primary = self.theme.get_color("primary", "#3498db")

        # 配置 ttk 样式
        style.configure("TFrame", background=bg)
        style.configure("TLabel", background=bg, foreground=text)
        style.configure("TButton", background=primary)
        style.configure("TEntry", fieldbackground=surface)
        style.configure("TCheckbutton", background=bg)
        style.configure("TRadiobutton", background=bg)
        style.configure("TCombobox", fieldbackground=surface)

        # 自定义样式
        style.configure("Card.TFrame", background=surface, relief="raised")
        style.configure("Primary.TButton", background=primary, foreground="white")
        style.configure("Danger.TButton", background="#e74c3c", foreground="white")
        style.configure("Success.TButton", background="#27ae60", foreground="white")

    def _render_layout(self):
        """渲染布局到窗口"""
        # 清空现有内容
        for widget in self._main_frame.winfo_children():
            widget.destroy()
        self._widget_map.clear()

        # 解析布局
        widgets = self.layout.parse()

        # 渲染每个组件
        for widget in widgets:
            self._render_widget(widget, self._main_frame)

    def _render_widget(self, widget, parent):
        """递归渲染组件"""
        if widget is None:
            return

        # 处理列表（多个组件）
        if isinstance(widget, list):
            for w in widget:
                self._render_widget(w, parent)
            return

        # 处理 ComponentInstance
        if hasattr(widget, "layout"):
            inner_layout = Layout(widget.layout)
            inner_layout.parse()
            for w in inner_layout.parse():
                self._render_widget(w, parent)
            return

        # 处理 For
        if hasattr(widget, "render") and widget.__class__.__name__ == "For":
            items = widget.render()
            for item in items:
                self._render_widget(item, parent)
            return

        # 处理 If
        if hasattr(widget, "render") and widget.__class__.__name__ == "If":
            items = widget.render()
            self._render_widget(items, parent)
            return

        # 渲染具体组件
        if hasattr(widget, "_render_tk"):
            widget._render_tk(parent, self)
        elif hasattr(widget, "render"):
            widget.render(backend="tkinter", parent=parent, app=self)

    def run(self):
        """运行应用"""
        self._create_window()
        self._render_layout()

        self._running = True
        self.root.mainloop()

    def quit(self):
        """退出应用"""
        if self.root:
            self.root.quit()
        self._running = False

    def __repr__(self):
        return f"App(title='{self.title}', size={self.size})"
