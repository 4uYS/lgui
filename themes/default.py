"""
默认亮色主题
"""
from ..core.style import Theme

default_theme = Theme(
    # 主色调
    primary="#3498db",
    secondary="#6c757d",
    success="#27ae60",
    danger="#e74c3c",
    warning="#f39c12",
    info="#17a2b8",
    light="#f8f9fa",
    dark="#343a40",

    # 背景色
    background="#ffffff",
    surface="#f8f9fa",
    text="#212529",
    text_secondary="#6c757d",
    border="#dee2e6",
    muted="#6c757d",
    accent="#3498db",

    # 字体
    font_family="system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto",
    font_size_base="14px",
    font_weight_base="400",
    line_height_base="1.5",

    # 阴影
    shadow_sm="0 1px 2px rgba(0,0,0,0.05)",
    shadow_md="0 4px 6px rgba(0,0,0,0.1)",
    shadow_lg="0 10px 15px rgba(0,0,0,0.1)",
    shadow_xl="0 20px 25px rgba(0,0,0,0.15)",

    # 尺寸
    border_radius="6px",
    border_radius_sm="4px",
    border_radius_lg="8px",
    spacing_unit="8px",
)
