"""
样式系统 - 支持 CSS-like 样式、主题和动画
"""
import re
from typing import Dict, Any, Optional, Union, List, Tuple
from dataclasses import dataclass, field


@dataclass
class Style:
    """样式对象 - 类似 CSS 的样式定义"""

    # 颜色
    color: Optional[str] = None
    bg: Optional[str] = None
    background: Optional[str] = None

    # 字体
    font_family: Optional[str] = None
    font_size: Optional[str] = None
    font_weight: Optional[str] = None
    bold: Optional[bool] = None
    italic: Optional[bool] = None
    underline: Optional[bool] = None

    # 尺寸
    width: Optional[str] = None
    height: Optional[str] = None
    min_width: Optional[str] = None
    min_height: Optional[str] = None
    max_width: Optional[str] = None
    max_height: Optional[str] = None

    # 边距
    margin: Optional[str] = None
    margin_top: Optional[str] = None
    margin_bottom: Optional[str] = None
    margin_left: Optional[str] = None
    margin_right: Optional[str] = None

    # 内边距
    padding: Optional[str] = None
    padding_top: Optional[str] = None
    padding_bottom: Optional[str] = None
    padding_left: Optional[str] = None
    padding_right: Optional[str] = None

    # 边框
    border: Optional[str] = None
    border_top: Optional[str] = None
    border_bottom: Optional[str] = None
    border_left: Optional[str] = None
    border_right: Optional[str] = None
    border_radius: Optional[str] = None
    border_color: Optional[str] = None
    border_width: Optional[str] = None

    # 布局
    display: Optional[str] = None
    flex: Optional[Union[int, str]] = None
    flex_direction: Optional[str] = None
    justify_content: Optional[str] = None
    align_items: Optional[str] = None
    gap: Optional[str] = None

    # 阴影
    shadow: Optional[str] = None
    box_shadow: Optional[str] = None

    # 动画
    transition: Optional[str] = None
    hover: Optional[str] = None
    active: Optional[str] = None

    # 其他
    opacity: Optional[float] = None
    cursor: Optional[str] = None
    overflow: Optional[str] = None
    z_index: Optional[int] = None
    text_align: Optional[str] = None
    line_height: Optional[str] = None
    letter_spacing: Optional[str] = None
    text_transform: Optional[str] = None
    white_space: Optional[str] = None

    # 自定义属性
    custom: Dict[str, Any] = field(default_factory=dict)

    # 样式类
    classes: List[str] = field(default_factory=list)

    def __post_init__(self):
        """处理简写属性"""
        # bg 是 background 的简写
        if self.bg and not self.background:
            self.background = self.bg
        elif self.background and not self.bg:
            self.bg = self.background

    @classmethod
    def from_string(cls, style_str: str) -> "Style":
        """从样式字符串解析

        格式: "color=red,bg=blue,bold=True,width=100px"
        """
        if not style_str or not style_str.strip():
            return cls()

        kwargs = {}
        parts = [p.strip() for p in style_str.split(",")]

        for part in parts:
            if "=" in part:
                key, value = part.split("=", 1)
                key = key.strip()
                value = value.strip()

                # 转换布尔值
                if value.lower() == "true":
                    value = True
                elif value.lower() == "false":
                    value = False
                # 转换数字
                elif value.isdigit():
                    value = int(value)
                elif re.match(r"^-?\d+\.\d+$", value):
                    value = float(value)

                # 处理特殊键名映射
                key_mapping = {
                    "color": "color",
                    "bg": "bg",
                    "background": "background",
                    "size": "font_size",
                    "font-size": "font_size",
                    "font-size": "font_size",
                    "bold": "bold",
                    "italic": "italic",
                    "underline": "underline",
                    "width": "width",
                    "height": "height",
                    "margin": "margin",
                    "padding": "padding",
                    "border": "border",
                    "border-radius": "border_radius",
                    "border_radius": "border_radius",
                    "shadow": "shadow",
                    "transition": "transition",
                    "hover": "hover",
                    "active": "active",
                    "opacity": "opacity",
                    "cursor": "cursor",
                    "overflow": "overflow",
                    "z-index": "z_index",
                    "z_index": "z_index",
                    "text-align": "text_align",
                    "text_align": "text_align",
                    "line-height": "line_height",
                    "line_height": "line_height",
                    "gap": "gap",
                    "flex": "flex",
                    "display": "display",
                    "align": "align_items",
                    "justify": "justify_content",
                    "font-family": "font_family",
                    "font_family": "font_family",
                    "font-weight": "font_weight",
                    "font_weight": "font_weight",
                }

                mapped_key = key_mapping.get(key, key)
                kwargs[mapped_key] = value

        return cls(**kwargs)

    @classmethod
    def from_dict(cls, style_dict: Dict[str, Any]) -> "Style":
        """从字典创建样式"""
        return cls(**style_dict)

    def merge(self, other: "Style") -> "Style":
        """合并另一个样式（other 优先级更高）"""
        merged = Style()

        for field_name in self.__dataclass_fields__:
            self_val = getattr(self, field_name)
            other_val = getattr(other, field_name)

            if other_val is not None:
                setattr(merged, field_name, other_val)
            elif self_val is not None:
                setattr(merged, field_name, self_val)

        # 合并 custom
        merged.custom = {**self.custom, **other.custom}
        # 合并 classes
        merged.classes = list(set(self.classes + other.classes))

        return merged

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        result = {}
        for field_name in self.__dataclass_fields__:
            val = getattr(self, field_name)
            if val is not None and field_name not in ("custom", "classes"):
                result[field_name] = val

        if self.custom:
            result.update(self.custom)

        if self.classes:
            result["classes"] = self.classes

        return result

    def to_tk_style(self) -> Dict[str, Any]:
        """转换为 tkinter 样式字典"""
        tk_style = {}

        # 颜色映射
        if self.color:
            tk_style["fg"] = self._resolve_color(self.color)
        if self.background:
            tk_style["bg"] = self._resolve_color(self.background)

        # 字体
        font_parts = []
        if self.font_family:
            font_parts.append(self.font_family)
        if self.font_size:
            size = self.font_size.replace("px", "").replace("pt", "")
            font_parts.append(int(size))
        if self.bold:
            font_parts.append("bold")
        if self.italic:
            font_parts.append("italic")

        if font_parts:
            tk_style["font"] = tuple(font_parts)

        # 尺寸
        if self.width:
            tk_style["width"] = self._parse_size(self.width)
        if self.height:
            tk_style["height"] = self._parse_size(self.height)

        # 边框
        if self.border:
            tk_style["relief"] = self._parse_border_style(self.border)
        if self.border_width:
            tk_style["borderwidth"] = self._parse_size(self.border_width)

        # 光标
        if self.cursor:
            tk_style["cursor"] = self.cursor

        # 其他
        if self.text_align:
            tk_style["justify"] = self.text_align

        return tk_style

    def _resolve_color(self, color: str) -> str:
        """解析颜色值"""
        color_map = {
            "primary": "#3498db",
            "secondary": "#2ecc71",
            "danger": "#e74c3c",
            "warning": "#f39c12",
            "success": "#27ae60",
            "info": "#17a2b8",
            "light": "#f8f9fa",
            "dark": "#343a40",
            "white": "#ffffff",
            "black": "#000000",
            "gray": "#6c757d",
            "red": "#FF0000",
            "green": "#00FF00",
            "blue": "#0000FF",
            "yellow": "#FFFF00",
            "orange": "#FFA500",
            "purple": "#800080",
            "pink": "#FFC0CB",
            "cyan": "#00FFFF",
            "transparent": "transparent",
        }

        # 检查是否是主题颜色
        if color in color_map:
            return color_map[color]

        # 检查是否是十六进制
        if color.startswith("#"):
            return color

        # 检查是否是 rgb/rgba
        if color.startswith("rgb"):
            return color

        return color

    def _parse_size(self, size: str) -> Union[int, str]:
        """解析尺寸值"""
        if size.endswith("px"):
            return int(size[:-2])
        elif size.endswith("%"):
            return size
        elif size.isdigit():
            return int(size)
        return size

    def _parse_border_style(self, border: str) -> str:
        """解析边框样式"""
        if "solid" in border.lower():
            return "solid"
        elif "dashed" in border.lower():
            return "ridge"
        elif "dotted" in border.lower():
            return "groove"
        return "flat"

    def __repr__(self):
        attrs = [f"{k}={v}" for k, v in self.to_dict().items()]
        return f"Style({', '.join(attrs)})"


