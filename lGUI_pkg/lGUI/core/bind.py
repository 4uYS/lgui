"""
数据绑定系统 - 支持双向数据绑定和响应式更新
"""
from typing import Any, Dict, Callable, Optional, List
import weakref


class Observable:
    """可观察对象"""

    def __init__(self, value: Any = None):
        self._value = value
        self._callbacks: List[Callable] = []
        self._bindings: List[weakref.ref] = []

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        if self._value != new_value:
            old_value = self._value
            self._value = new_value
            self._notify(old_value, new_value)

    def _notify(self, old_value, new_value):
        """通知所有观察者"""
        for callback in self._callbacks:
            try:
                callback(new_value, old_value)
            except Exception as e:
                print(f"Binding callback error: {e}")

    def bind(self, callback: Callable):
        """绑定回调函数"""
        self._callbacks.append(callback)
        # 立即触发一次
        callback(self._value, None)

    def unbind(self, callback: Callable):
        """解绑回调函数"""
        if callback in self._callbacks:
            self._callbacks.remove(callback)

    def __repr__(self):
        return f"Observable({self._value!r})"

    def __str__(self):
        return str(self._value)

    def __eq__(self, other):
        if isinstance(other, Observable):
            return self._value == other._value
        return self._value == other

    def __hash__(self):
        return hash(self._value)


class ReactiveDict:
    """响应式字典"""

    def __init__(self, data: Dict[str, Any] = None):
        self._data = data or {}
        self._observers: Dict[str, Observable] = {}
        self._global_callbacks: List[Callable] = []

        # 为每个键创建 Observable
        for key, value in self._data.items():
            self._observers[key] = Observable(value)

    def __getitem__(self, key: str):
        if key in self._observers:
            return self._observers[key].value
        return self._data.get(key)

    def __setitem__(self, key: str, value: Any):
        if key in self._observers:
            old_value = self._observers[key].value
            self._observers[key].value = value
            self._data[key] = value
            self._notify_global(key, value, old_value)
        else:
            self._data[key] = value
            self._observers[key] = Observable(value)
            self._notify_global(key, value, None)

    def __contains__(self, key: str):
        return key in self._data

    def get(self, key: str, default=None):
        return self._data.get(key, default)

    def set(self, key: str, value: Any):
        self.__setitem__(key, value)

    def bind(self, key: str, callback: Callable):
        """绑定特定键的观察者"""
        if key not in self._observers:
            self._observers[key] = Observable(self._data.get(key))
        self._observers[key].bind(callback)

    def unbind(self, key: str, callback: Callable):
        """解绑特定键的观察者"""
        if key in self._observers:
            self._observers[key].unbind(callback)

    def bind_global(self, callback: Callable):
        """绑定全局观察者"""
        self._global_callbacks.append(callback)

    def _notify_global(self, key: str, new_value: Any, old_value: Any):
        """通知全局观察者"""
        for callback in self._global_callbacks:
            try:
                callback(key, new_value, old_value)
            except Exception as e:
                print(f"Global binding error: {e}")

    def to_dict(self) -> Dict[str, Any]:
        """转换为普通字典"""
        return dict(self._data)

    def keys(self):
        return self._data.keys()

    def values(self):
        return self._data.values()

    def items(self):
        return self._data.items()

    def __repr__(self):
        return f"ReactiveDict({self._data!r})"


def bind(data: Dict[str, Any] = None) -> ReactiveDict:
    """创建响应式数据对象

    Args:
        data: 初始数据字典

    Returns:
        ReactiveDict 对象

    Example:
        data = bind({"name": "张三", "age": 25})
        data.bind("name", lambda v: print(f"Name changed to: {v}"))
        data["name"] = "李四"  # 触发回调
    """
    return ReactiveDict(data)


def reactive(value: Any = None) -> Observable:
    """创建响应式值

    Args:
        value: 初始值

    Returns:
        Observable 对象

    Example:
        count = reactive(0)
        count.bind(lambda v: print(f"Count: {v}"))
        count.value = 5  # 触发回调，输出 "Count: 5"
    """
    return Observable(value)
