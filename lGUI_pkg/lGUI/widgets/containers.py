"""
容器组件 - 垂直/水平布局、网格、标签页、表单、卡片等
"""
import tkinter as tk
from tkinter import ttk
from typing import Any, List, Dict, Optional
from .base import Widget
from ..core.style import Style


class Container(Widget):
    """容器基类"""

    def __init__(self, children=None, **kwargs):
        super().__init__(**kwargs)
        self.children = children or []
        self._gap = kwargs.get("gap", None)
        self._padding = kwargs.get("padding", None)

    def add_child(self, child):
        """添加子组件"""
        self.children.append(child)

    def remove_child(self, child):
        """移除子组件"""
        if child in self.children:
            self.children.remove(child)

    def _render_children(self, container, app=None):
        """渲染子组件"""
        for child in self.children:
            if child is None:
                continue

            # 处理字符串
            if isinstance(child, str):
                from ..core.shorthand import parse_shorthand
                child = parse_shorthand(child)

            # 处理列表（嵌套布局）
            if isinstance(child, list):
                from ..core.shorthand import parse_shorthand
                child = parse_shorthand(child)

            # 渲染组件
            if hasattr(child, "_render_tk"):
                child._render_tk(container, app)
            elif hasattr(child, "render"):
                child.render(backend="tkinter", parent=container, app=app)
            elif isinstance(child, str):
                # 纯文本
                label = ttk.Label(container, text=child)
                label.pack(padx=2, pady=2)


class VBox(Container):
    """垂直布局容器"""

    def __init__(self, children=None, **kwargs):
        super().__init__(children, **kwargs)
        self._align = kwargs.get("align", None)  # left, center, right
        self._justify = kwargs.get("justify", None)  # start, center, end, space-between

    def _render_tk(self, parent, app=None):
        """Tkinter 渲染"""
        # 创建容器 Frame
        frame = ttk.Frame(parent)

        # 应用样式
        self._apply_tk_style(frame)

        # 设置背景色
        if self.style.background:
            frame.config(style="Custom.TFrame")
            style = ttk.Style()
            style.configure("Custom.TFrame", background=self._resolve_color(self.style.background))

        # 内边距
        padx, pady = self._parse_padding()

        # 渲染子组件
        for child in self.children:
            self._render_child(frame, child, app)

        # 布局
        if self.flex:
            frame.pack(fill=tk.BOTH, expand=True, padx=padx, pady=pady)
        else:
            frame.pack(fill=tk.X, padx=padx, pady=pady)

        self._native_widget = frame
        self._parent = parent

        if app:
            app._widget_map[self._id] = self

        return frame

    def _render_child(self, parent, child, app=None):
        """渲染单个子组件"""
        if child is None:
            return

        # 处理字符串
        if isinstance(child, str):
            from ..core.shorthand import parse_shorthand
            child = parse_shorthand(child)

        # 处理列表
        if isinstance(child, list):
            from ..core.shorthand import parse_shorthand
            child = parse_shorthand(child)

        # 渲染
        if hasattr(child, "_render_tk"):
            child._render_tk(parent, app)
        elif hasattr(child, "render"):
            child.render(backend="tkinter", parent=parent, app=app)
        elif isinstance(child, str):
            label = ttk.Label(parent, text=child)
            label.pack(fill=tk.X, padx=2, pady=2)

    def _parse_padding(self):
        """解析内边距"""
        if not self._padding:
            return 2, 2

        parts = str(self._padding).replace("px", "").split("_")
        if len(parts) == 1:
            return int(parts[0]), int(parts[0])
        elif len(parts) == 2:
            return int(parts[0]), int(parts[1])
        return 2, 2

    def __repr__(self):
        return f"VBox(children={len(self.children)}, id={self._id})"


