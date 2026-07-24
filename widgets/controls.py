"""
交互控件 - 按钮、输入框、标签、复选框等
"""
import tkinter as tk
from tkinter import ttk
from typing import Any, Optional, Callable, List
from .base import Widget
from ..core.style import Style


class Button(Widget):
    """按钮组件"""

    def __init__(self, text="", **kwargs):
        super().__init__(**kwargs)
        self.text = text
        self._on_click = kwargs.get("onclick", None) or kwargs.get("on_click", None)
        self._command = kwargs.get("command", None)

        # 图标
        self.icon = kwargs.get("icon", None)

        # 按钮类型
        self.variant = kwargs.get("variant", "default")  # default, primary, danger, success, ghost

    def _get_value(self):
        return self.text

    def _set_value(self, val):
        self.text = str(val)
        if self._native_widget:
            self._native_widget.config(text=self.text)

    def _render_tk(self, parent, app=None):
        """Tkinter 渲染"""
        # 确定样式
        style_name = "TButton"
        if self.variant == "primary":
            style_name = "Primary.TButton"
        elif self.variant == "danger":
            style_name = "Danger.TButton"
        elif self.variant == "success":
            style_name = "Success.TButton"
        elif self.variant == "ghost":
            style_name = "TButton"

        # 创建按钮
        btn = ttk.Button(parent, text=self.text, style=style_name)

        # 应用样式
        self._apply_tk_style(btn)

        # 绑定点击事件
        def on_click():
            if self._on_click:
                if callable(self._on_click):
                    self._on_click()
                elif app and self._on_click in app._callbacks:
                    app._callbacks[self._on_click]()
                elif isinstance(self._on_click, str) and app:
                    # 尝试从 app 回调中查找
                    cb = app._callbacks.get(self._on_click)
                    if cb:
                        cb()

            if self._command:
                self._command()

            self.trigger("click")

        btn.config(command=on_click)

        # 布局
        self._pack_widget(btn)

        self._native_widget = btn
        self._parent = parent

        # 注册到 app
        if app:
            app._widget_map[self._id] = self

        return btn

    def _pack_widget(self, widget):
        """智能布局"""
        # 检查是否有 flex 属性
        if self.flex:
            widget.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        else:
            widget.pack(padx=2, pady=2)

    def __repr__(self):
        return f"Button('{self.text}', id={self._id})"


class Input(Widget):
    """输入框组件"""

    def __init__(self, placeholder="", **kwargs):
        super().__init__(**kwargs)
        self.placeholder = placeholder
        self._value = kwargs.get("value", "")
        self._password = kwargs.get("password", False)
        self._type = kwargs.get("type", "text")  # text, int, float, password

        # 事件
        self._on_enter = kwargs.get("on_enter", None)

    def _get_value(self):
        if self._native_widget:
            return self._native_widget.get()
        return self._value

    def _set_value(self, val):
        self._value = str(val)
        if self._native_widget:
            self._native_widget.delete(0, tk.END)
            self._native_widget.insert(0, self._value)

    def _render_tk(self, parent, app=None):
        """Tkinter 渲染"""
        # 创建输入框
        show_char = "*" if self._password or self._type == "password" else ""

        entry = ttk.Entry(parent, show=show_char)

        # 设置初始值
        if self._value:
            entry.insert(0, str(self._value))

        # 应用样式
        self._apply_tk_style(entry)

        # 占位符处理
        if self.placeholder and not self._value:
            entry.insert(0, self.placeholder)
            entry.config(foreground="gray")

            def on_focus_in(event):
                if entry.get() == self.placeholder:
                    entry.delete(0, tk.END)
                    entry.config(foreground="black")

            def on_focus_out(event):
                if not entry.get():
                    entry.insert(0, self.placeholder)
                    entry.config(foreground="gray")

            entry.bind("<FocusIn>", on_focus_in)
            entry.bind("<FocusOut>", on_focus_out)

        # 绑定输入事件
        def on_input(event):
            val = entry.get()
            self._value = val

            if self._on_input:
                if callable(self._on_input):
                    self._on_input(val)
                elif app and self._on_input in app._callbacks:
                    app._callbacks[self._on_input](val)

            self.trigger("input", val)

            # 数据绑定更新
            if self._bind_key and app:
                app.data[self._bind_key] = val

        entry.bind("<KeyRelease>", on_input)

        # 回车事件
        def on_enter(event):
            if self._on_enter:
                if callable(self._on_enter):
                    self._on_enter(entry.get())
                elif app and self._on_enter in app._callbacks:
                    app._callbacks[self._on_enter](entry.get())
            self.trigger("enter", entry.get())

        entry.bind("<Return>", on_enter)

        # 布局
        self._pack_widget(entry)

        self._native_widget = entry
        self._parent = parent

        if app:
            app._widget_map[self._id] = self

        return entry

    def _pack_widget(self, widget):
        widget.pack(fill=tk.X, padx=2, pady=2)

    def __repr__(self):
        return f"Input(placeholder='{self.placeholder}', id={self._id})"


