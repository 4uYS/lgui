"""
工具函数 - 组件装饰器、条件渲染、循环渲染等
"""
from typing import Any, Callable, List, Dict, Optional
import functools


# 组件注册表
_component_registry: Dict[str, Callable] = {}


def component(func: Callable = None, *, name: str = None):
    """组件装饰器 - 将函数标记为可复用组件

    Args:
        func: 被装饰的函数
        name: 组件名称（可选，默认使用函数名）

    Returns:
        包装后的组件函数

    Example:
        @component
        def UserCard(name, role):
            return [
                ["L:{name}|bold=True"],
                ["L:{role}|color=gray"],
            ]

        # 使用
        layout = [
            UserCard("张三", "管理员"),
            UserCard("李四", "用户"),
        ]
    """
    def decorator(f):
        comp_name = name or f.__name__

        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            # 执行组件函数获取布局定义
            result = f(*args, **kwargs)

            # 标记为组件实例
            if isinstance(result, list):
                result = ComponentInstance(comp_name, result, args, kwargs)

            return result

        wrapper._is_component = True
        wrapper._component_name = comp_name
        _component_registry[comp_name] = wrapper

        return wrapper

    if func is not None:
        return decorator(func)
    return decorator


class ComponentInstance:
    """组件实例"""

    def __init__(self, name: str, layout: List, args: tuple, kwargs: dict):
        self.name = name
        self.layout = layout
        self.args = args
        self.kwargs = kwargs
        self._is_widget = True

    def __repr__(self):
        return f"ComponentInstance({self.name})"


class For:
    """循环渲染器

    Example:
        items = ["苹果", "香蕉", "橙子"]
        layout = [
            For(items, lambda i, item: [
                ["H|gap=10",
                    [f"L:{item}|bold=True"],
                    [f"B:删除|onclick=del_{i}"],
                ]
            ])
        ]
    """

    def __init__(self, items: List, render_fn: Callable = None, key: str = None):
        self.items = items
        self.render_fn = render_fn
        self.key = key
        self._is_widget = True

    def render(self, parent=None):
        """渲染循环内容"""
        results = []
        for i, item in enumerate(self.items):
            if self.render_fn:
                result = self.render_fn(i, item)
                results.append(result)
        return results

    def __repr__(self):
        return f"For({len(self.items)} items)"


class If:
    """条件渲染器

    Example:
        show_admin = True
        layout = [
            If(show_admin, [
                ["L:管理员面板|color=red"],
                ["B:用户管理"],
            ]),
            If(lambda: user.role == "admin", [
                ["B:删除|bg=danger"],
            ]),
        ]
    """

    def __init__(self, condition: Any, true_content: List, false_content: List = None):
        self.condition = condition
        self.true_content = true_content
        self.false_content = false_content or []
        self._is_widget = True

    def render(self, parent=None):
        """渲染条件内容"""
        # 评估条件
        if callable(self.condition):
            result = self.condition()
        else:
            result = bool(self.condition)

        if result:
            return self.true_content
        else:
            return self.false_content

    def __repr__(self):
        return "If(...)"


class Switch:
    """多条件渲染器

    Example:
        layout = [
            Switch("view_mode",
                list=["L:列表视图"],
                grid=["L:网格视图"],
                default=["L:默认视图"]
            )
        ]
    """

    def __init__(self, value: Any, **cases):
        self.value = value
        self.cases = cases
        self._is_widget = True

    def render(self, parent=None):
        """渲染匹配的内容"""
        if callable(self.value):
            val = self.value()
        else:
            val = self.value

        if val in self.cases:
            return self.cases[val]
        elif "default" in self.cases:
            return self.cases["default"]
        return []

    def __repr__(self):
        return f"Switch({self.value})"


def get_component(name: str) -> Optional[Callable]:
    """获取已注册的组件"""
    return _component_registry.get(name)


def list_components() -> List[str]:
    """列出所有已注册的组件"""
    return list(_component_registry.keys())
