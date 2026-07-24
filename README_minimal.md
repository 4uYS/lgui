<div align="center">

# lGUI

> 轻量级声明式 GUI 库

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![PyPI](https://img.shields.io/badge/PyPI-v0.1.0-orange.svg)](https://pypi.org/project/lGUI)

</div>

```python
import lGUI as lg

app = lg.App("Hello", size=(400, 300))
app.set_layout([
    ["L:Hello World|size=20px,bold=True"],
    ["B:点击我|bg=primary"],
])
app.run()
```

## Install

```bash
pip install lGUI
```

## Quick Start

| 简写 | 组件 | 示例 |
|------|------|------|
| `B` | Button | `["B:提交|bg=primary"]` |
| `I` | Input | `["I:请输入|width=200"]` |
| `L` | Label | `["L:标题|bold=True"]` |
| `V` | VBox | `["V|gap=10", [...]]` |
| `H` | HBox | `["H|gap=10", [...]]` |

## License

MIT