class Label(Widget):
    """标签组件"""

    def __init__(self, text="", **kwargs):
        super().__init__(**kwargs)
        self.text = text
        self._raw_text = text

    def _get_value(self):
        return self.text

    def _set_value(self, val):
        self.text = str(val)
        if self._native_widget:
            self._native_widget.config(text=self.text)

    def _render_tk(self, parent, app=None):
        """Tkinter 渲染"""
        # 处理样式
        tk_style = self.style.to_tk_style()

        # 处理粗体
        if self.style.bold:
            font = tk_style.get("font", ("TkDefaultFont",))
            if isinstance(font, tuple):
                font = list(font)
                if "bold" not in font:
                    font.append("bold")
                tk_style["font"] = tuple(font)

        # 处理斜体
        if self.style.italic:
            font = tk_style.get("font", ("TkDefaultFont",))
            if isinstance(font, tuple):
                font = list(font)
                if "italic" not in font:
                    font.append("italic")
                tk_style["font"] = tuple(font)

        label = ttk.Label(parent, text=self.text, **tk_style)

        # 应用尺寸
        self._apply_tk_style(label)

        # 布局
        self._pack_widget(label)

        self._native_widget = label
        self._parent = parent

        if app:
            app._widget_map[self._id] = self

        return label

    def _pack_widget(self, widget):
        if self.style.text_align == "center":
            widget.pack(anchor=tk.CENTER, padx=2, pady=2)
        elif self.style.text_align == "right":
            widget.pack(anchor=tk.E, padx=2, pady=2)
        else:
            widget.pack(anchor=tk.W, padx=2, pady=2)

    def __repr__(self):
        return f"Label('{self.text}', id={self._id})"


class Checkbox(Widget):
    """复选框组件"""

    def __init__(self, text="", **kwargs):
        super().__init__(**kwargs)
        self.text = text
        self._checked = kwargs.get("checked", False)
        self._value = kwargs.get("value", None)
        self._on_change = kwargs.get("on_change", None)

    def _get_value(self):
        return self._checked

    def _set_value(self, val):
        self._checked = bool(val)
        if self._native_widget:
            self._var.set(self._checked)

    def _render_tk(self, parent, app=None):
        """Tkinter 渲染"""
        self._var = tk.BooleanVar(value=self._checked)

        cb = ttk.Checkbutton(parent, text=self.text, variable=self._var)

        # 应用样式
        self._apply_tk_style(cb)

        # 绑定变化事件
        def on_change():
            self._checked = self._var.get()

            if self._on_change:
                if callable(self._on_change):
                    self._on_change(self._checked)
                elif app and self._on_change in app._callbacks:
                    app._callbacks[self._on_change](self._checked)

            self.trigger("change", self._checked)

            # 数据绑定
            if self._bind_key and app:
                app.data[self._bind_key] = self._checked

        cb.config(command=on_change)

        # 布局
        self._pack_widget(cb)

        self._native_widget = cb
        self._parent = parent

        if app:
            app._widget_map[self._id] = self

        return cb

    def _pack_widget(self, widget):
        widget.pack(anchor=tk.W, padx=2, pady=2)

    def __repr__(self):
        return f"Checkbox('{self.text}', checked={self._checked}, id={self._id})"


class Radio(Widget):
    """单选框组件"""

    def __init__(self, options=None, **kwargs):
        super().__init__(**kwargs)
        self.options = options or []
        self._selected = kwargs.get("selected", None)
        self._on_change = kwargs.get("on_change", None)

    def _get_value(self):
        return self._selected

    def _set_value(self, val):
        self._selected = val
        if self._native_widget:
            self._var.set(val)

    def _render_tk(self, parent, app=None):
        """Tkinter 渲染"""
        self._var = tk.StringVar(value=self._selected or "")

        # 创建容器
        frame = ttk.Frame(parent)

        for option in self.options:
            rb = ttk.Radiobutton(
                frame, 
                text=option, 
                variable=self._var, 
                value=option
            )
            rb.pack(anchor=tk.W, padx=5, pady=2)

            # 绑定变化
            def make_handler(opt):
                def handler():
                    self._selected = opt
                    if self._on_change:
                        if callable(self._on_change):
                            self._on_change(opt)
                        elif app and self._on_change in app._callbacks:
                            app._callbacks[self._on_change](opt)
                    self.trigger("change", opt)
                    if self._bind_key and app:
                        app.data[self._bind_key] = opt
                return handler

            rb.config(command=make_handler(option))

        # 应用样式
        self._apply_tk_style(frame)

        # 布局
        self._pack_widget(frame)

        self._native_widget = frame
        self._parent = parent

        if app:
            app._widget_map[self._id] = self

        return frame

    def _pack_widget(self, widget):
        widget.pack(fill=tk.X, padx=2, pady=2)

    def __repr__(self):
        return f"Radio(options={self.options}, selected={self._selected}, id={self._id})"


