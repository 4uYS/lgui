"""
布局引擎 - 解析和渲染布局定义
"""
from typing import Any, List, Dict, Optional, Union
from .shorthand import parse_shorthand


class Layout:
    """布局引擎"""

    def __init__(self, definition: List = None):
        """初始化布局

        Args:
            definition: 布局定义（列表形式）
        """
        self.definition = definition or []
        self._parsed = None
        self._widgets = []

    def set_definition(self, definition: List):
        """设置布局定义"""
        self.definition = definition
        self._parsed = None

    def parse(self) -> List[Any]:
        """解析布局定义为组件树"""
        if self._parsed is not None:
            return self._parsed

        self._parsed = self._parse_items(self.definition)
        return self._parsed

    def _parse_items(self, items: List) -> List[Any]:
        """递归解析布局项"""
        results = []

        for item in items:
            parsed = self._parse_item(item)
            if parsed is not None:
                results.append(parsed)

        return results

    def _parse_item(self, item: Any) -> Any:
        """解析单个布局项"""
        # None 跳过
        if item is None:
            return None

        # 已经是组件对象
        if hasattr(item, "_is_widget"):
            return item

        # 字符串或元组 - 使用简写解析
        if isinstance(item, (str, tuple)):
            return parse_shorthand(item)

        # 列表 - 可能是容器定义
        if isinstance(item, list):
            return parse_shorthand(item)

        # 字典
        if isinstance(item, dict):
            return parse_shorthand(item)

        # 其他类型
        return item

    def render(self, backend=None, parent=None):
        """渲染布局到指定后端"""
        widgets = self.parse()
        rendered = []

        for widget in widgets:
            if hasattr(widget, "render"):
                result = widget.render(backend=backend, parent=parent)
                if result:
                    rendered.append(result)
            elif hasattr(widget, "layout"):
                # ComponentInstance
                from .shorthand import ShorthandParser
                inner_layout = Layout(widget.layout)
                inner_layout.parse()
                result = inner_layout.render(backend=backend, parent=parent)
                if result:
                    rendered.extend(result)

        self._widgets = rendered
        return rendered

    def __repr__(self):
        return f"Layout({len(self.definition)} items)"
