from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="lGUI",
    version="0.1.0",
    description="轻量级声明式 GUI 库 - Lightweight Declarative GUI Library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="lGUI Team",
    author_email="lgui@example.com",
    url="https://github.com/lgui-team/lgui",
    project_urls={
        "Bug Tracker": "https://github.com/lgui-team/lgui/issues",
        "Documentation": "https://lgui.readthedocs.io",
        "Source Code": "https://github.com/lgui-team/lgui",
    },
    python_requires=">=3.7",
    packages=find_packages(),
    install_requires=[
        # tkinter 是 Python 标准库，无需安装
    ],
    extras_require={
        "pillow": ["Pillow>=8.0.0"],  # 图片支持
        "qt": ["PyQt5>=5.15.0"],      # Qt 后端（未来）
        "dev": [
            "pytest>=6.0",
            "black>=21.0",
            "flake8>=3.9",
            "twine>=3.4",
            "build>=0.5",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: User Interfaces",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    keywords="gui tkinter declarative layout shorthand widget",
    license="MIT",
    include_package_data=True,
    zip_safe=False,
)