class Dropdown(Widget):
    """下拉框组件"""

    def __init__(self, options=None, **kwargs):
        super().__init__(**kwargs)
        self.options = options or []
        self._selected = kwargs.get("value", kwargs.get("selected", None))
        self._on_change = kwargs.get("on_change", None)

    def _get_value(self):
        if self._native_widget:
            return self._var.get()
        return self._selected

    def _set_value(self, val):
        self._selected = val
        if self._native_widget:
            self._var.set(val)

    def _render_tk(self, parent, app=None):
        """Tkinter 渲染"""
        self._var = tk.StringVar(value=self._selected or "")

        combo = ttk.Combobox(parent, textvariable=self._var, values=self.options)

        # 应用样式
        self._apply_tk_style(combo)

        # 绑定变化
        def on_change(event):
            val = self._var.get()
            self._selected = val

            if self._on_change:
                if callable(self._on_change):
                    self._on_change(val)
                elif app and self._on_change in app._callbacks:
                    app._callbacks[self._on_change](val)

            self.trigger("change", val)

            if self._bind_key and app:
                app.data[self._bind_key] = val

        combo.bind("<<ComboboxSelected>>", on_change)

        # 布局
        self._pack_widget(combo)

        self._native_widget = combo
        self._parent = parent

        if app:
            app._widget_map[self._id] = self

        return combo

    def _pack_widget(self, widget):
        widget.pack(fill=tk.X, padx=2, pady=2)

    def __repr__(self):
        return f"Dropdown(options={self.options}, value={self._selected}, id={self._id})"


class Slider(Widget):
    """滑块组件"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._min = kwargs.get("min", 0)
        self._max = kwargs.get("max", 100)
        self._value = kwargs.get("value", self._min)
        self._step = kwargs.get("step", 1)
        self._on_change = kwargs.get("on_change", None)

    def _get_value(self):
        if self._native_widget:
            return self._var.get()
        return self._value

    def _set_value(self, val):
        self._value = val
        if self._native_widget:
            self._var.set(val)

    def _render_tk(self, parent, app=None):
        """Tkinter 渲染"""
        self._var = tk.DoubleVar(value=self._value)

        scale = ttk.Scale(
            parent,
            from_=self._min,
            to=self._max,
            variable=self._var,
            orient=tk.HORIZONTAL
        )

        # 应用样式
        self._apply_tk_style(scale)

        # 绑定变化
        def on_change(event):
            val = self._var.get()
            self._value = val

            if self._on_change:
                if callable(self._on_change):
                    self._on_change(val)
                elif app and self._on_change in app._callbacks:
                    app._callbacks[self._on_change](val)

            self.trigger("change", val)

            if self._bind_key and app:
                app.data[self._bind_key] = val

        scale.bind("<ButtonRelease-1>", on_change)

        # 布局
        self._pack_widget(scale)

        self._native_widget = scale
        self._parent = parent

        if app:
            app._widget_map[self._id] = self

        return scale

    def _pack_widget(self, widget):
        widget.pack(fill=tk.X, padx=2, pady=2)

    def __repr__(self):
        return f"Slider(min={self._min}, max={self._max}, value={self._value}, id={self._id})"


class Image(Widget):
    """图片组件"""

    def __init__(self, src="", **kwargs):
        super().__init__(**kwargs)
        self.src = src
        self._width = kwargs.get("width", None)
        self._height = kwargs.get("height", None)

    def _get_value(self):
        return self.src

    def _set_value(self, val):
        self.src = val
        if self._native_widget:
            self._load_image()

    def _load_image(self):
        """加载图片"""
        try:
            from PIL import Image as PILImage
            from PIL import ImageTk

            img = PILImage.open(self.src)

            if self._width or self._height:
                w = self._width or img.width
                h = self._height or img.height
                img = img.resize((w, h))

            self._tk_image = ImageTk.PhotoImage(img)
            self._native_widget.config(image=self._tk_image)
        except Exception as e:
            # 加载失败显示文本
            self._native_widget.config(text=f"[Image: {self.src}]")

    def _render_tk(self, parent, app=None):
        """Tkinter 渲染"""
        label = ttk.Label(parent)

        # 应用样式
        self._apply_tk_style(label)

        # 尝试加载图片
        self._native_widget = label
        self._load_image()

        # 布局
        self._pack_widget(label)

        self._parent = parent

        if app:
            app._widget_map[self._id] = self

        return label

    def _pack_widget(self, widget):
        widget.pack(padx=2, pady=2)

    def __repr__(self):
        return f"Image(src='{self.src}', id={self._id})"


class Divider(Widget):
    """分割线组件"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._style = kwargs.get("style", "solid")  # solid, dashed, dotted

    def _render_tk(self, parent, app=None):
        """Tkinter 渲染"""
        # 使用 Frame 模拟分割线
        frame = tk.Frame(parent, height=2, bg="#cccccc")

        # 应用样式
        if self.style.bg or self.style.background:
            color = self.style.bg or self.style.background
            frame.config(bg=self._resolve_color(color))

        # 布局
        frame.pack(fill=tk.X, padx=5, pady=10)

        self._native_widget = frame
        self._parent = parent

        if app:
            app._widget_map[self._id] = self

        return frame

    def __repr__(self):
        return f"Divider(id={self._id})"


