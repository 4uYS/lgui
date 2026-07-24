<div align="center">

# 🎨 lGUI

**用 Python 写 GUI，像写 Markdown 一样简单**

[![PyPI](https://img.shields.io/pypi/v/lGUI?color=blue&label=PyPI)](https://pypi.org/project/lGUI)
[![Python](https://img.shields.io/badge/Python-3.7%2B-blue)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Stars](https://img.shields.io/github/stars/4uYS/lgui?style=social)](https://github.com/4uYS/lgui)

</div>

## 📖 简介

lGUI 是一个**轻量级声明式 GUI 库**，让你用 Python 数据结构就能创建复杂的桌面应用界面。

告别繁琐的逐行 widget 创建代码，用**简写语法**一行搞定！

## 🚀 快速开始

### 安装

```bash
pip install lGUI
```

### 第一个程序

```python
import lGUI as lg

app = lg.App("你好 lGUI", size=(400, 300))

layout = [
    ["L:欢迎使用 lGUI！|size=20px,bold=True,color=primary"],
    ["I:请输入姓名|width=200"],
    ["B:提交|bg=primary,color=white"],
]

app.set_layout(layout)
app.run()
```

就这么简单！🎉

## ✨ 核心特性

- 📝 **声明式布局** — 用列表定义界面，直观清晰
- ⚡ **简写语法** — `B:提交` = 按钮，`I:输入` = 输入框
- 🎨 **主题系统** — 内置亮色/暗色主题，支持自定义
- 🔗 **数据绑定** — 自动双向绑定，数据驱动视图
- 🧩 **组件化** — `@component` 装饰器，轻松复用

## 📦 简写速查

| 简写 | 组件 | 完整写法示例 |
|:----:|:----:|:------------|
| `B` | 按钮 | `["B:提交|bg=primary"]` |
| `I` | 输入框 | `["I:请输入|width=200"]` |
| `L` | 标签 | `["L:标题|bold=True"]` |
| `C` | 复选框 | `["C:同意协议|checked=True"]` |
| `D` | 下拉框 | `["D:男;女;保密|value=男"]` |
| `V` | 垂直布局 | `["V|gap=10", [...]]` |
| `H` | 水平布局 | `["H|gap=10", [...]]` |
| `CARD` | 卡片 | `["CARD|title=标题", [...]]` |

## 🎨 主题切换

```python
import lGUI as lg

lg.set_theme("dark")   # 暗色主题
# 或
lg.set_theme("default") # 亮色主题
```

## 💡 更多示例

### 表单布局

```python
layout = [
    ["F|label_width=80",
        ["用户名", "I:|placeholder=输入用户名"],
        ["密码", "I:|password=True"],
        ["", "B:登录|bg=primary,full_width=True"],
    ],
]
```

### 数据绑定

```python
data = lg.bind({"name": "张三", "age": 25})

layout = [
    ["I:姓名|bind=name"],
    ["I:年龄|bind=age,type=int"],
]

app.bind_data(data.to_dict())
```

## 🤝 参与贡献

欢迎提交 Issue 和 PR！

1. Fork 本仓库
2. 创建分支：`git checkout -b feature/xxx`
3. 提交更改：`git commit -m "feat: xxx"`
4. 推送分支：`git push origin feature/xxx`
5. 提交 Pull Request

## 📄 开源协议

[MIT](LICENSE) © lGUI Team
