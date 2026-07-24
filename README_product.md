<div align="center">

<img src="https://img.shields.io/badge/lGUI-声明式GUI库-blue?style=for-the-badge&logo=python&logoColor=white" alt="lGUI">

### 🎨 用 Python 写 GUI，像写 HTML 一样简单

[![PyPI Version](https://img.shields.io/pypi/v/lGUI?style=flat-square)](https://pypi.org/project/lGUI)
[![Python Version](https://img.shields.io/pypi/pyversions/lGUI?style=flat-square)](https://pypi.org/project/lGUI)
[![GitHub Stars](https://img.shields.io/github/stars/4uYS/lgui?style=flat-square&logo=github)](https://github.com/4uYS/lgui)
[![License](https://img.shields.io/github/license/4uYS/lgui?style=flat-square)](LICENSE)

[📖 文档](https://github.com/4uYS/lgui#readme) · [🚀 快速开始](https://github.com/4uYS/lgui#quick-start) · [💬 讨论](https://github.com/4uYS/lgui/discussions)

</div>

---

## ✨ 为什么选择 lGUI？

| 特性 | 说明 |
|------|------|
| 📝 **声明式布局** | 用数据结构定义界面，告别繁琐的逐行代码 |
| ⚡ **简写语法** | `B:提交` = Button，代码量减少 50%+ |
| 🎨 **主题系统** | 内置亮色/暗色主题，一键切换 |
| 🔗 **数据绑定** | 自动双向绑定，数据驱动视图 |
| 🧩 **自定义组件** | `@component` 装饰器，轻松复用 |

## 🚀 Quick Start

```bash
pip install lGUI
```

```python
import lGUI as lg

lg.set_theme("dark")

app = lg.App("我的应用", size=(800, 600))

layout = [
    ["H|height=60,bg=primary",
        ["L:lGUI Dashboard|color=white,bold=True,size=18"],
    ],
    ["H|flex=1",
        ["V|width=200,bg=surface",
            ["B:概览"],
            ["B:分析"],
            ["B:设置"],
        ],
        ["V|flex=1,padding=20",
            ["CARD|title=统计",
                ["L:¥128,430|size=24,bold=True"],
                ["L:+12.5%|color=success"],
            ],
            ["F|label_width=80",
                ["姓名", "I:|placeholder=输入姓名"],
                ["邮箱", "I:|type=email"],
                ["", "B:提交|bg=primary,color=white"],
            ],
        ],
    ],
]

app.set_layout(layout)
app.run()
```

## 📦 简写速查表

```
B → Button      I → Input       L → Label
C → Checkbox    R → Radio       D → Dropdown
S → Slider      V → VBox        H → HBox
G → Grid        T → Tabs        F → Form
CARD → Card     IMG → Image     HR → Divider
```

## 🎨 主题

```python
lg.set_theme("dark")      # 暗色主题
lg.set_theme("default")   # 亮色主题（默认）

# 自定义主题
my_theme = lg.Theme(
    primary="#3498db",
    background="#0f0f23",
    surface="#1a1a2e",
)
lg.set_theme(my_theme)
```

## 🤝 Contributing

1. Fork 本仓库
2. 创建分支：`git checkout -b feature/xxx`
3. 提交 PR

## 📄 License

[MIT](LICENSE) © lGUI Team