class Progress(Widget):
    """进度条组件"""

    def __init__(self, value=0, **kwargs):
        super().__init__(**kwargs)
        self._value = float(value)
        self._max = kwargs.get("max", 100)
        self._show_percent = kwargs.get("show_percent", False)

    def _get_value(self):
        return self._value

    def _set_value(self, val):
        self._value = float(val)
        if self._native_widget:
            self._var.set(self._value)

    def _render_tk(self, parent, app=None):
        """Tkinter 渲染"""
        self._var = tk.DoubleVar(value=self._value)

        # 创建容器
        frame = ttk.Frame(parent)

        # 进度条
        progress = ttk.Progressbar(
            frame,
            variable=self._var,
            maximum=self._max,
            mode="determinate"
        )
        progress.pack(fill=tk.X, expand=True)

        # 百分比标签
        if self._show_percent:
            percent = ttk.Label(frame, text=f"{self._value:.0f}%")
            percent.pack()
            self._percent_label = percent

        # 应用样式
        self._apply_tk_style(frame)

        # 布局
        frame.pack(fill=tk.X, padx=2, pady=2)

        self._native_widget = progress
        self._parent = parent

        if app:
            app._widget_map[self._id] = self

        return frame

    def __repr__(self):
        return f"Progress(value={self._value}, id={self._id})"


class DatePicker(Widget):
    """日期选择器组件"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._value = kwargs.get("value", "")
        self._format = kwargs.get("format", "YYYY-MM-DD")

    def _get_value(self):
        if self._native_widget:
            return self._entry.get()
        return self._value

    def _set_value(self, val):
        self._value = val
        if self._native_widget:
            self._entry.delete(0, tk.END)
            self._entry.insert(0, val)

    def _render_tk(self, parent, app=None):
        """Tkinter 渲染 - 使用简单输入框模拟"""
        frame = ttk.Frame(parent)

        # 输入框
        self._entry = ttk.Entry(frame)
        if self._value:
            self._entry.insert(0, self._value)
        self._entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # 日期按钮
        btn = ttk.Button(frame, text="📅", width=3)
        btn.pack(side=tk.LEFT, padx=2)

        # 应用样式
        self._apply_tk_style(frame)

        # 布局
        frame.pack(fill=tk.X, padx=2, pady=2)

        self._native_widget = frame
        self._parent = parent

        if app:
            app._widget_map[self._id] = self

        return frame

    def __repr__(self):
        return f"DatePicker(value='{self._value}', id={self._id})"


class ColorPicker(Widget):
    """颜色选择器组件"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._value = kwargs.get("value", "#000000")

    def _get_value(self):
        return self._value

    def _set_value(self, val):
        self._value = val
        if self._native_widget:
            self._canvas.config(bg=val)

    def _render_tk(self, parent, app=None):
        """Tkinter 渲染"""
        frame = ttk.Frame(parent)

        # 颜色预览
        self._canvas = tk.Canvas(frame, width=30, height=20, bg=self._value, highlightthickness=1, highlightbackground="#ccc")
        self._canvas.pack(side=tk.LEFT)

        # 输入框
        self._entry = ttk.Entry(frame, width=10)
        self._entry.insert(0, self._value)
        self._entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        # 选择按钮
        def pick_color():
            from tkinter import colorchooser
            color = colorchooser.askcolor(initialcolor=self._value)
            if color[1]:
                self._value = color[1]
                self._canvas.config(bg=self._value)
                self._entry.delete(0, tk.END)
                self._entry.insert(0, self._value)
                self.trigger("change", self._value)

        btn = ttk.Button(frame, text="选择", command=pick_color)
        btn.pack(side=tk.LEFT, padx=2)

        # 应用样式
        self._apply_tk_style(frame)

        # 布局
        frame.pack(fill=tk.X, padx=2, pady=2)

        self._native_widget = frame
        self._parent = parent

        if app:
            app._widget_map[self._id] = self

        return frame

    def __repr__(self):
        return f"ColorPicker(value='{self._value}', id={self._id})"