class HBox(Container):
    """水平布局容器"""

    def __init__(self, children=None, **kwargs):
        super().__init__(children, **kwargs)
        self._align = kwargs.get("align", None)  # top, center, bottom, baseline
        self._justify = kwargs.get("justify", None)

    def _render_tk(self, parent, app=None):
        """Tkinter 渲染"""
        frame = ttk.Frame(parent)

        # 应用样式
        self._apply_tk_style(frame)

        # 设置背景色
        if self.style.background:
            frame.config(style="CustomH.TFrame")
            style = ttk.Style()
            style.configure("CustomH.TFrame", background=self._resolve_color(self.style.background))

        # 内边距
        padx, pady = self._parse_padding()

        # 渲染子组件
        for child in self.children:
            self._render_child(frame, child, app)

        # 布局
        if self.flex:
            frame.pack(fill=tk.BOTH, expand=True, padx=padx, pady=pady)
        else:
            frame.pack(fill=tk.X, padx=padx, pady=pady)

        self._native_widget = frame
        self._parent = parent

        if app:
            app._widget_map[self._id] = self

        return frame

    def _render_child(self, parent, child, app=None):
        """渲染单个子组件"""
        if child is None:
            return

        # 处理字符串
        if isinstance(child, str):
            from ..core.shorthand import parse_shorthand
            child = parse_shorthand(child)

        # 处理列表
        if isinstance(child, list):
            from ..core.shorthand import parse_shorthand
            child = parse_shorthand(child)

        # 渲染
        if hasattr(child, "_render_tk"):
            widget = child._render_tk(parent, app)
            # 水平布局的子组件需要特殊处理
            if widget and hasattr(widget, "pack"):
                widget.pack(side=tk.LEFT, padx=2, pady=2)
        elif hasattr(child, "render"):
            child.render(backend="tkinter", parent=parent, app=app)
        elif isinstance(child, str):
            label = ttk.Label(parent, text=child)
            label.pack(side=tk.LEFT, padx=2, pady=2)

    def _parse_padding(self):
        """解析内边距"""
        if not self._padding:
            return 2, 2

        parts = str(self._padding).replace("px", "").split("_")
        if len(parts) == 1:
            return int(parts[0]), int(parts[0])
        elif len(parts) == 2:
            return int(parts[0]), int(parts[1])
        return 2, 2

    def __repr__(self):
        return f"HBox(children={len(self.children)}, id={self._id})"