class Theme:
    """主题系统"""

    _global_theme = None
    _presets = {}

    def __init__(self, **kwargs):
        """创建主题

        支持的颜色键:
        - primary, secondary, danger, warning, success, info
        - background, surface, text, text_secondary
        - border, border_radius
        - font_family, font_size_base
        - shadow_sm, shadow_md, shadow_lg
        """
        self.colors = {}
        self.fonts = {}
        self.shadows = {}
        self.sizes = {}
        self.custom = {}

        # 颜色
        color_keys = [
            "primary", "secondary", "danger", "warning", 
            "success", "info", "light", "dark",
            "background", "surface", "text", "text_secondary",
            "border", "muted", "accent"
        ]

        for key in color_keys:
            if key in kwargs:
                self.colors[key] = kwargs.pop(key)

        # 字体
        font_keys = ["font_family", "font_size_base", "font_weight_base", "line_height_base"]
        for key in font_keys:
            if key in kwargs:
                self.fonts[key] = kwargs.pop(key)

        # 阴影
        shadow_keys = ["shadow_sm", "shadow_md", "shadow_lg", "shadow_xl"]
        for key in shadow_keys:
            if key in kwargs:
                self.shadows[key] = kwargs.pop(key)

        # 尺寸
        size_keys = ["border_radius", "border_radius_sm", "border_radius_lg", "spacing_unit"]
        for key in size_keys:
            if key in kwargs:
                self.sizes[key] = kwargs.pop(key)

        # 其他自定义
        self.custom = kwargs

    def get_color(self, name: str, fallback: str = "#000000") -> str:
        """获取主题颜色"""
        return self.colors.get(name, fallback)

    def get_font(self, name: str, fallback: str = None):
        """获取主题字体设置"""
        return self.fonts.get(name, fallback)

    def get_shadow(self, name: str, fallback: str = None):
        """获取主题阴影"""
        return self.shadows.get(name, fallback)

    def get_size(self, name: str, fallback: str = None):
        """获取主题尺寸"""
        return self.sizes.get(name, fallback)

    def apply_to_style(self, style: Style) -> Style:
        """将主题应用到样式"""
        new_style = Style()

        # 应用主题默认值
        if not style.font_family and self.fonts.get("font_family"):
            new_style.font_family = self.fonts["font_family"]

        if not style.font_size and self.fonts.get("font_size_base"):
            new_style.font_size = self.fonts["font_size_base"]

        if not style.border_radius and self.sizes.get("border_radius"):
            new_style.border_radius = self.sizes["border_radius"]

        # 解析颜色引用
        for attr in ["color", "bg", "background", "border_color"]:
            val = getattr(style, attr)
            if val and val in self.colors:
                setattr(new_style, attr, self.colors[val])

        return new_style.merge(style)

    @classmethod
    def set_global(cls, theme):
        """设置全局主题"""
        if isinstance(theme, str):
            theme = cls.get_preset(theme)
        cls._global_theme = theme

    @classmethod
    def get_global(cls):
        """获取全局主题"""
        if cls._global_theme is None:
            from ..themes.default import default_theme
            cls._global_theme = default_theme
        return cls._global_theme

    @classmethod
    def register_preset(cls, name: str, theme: "Theme"):
        """注册预设主题"""
        cls._presets[name] = theme

    @classmethod
    def get_preset(cls, name: str) -> "Theme":
        """获取预设主题"""
        if name not in cls._presets:
            # 延迟加载内置主题
            if name == "default":
                from ..themes.default import default_theme
                cls._presets[name] = default_theme
            elif name == "dark":
                from ..themes.dark import dark_theme
                cls._presets[name] = dark_theme

        return cls._presets.get(name)

    def __repr__(self):
        return f"Theme(colors={self.colors})"
