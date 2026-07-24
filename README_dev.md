<div align="center">

```
 _     _____   ____   _
| |   |  __ \ / __ \ | |
| |   | |  | || |  | || |
| |___| |__| || |__| || |___
|_____|_____/ \____/ |_____|
```

**lGUI** — Lightweight Declarative GUI for Python

[![CI](https://github.com/4uYS/lgui/actions/workflows/ci.yml/badge.svg)](https://github.com/4uYS/lgui/actions)
[![PyPI](https://img.shields.io/pypi/v/lGUI)](https://pypi.org/project/lGUI)
[![Downloads](https://img.shields.io/pypi/dm/lGUI)](https://pypi.org/project/lGUI)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

</div>

## Overview

lGUI is a **declarative GUI library** for Python that lets you build complex interfaces using data structures instead of imperative widget creation. Think of it as "React for Tkinter" — you describe *what* the UI should look like, and lGUI handles *how* to build it.

## Architecture

```
lGUI/
├── core/           # Layout engine, style system, data binding
│   ├── app.py      # Application runtime
│   ├── layout.py   # Layout parser
│   ├── style.py    # CSS-like styling
│   ├── shorthand.py # String/tuple shorthand parser
│   ├── bind.py     # Reactive data binding
│   └── utils.py    # Component decorators
├── widgets/        # Widget implementations
│   ├── controls.py # Button, Input, Label, etc.
│   ├── containers.py # VBox, HBox, Grid, Tabs, etc.
│   └── base.py     # Widget base class
└── themes/         # Theme presets
    ├── default.py  # Light theme
    └── dark.py     # Dark theme
```

## Installation

```bash
pip install lGUI
```

## Usage

### Shorthand Syntax

```python
import lGUI as lg

app = lg.App()
app.set_layout([
    # String shorthand: "TYPE:content|attr1=val1,attr2=val2"
    ["B:Submit|bg=primary,onclick=save"],
    ["I:Enter name|width=200,bind=username"],
    ["C:Agree to terms|checked=True"],
    ["D:Male;Female;Other|value=Male"],

    # Tuple shorthand: ("TYPE", "content", {attrs})
    ("B", "Cancel", {"bg": "danger"}),

    # Container shorthand
    ["V|padding=20,gap=10",       # Vertical container
        ["L:Section Title|bold=True"],
        ["I:|placeholder=Type here"],
    ],

    ["H|gap=10",                  # Horizontal container
        ["B:OK|bg=success"],
        ["B:Cancel|bg=danger"],
    ],
])
app.run()
```

### Full API

```python
from lGUI import App, Button, Input, VBox, Style
from lGUI.core.bind import bind

# Data binding
data = bind({"name": "", "email": ""})

app = App("Form Demo")
app.bind_data(data.to_dict())

layout = VBox([
    Input(placeholder="Name", bind="name"),
    Input(placeholder="Email", bind="email", type="email"),
    Button("Submit", onclick=lambda: print(data.to_dict())),
], padding="20px", gap="10px")

app.set_layout([layout])
app.run()
```

### Custom Components

```python
from lGUI import component

@component
def UserCard(name, role):
    return [
        ["CARD|padding=15",
            ["L:{name}|bold=True,size=16"],
            ["L:{role}|color=gray,size=12"],
        ],
    ]

layout = [
    UserCard("Alice", "Admin"),
    UserCard("Bob", "Developer"),
]
```

## Shorthand Reference

| Alias | Widget | Constructor |
|-------|--------|-------------|
| `B` | `Button` | `Button(text, **kwargs)` |
| `I` | `Input` | `Input(placeholder, **kwargs)` |
| `L` | `Label` | `Label(text, **kwargs)` |
| `C` | `Checkbox` | `Checkbox(text, **kwargs)` |
| `R` | `Radio` | `Radio(options, **kwargs)` |
| `D` | `Dropdown` | `Dropdown(options, **kwargs)` |
| `S` | `Slider` | `Slider(**kwargs)` |
| `V` | `VBox` | `VBox(children, **kwargs)` |
| `H` | `HBox` | `HBox(children, **kwargs)` |
| `G` | `Grid` | `Grid(children, cols=N, **kwargs)` |
| `T` | `Tabs` | `Tabs(tabs, **kwargs)` |
| `F` | `Form` | `Form(fields, **kwargs)` |
| `CARD` | `Card` | `Card(children, **kwargs)` |

## Development

```bash
git clone https://github.com/4uYS/lgui.git
cd lgui
pip install -e ".[dev]"
python -m pytest
```

## License

MIT. See [LICENSE](LICENSE).