class Grid(Container):
    """网格布局容器"""

    def __init__(self, children=None, **kwargs):
        super().__init__(children, **kwargs)
        self._cols = kwargs.get("cols", 2)
        self._rows = kwargs.get("rows", None)
        self._gap = kwargs.get("gap", 5)

    def _render_tk(self, parent, app=None):
        """Tkinter 渲染"""
        frame = ttk.Frame(parent)

        # 应用样式
        self._apply_tk_style(frame)

        # 设置背景色
        if self.style.background:
            frame.config(style="CustomG.TFrame")
            style = ttk.Style()
            style.configure("CustomG.TFrame", background=self._resolve_color(self.style.background))

        # 渲染子组件到网格
        row, col = 0, 0
        for child in self.children:
            if child is None:
                col += 1
                if col >= self._cols:
                    col = 0
                    row += 1
                continue

            # 处理字符串
            if isinstance(child, str):
                from ..core.shorthand import parse_shorthand
                child = parse_shorthand(child)

            # 处理列表
            if isinstance(child, list):
                from ..core.shorthand import parse_shorthand
                child = parse_shorthand(child)

            # 渲染
            cell_frame = ttk.Frame(frame)
            cell_frame.grid(row=row, column=col, padx=self._gap//2, pady=self._gap//2, sticky="nsew")

            if hasattr(child, "_render_tk"):
                widget = child._render_tk(cell_frame, app)
                if widget and hasattr(widget, "pack"):
                    widget.pack(fill=tk.BOTH, expand=True)
            elif hasattr(child, "render"):
                child.render(backend="tkinter", parent=cell_frame, app=app)
            elif isinstance(child, str):
                label = ttk.Label(cell_frame, text=child)
                label.pack(fill=tk.BOTH, expand=True)

            col += 1
            if col >= self._cols:
                col = 0
                row += 1

        # 配置列权重
        for c in range(self._cols):
            frame.columnconfigure(c, weight=1)

        # 布局
        if self.flex:
            frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        else:
            frame.pack(fill=tk.X, padx=5, pady=5)

        self._native_widget = frame
        self._parent = parent

        if app:
            app._widget_map[self._id] = self

        return frame

    def __repr__(self):
        return f"Grid(cols={self._cols}, children={len(self.children)}, id={self._id})"


class Tabs(Container):
    """标签页容器"""

    def __init__(self, tabs=None, **kwargs):
        super().__init__(tabs or [], **kwargs)
        self._tab_position = kwargs.get("tab_position", "top")  # top, bottom, left, right

    def _render_tk(self, parent, app=None):
        """Tkinter 渲染"""
        notebook = ttk.Notebook(parent)

        # 应用样式
        self._apply_tk_style(notebook)

        # 渲染每个标签页
        for tab_def in self.children:
            if not isinstance(tab_def, list) or len(tab_def) < 2:
                continue

            tab_name = tab_def[0]
            tab_content = tab_def[1:]

            # 创建标签页 Frame
            tab_frame = ttk.Frame(notebook)

            # 渲染内容
            for child in tab_content:
                self._render_tab_child(tab_frame, child, app)

            # 添加标签页
            notebook.add(tab_frame, text=tab_name)

        # 布局
        if self.flex:
            notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        else:
            notebook.pack(fill=tk.X, padx=5, pady=5)

        self._native_widget = notebook
        self._parent = parent

        if app:
            app._widget_map[self._id] = self

        return notebook

    def _render_tab_child(self, parent, child, app=None):
        """渲染标签页内的子组件"""
        if child is None:
            return

        if isinstance(child, str):
            from ..core.shorthand import parse_shorthand
            child = parse_shorthand(child)

        if isinstance(child, list):
            from ..core.shorthand import parse_shorthand
            child = parse_shorthand(child)

        if hasattr(child, "_render_tk"):
            child._render_tk(parent, app)
        elif hasattr(child, "render"):
            child.render(backend="tkinter", parent=parent, app=app)
        elif isinstance(child, str):
            label = ttk.Label(parent, text=child)
            label.pack(fill=tk.X, padx=2, pady=2)

    def __repr__(self):
        return f"Tabs(tabs={len(self.children)}, id={self._id})"


class Form(Container):
    """表单容器"""

    def __init__(self, fields=None, **kwargs):
        super().__init__(fields or [], **kwargs)
        self._label_width = kwargs.get("label_width", 80)

    def _render_tk(self, parent, app=None):
        """Tkinter 渲染"""
        frame = ttk.Frame(parent)

        # 应用样式
        self._apply_tk_style(frame)

        # 渲染每个字段
        for field_def in self.children:
            if not isinstance(field_def, list) or len(field_def) < 2:
                continue

            label_text = field_def[0]
            field_widget = field_def[1]

            # 创建行
            row_frame = ttk.Frame(frame)
            row_frame.pack(fill=tk.X, pady=3)

            # 标签
            if label_text:
                label = ttk.Label(row_frame, text=label_text, width=self._label_width // 8)
                label.pack(side=tk.LEFT, padx=(0, 10))

            # 字段组件
            if isinstance(field_widget, str):
                from ..core.shorthand import parse_shorthand
                field_widget = parse_shorthand(field_widget)

            if hasattr(field_widget, "_render_tk"):
                widget = field_widget._render_tk(row_frame, app)
                if widget and hasattr(widget, "pack"):
                    widget.pack(side=tk.LEFT, fill=tk.X, expand=True)
            elif hasattr(field_widget, "render"):
                field_widget.render(backend="tkinter", parent=row_frame, app=app)
            elif isinstance(field_widget, str):
                label = ttk.Label(row_frame, text=field_widget)
                label.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # 布局
        if self.flex:
            frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        else:
            frame.pack(fill=tk.X, padx=10, pady=10)

        self._native_widget = frame
        self._parent = parent

        if app:
            app._widget_map[self._id] = self

        return frame

    def __repr__(self):
        return f"Form(fields={len(self.children)}, id={self._id})"


class Card(Container):
    """卡片容器"""

    def __init__(self, children=None, **kwargs):
        super().__init__(children, **kwargs)
        self._title = kwargs.get("title", None)
        self._shadow = kwargs.get("shadow", False)
        self._border = kwargs.get("border", True)

    def _render_tk(self, parent, app=None):
        """Tkinter 渲染"""
        # 使用 LabelFrame 或 Frame + Label 实现卡片效果
        if self._title:
            frame = ttk.LabelFrame(parent, text=self._title)
        else:
            frame = ttk.Frame(parent)

        # 应用样式
        self._apply_tk_style(frame)

        # 设置背景色和边框
        if self.style.background:
            bg_color = self._resolve_color(self.style.background)
            frame.config(style="Card.TFrame")
            style = ttk.Style()
            style.configure("Card.TFrame", background=bg_color)
            if self._title:
                style.configure("Card.TLabelframe", background=bg_color)
                style.configure("Card.TLabelframe.Label", background=bg_color)

        # 内边距
        padx, pady = self._parse_padding()

        # 渲染子组件
        for child in self.children:
            self._render_child(frame, child, app)

        # 布局
        if self.flex:
            frame.pack(fill=tk.BOTH, expand=True, padx=padx, pady=pady)
        else:
            frame.pack(fill=tk.X, padx=padx, pady=pady)

        self._native_widget = frame
        self._parent = parent

        if app:
            app._widget_map[self._id] = self

        return frame

    def _render_child(self, parent, child, app=None):
        """渲染单个子组件"""
        if child is None:
            return

        if isinstance(child, str):
            from ..core.shorthand import parse_shorthand
            child = parse_shorthand(child)

        if isinstance(child, list):
            from ..core.shorthand import parse_shorthand
            child = parse_shorthand(child)

        if hasattr(child, "_render_tk"):
            child._render_tk(parent, app)
        elif hasattr(child, "render"):
            child.render(backend="tkinter", parent=parent, app=app)
        elif isinstance(child, str):
            label = ttk.Label(parent, text=child)
            label.pack(fill=tk.X, padx=2, pady=2)

    def _parse_padding(self):
        """解析内边距"""
        if not self._padding:
            return 10, 10

        parts = str(self._padding).replace("px", "").split("_")
        if len(parts) == 1:
            return int(parts[0]), int(parts[0])
        elif len(parts) == 2:
            return int(parts[0]), int(parts[1])
        return 10, 10

    def __repr__(self):
        return f"Card(title={self._title}, children={len(self.children)}, id={self._id})"
