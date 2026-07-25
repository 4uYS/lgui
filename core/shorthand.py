
"""
简写解析器 - 将字符串/元组简写解析为组件对象
"""
import re
from typing import Any, Dict, List, Union, Optional, Tuple


class ShorthandParser:
    """简写语法解析器"""

    # 组件类型映射
    TYPE_MAP = {
        "B": "Button",
        "I": "Input", 
        "L": "Label",
        "C": "Checkbox",
        "R": "Radio",
        "D": "Dropdown",
        "S": "Slider",
        "H": "HBox",
        "V": "VBox",
        "G": "Grid",
        "T": "Tabs",
        "F": "Form",
        "IMG": "Image",
        "HR": "Divider",
        "PROG": "Progress",
        "DATE": "DatePicker",
        "COLOR": "ColorPicker",
        "CARD": "Card",
    }

    @classmethod
    def parse(cls, item: Any) -> Any:
        """解析简写为组件对象

        支持的简写格式:
        1. 字符串简写: "B:提交|bg=blue,color=white"
        2. 元组简写: ("B", "提交", {"bg": "blue"})
        3. 列表简写: ["B:提交|bg=blue"] 或 ["V|padding=20", [...]]
        4. 完整对象: 直接返回
        """
        # 已经是组件对象
        if hasattr(item, "_is_widget") or hasattr(item, "render"):
            return item

        # 字符串简写
        if isinstance(item, str):
            return cls._parse_string(item)

        # 元组简写
        if isinstance(item, tuple):
            return cls._parse_tuple(item)

        # 列表简写（布局容器）
        if isinstance(item, list) and len(item) > 0:
            return cls._parse_list(item)

        # 字典
        if isinstance(item, dict):
            return cls._parse_dict(item)

        return item

    @classmethod
    def _parse_string(cls, s: str) -> Any:
        """解析字符串简写"""
        s = s.strip()

        if not s:
            return None

        # 检查是否是纯文本（没有类型前缀）
        if not any(s.startswith(prefix) for prefix in list(cls.TYPE_MAP.keys()) + ["CARD"]):
            # 纯文本当作 Label
            from ..widgets.controls import Label
            return Label(s)

        # 解析格式: "TYPE:内容|属性1=值1,属性2=值2"
        # 或: "TYPE|属性1=值1" (无内容)

        parts = s.split("|", 1)
        type_and_content = parts[0]
        attrs_str = parts[1] if len(parts) > 1 else ""

        # 分离类型和内容
        type_content_parts = type_and_content.split(":", 1)
        widget_type = type_content_parts[0].strip().upper()
        content = type_content_parts[1].strip() if len(type_content_parts) > 1 else ""

        # 解析属性
        kwargs = cls._parse_attrs(attrs_str)

        # 创建对应组件
        return cls._create_widget(widget_type, content, kwargs)

    @classmethod
    def _parse_tuple(cls, t: Tuple) -> Any:
        """解析元组简写

        格式: (TYPE, content, {attrs}) 或 (TYPE, content) 或 (TYPE,)
        """
        if len(t) == 0:
            return None

        widget_type = str(t[0]).upper()
        content = t[1] if len(t) > 1 else ""
        kwargs = t[2] if len(t) > 2 else {}

        return cls._create_widget(widget_type, content, kwargs)

    @classmethod
    def _parse_list(cls, lst: List) -> Any:
        """解析列表简写

        格式: ["TYPE|属性", [子元素1, 子元素2, ...]]
        或: ["TYPE:内容|属性", ...] (非容器组件)
        """
        if len(lst) == 0:
            return None

        first = lst[0]

        # 第一个元素是字符串，可能是容器定义
        if isinstance(first, str):
            # 检查是否是容器类型
            container_types = ["V", "H", "G", "T", "F", "CARD"]
            type_match = re.match(r'^([A-Z]+)', first)

            if type_match and type_match.group(1) in container_types:
                widget_type = type_match.group(1)

                # 解析容器属性
                parts = first.split("|", 1)
                attrs_str = parts[1] if len(parts) > 1 else ""
                kwargs = cls._parse_attrs(attrs_str)

                # 解析子元素
                children = []
                for child in lst[1:]:
                    parsed = cls.parse(child)
                    if parsed is not None:
                        children.append(parsed)

                kwargs["children"] = children
                return cls._create_widget(widget_type, "", kwargs)
            else:
                # 非容器，当作字符串简写处理
                return cls._parse_string(first)

        # 不是容器定义，逐个解析
        return [cls.parse(item) for item in lst]

    @classmethod
    def _parse_dict(cls, d: Dict) -> Any:
        """解析字典"""
        if "type" in d:
            widget_type = d.pop("type").upper()
            return cls._create_widget(widget_type, d.pop("content", ""), d)
        return d

    @classmethod
    def _parse_attrs(cls, attrs_str: str) -> Dict[str, Any]:
        """解析属性字符串"""
        kwargs = {}

        if not attrs_str:
            return kwargs

        # 处理逗号分隔的属性
        # 注意: 需要处理值中包含逗号的情况（如 shadow=(0,0,#000,0.3)）
        parts = cls._smart_split(attrs_str, ",")

        for part in parts:
            part = part.strip()
            if not part:
                continue

            if "=" in part:
                key, value = part.split("=", 1)
                key = key.strip()
                value = value.strip()

                # 转换类型
                value = cls._convert_value(value)
                kwargs[key] = value
            else:
                # 无值的属性（如 checked）
                kwargs[part] = True

        return kwargs

    @classmethod
    def _smart_split(cls, s: str, delimiter: str) -> List[str]:
        """智能分割字符串，处理括号内的分隔符"""
        parts = []
        current = ""
        depth = 0

        for char in s:
            if char in "([{":
                depth += 1
                current += char
            elif char in ")]}":
                depth -= 1
                current += char
            elif char == delimiter and depth == 0:
                parts.append(current)
                current = ""
            else:
                current += char

        if current:
            parts.append(current)

        return parts

    @classmethod
    def _convert_value(cls, value: str) -> Any:
        """转换字符串值为适当类型"""
        # 布尔值
        if value.lower() == "true":
            return True
        if value.lower() == "false":
            return False

        # 空值
        if value.lower() == "none" or value == "":
            return None

        # 整数
        if re.match(r"^-?\\d+$", value):
            return int(value)

        # 浮点数
        if re.match(r"^-?\\d+\\.\\d+$", value):
            return float(value)

        # 元组（如 shadow=(2,2,#000,0.3)）
        if value.startswith("(") and value.endswith(")"):
            inner = value[1:-1]
            parts = [cls._convert_value(p.strip()) for p in inner.split(",")]
            return tuple(parts)

        # 列表
        if value.startswith("[") and value.endswith("]"):
            inner = value[1:-1]
            parts = [cls._convert_value(p.strip()) for p in inner.split(";")]
            return parts

        return value

    @classmethod
    def _create_widget(cls, widget_type: str, content: str, kwargs: Dict) -> Any:
        """创建组件实例"""
        from .. import widgets

        widget_type = widget_type.upper()

        # 处理内容中的占位符
        if content:
            kwargs["text"] = content

        # 特殊处理某些组件
        if widget_type == "B":
            from ..widgets.controls import Button
            text = kwargs.pop("text", "")
            return Button(text, **kwargs)

        elif widget_type == "I":
            from ..widgets.controls import Input
            placeholder = kwargs.pop("text", "")
            if placeholder:
                kwargs["placeholder"] = placeholder
            return Input(**kwargs)

        elif widget_type == "L":
            from ..widgets.controls import Label
            text = kwargs.pop("text", "")
            return Label(text, **kwargs)

        elif widget_type == "C":
            from ..widgets.controls import Checkbox
            text = kwargs.pop("text", "")
            return Checkbox(text, **kwargs)

        elif widget_type == "R":
            from ..widgets.controls import Radio
            text = kwargs.pop("text", "")
            if text:
                kwargs["options"] = text.split(";") if ";" in text else [text]
            return Radio(**kwargs)

        elif widget_type == "D":
            from ..widgets.controls import Dropdown
            text = kwargs.pop("text", "")
            if text:
                kwargs["options"] = text.split(";") if ";" in text else [text]
            return Dropdown(**kwargs)

        elif widget_type == "S":
            from ..widgets.controls import Slider
            return Slider(**kwargs)

        elif widget_type == "IMG":
            from ..widgets.controls import Image
            src = kwargs.pop("text", "")
            if src:
                kwargs["src"] = src
            return Image(**kwargs)

        elif widget_type == "HR":
            from ..widgets.controls import Divider
            return Divider(**kwargs)

        elif widget_type == "PROG":
            from ..widgets.controls import Progress
            value = kwargs.pop("text", 0)
            if value:
                try:
                    kwargs["value"] = float(value)
                except:
                    kwargs["value"] = 0
            return Progress(**kwargs)

        elif widget_type == "DATE":
            from ..widgets.controls import DatePicker
            return DatePicker(**kwargs)

        elif widget_type == "COLOR":
            from ..widgets.controls import ColorPicker
            return ColorPicker(**kwargs)

        # 容器组件
        elif widget_type == "H":
            from ..widgets.containers import HBox
            children = kwargs.pop("children", [])
            return HBox(children, **kwargs)

        elif widget_type == "V":
            from ..widgets.containers import VBox
            children = kwargs.pop("children", [])
            return VBox(children, **kwargs)

        elif widget_type == "G":
            from ..widgets.containers import Grid
            children = kwargs.pop("children", [])
            return Grid(children, **kwargs)

        elif widget_type == "T":
            from ..widgets.containers import Tabs
            children = kwargs.pop("children", [])
            return Tabs(children, **kwargs)

        elif widget_type == "F":
            from ..widgets.containers import Form
            children = kwargs.pop("children", [])
            return Form(children, **kwargs)

        elif widget_type == "CARD":
            from ..widgets.containers import Card
            children = kwargs.pop("children", [])
            return Card(children, **kwargs)

        # 未知类型，返回文本
        from ..widgets.controls import Label
        return Label(f"[Unknown: {widget_type}]")


def parse_shorthand(item: Any) -> Any:
    """便捷函数：解析简写"""
    return ShorthandParser.parse(item)
