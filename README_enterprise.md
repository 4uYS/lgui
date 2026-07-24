<div align="center">

# <img src="https://raw.githubusercontent.com/4uYS/lgui/main/docs/logo.png" width="40" alt="lGUI"> lGUI

**Enterprise-grade Declarative GUI Framework for Python**

[![Build Status](https://github.com/4uYS/lgui/workflows/CI/badge.svg)](https://github.com/4uYS/lgui/actions)
[![PyPI Version](https://img.shields.io/pypi/v/lGUI)](https://pypi.org/project/lGUI)
[![Python Versions](https://img.shields.io/pypi/pyversions/lGUI)](https://pypi.org/project/lGUI)
[![Code Coverage](https://img.shields.io/codecov/c/github/4uYS/lgui)](https://codecov.io/gh/4uYS/lgui)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Documentation](https://img.shields.io/badge/Docs-ReadTheDocs-blue)](https://lgui.readthedocs.io)

[Documentation](https://lgui.readthedocs.io) · [API Reference](https://lgui.readthedocs.io/api) · [Examples](https://lgui.readthedocs.io/examples) · [Changelog](CHANGELOG.md)

</div>

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Documentation](#documentation)
- [Architecture](#architecture)
- [Contributing](#contributing)
- [License](#license)

## Overview

lGUI is a production-ready declarative GUI library designed for Python developers who need to build desktop applications quickly without sacrificing flexibility or maintainability.

### Design Principles

- **Declarative over Imperative**: Describe what the UI should look like, not how to build it
- **Convention over Configuration**: Sensible defaults that work out of the box
- **Progressive Enhancement**: Start with simple shorthand, graduate to full API when needed
- **Backend Agnostic**: Currently supports Tkinter, with PyQt and WxPython backends planned

## Features

### Core Capabilities

- ✅ **Declarative Layout Engine** — Build UIs with Python data structures
- ✅ **Shorthand Syntax** — Reduce boilerplate by 50%+ with string/tuple abbreviations
- ✅ **Theme System** — Built-in light/dark themes with full customization support
- ✅ **Data Binding** — Automatic two-way binding between widgets and data models
- ✅ **Component System** — Reusable custom components via `@component` decorator
- ✅ **Style Engine** — CSS-like inline styling with theme integration

### Widget Library

| Category | Widgets |
|----------|---------|
| Controls | Button, Input, Label, Checkbox, Radio, Dropdown, Slider, Image, Divider, Progress, DatePicker, ColorPicker |
| Containers | VBox, HBox, Grid, Tabs, Form, Card |

### Supported Platforms

| Platform | Status | Backend |
|----------|--------|---------|
| Windows | ✅ Supported | Tkinter |
| macOS | ✅ Supported | Tkinter |
| Linux | ✅ Supported | Tkinter |

## Installation

### From PyPI (Recommended)

```bash
pip install lGUI
```

### From Source

```bash
git clone https://github.com/4uYS/lgui.git
cd lgui
pip install -e ".[dev]"
```

### Optional Dependencies

```bash
# Image support
pip install lGUI[pillow]

# Development tools
pip install lGUI[dev]
```

## Quick Start

### Hello World

```python
import lGUI as lg

app = lg.App("Hello World", size=(400, 300))
app.set_layout([
    ["L:Hello, lGUI!|size=20px,bold=True,color=primary"],
    ["B:Get Started|bg=primary,color=white,onclick=start"],
])
app.run()
```

### Dashboard Example

```python
import lGUI as lg

lg.set_theme("dark")

app = lg.App("Dashboard", size=(1200, 800))

layout = [
    ["H|height=60,bg=primary,padding=15",
        ["L:Analytics Dashboard|color=white,bold=True,size=18"],
        ["H|gap=10",
            ["B:Settings|variant=ghost"],
            ["B:Logout|variant=danger"],
        ],
    ],
    ["H|flex=1",
        ["V|width=240,bg=surface,padding=15,gap=5",
            ["L:NAVIGATION|color=text_secondary,size=11,uppercase"],
            ["B:Overview|active=True"],
            ["B:Analytics"],
            ["B:Users"],
            ["B:Settings"],
        ],
        ["V|flex=1,padding=24,gap=24",
            ["H|gap=20",
                ["CARD|flex=1,padding=20",
                    ["L:Total Revenue|color=text_secondary"],
                    ["L:$128,430|size=28,bold=True"],
                    ["L:+12.5%|color=success"],
                ],
                ["CARD|flex=1,padding=20",
                    ["L:Active Users|color=text_secondary"],
                    ["L:8,432|size=28,bold=True"],
                    ["L:+5.2%|color=success"],
                ],
            ],
            ["CARD|title=Recent Orders,padding=20",
                ["V|gap=5",
                    ["H|gap=10,bg=surface,padding=8",
                        ["L:Order|flex=1,bold=True"],
                        ["L:Customer|flex=1,bold=True"],
                        ["L:Amount|flex=1,bold=True"],
                        ["L:Status|flex=1,bold=True"],
                    ],
                    ["H|gap=10,padding=8",
                        ["L:#1001|flex=1"],
                        ["L:Alice|flex=1"],
                        ["L:$299|flex=1"],
                        ["L:Completed|color=success,flex=1"],
                    ],
                ],
            ],
        ],
    ],
]

app.set_layout(layout)
app.run()
```

## Documentation

Full documentation is available at [lgui.readthedocs.io](https://lgui.readthedocs.io).

### API Reference

- [Application](https://lgui.readthedocs.io/api/app)
- [Layout Engine](https://lgui.readthedocs.io/api/layout)
- [Style System](https://lgui.readthedocs.io/api/style)
- [Data Binding](https://lgui.readthedocs.io/api/bind)
- [Widget Reference](https://lgui.readthedocs.io/api/widgets)

## Architecture

```
┌─────────────────────────────────────────┐
│              Application                  │
├─────────────────────────────────────────┤
│  Layout Engine  │  Style Engine         │
├─────────────────────────────────────────┤
│  Shorthand Parser │  Data Binding       │
├─────────────────────────────────────────┤
│  Widget Layer (Controls + Containers)   │
├─────────────────────────────────────────┤
│  Tkinter Backend │ (PyQt/WxPython TBD)  │
└─────────────────────────────────────────┘
```

## Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Setup

```bash
# Clone the repository
git clone https://github.com/4uYS/lgui.git
cd lgui

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest

# Run linting
flake8 lGUI
black lGUI
```

### Commit Convention

We follow [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` — New feature
- `fix:` — Bug fix
- `docs:` — Documentation changes
- `style:` — Code style changes
- `refactor:` — Code refactoring
- `test:` — Test changes
- `chore:` — Build/dependency changes

## License

This project is licensed under the [MIT License](LICENSE).

---

<div align="center">

**[⬆ Back to Top](#lGUI)**

Made with ❤️ by the lGUI Team

</div>
