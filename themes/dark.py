"""
暗色主题
"""
from ..core.style import Theme

dark_theme = Theme(
    # 主色调
    primary="#5b8def",
    secondary="#6c757d",
    success="#2ecc71",
    danger="#e74c3c",
    warning="#f39c12",
    info="#3498db",
    light="#f8f9fa",
    dark="#1a1a2e",

    # 背景色
    background="#0f0f23",
    surface="#1a1a2e",
    text="#e0e0e0",
    text_secondary="#a0a0a0",
    border="#2d2d44",
    muted="#6c757d",
    accent="#5b8def",

    # 字体
    font_family="system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto",
    font_size_base="14px",
    font_weight_base="400",
    line_height_base="1.5",

    # 阴影
    shadow_sm="0 1px 2px rgba(0,0,0,0.2)",
    shadow_md="0 4px 6px rgba(0,0,0,0.3)",
    shadow_lg="0 10px 15px rgba(0,0,0,0.4)",
    shadow_xl="0 20px 25px rgba(0,0,0,0.5)",

    # 尺寸
    border_radius="6px",
    border_radius_sm="4px",
    border_radius_lg="8px",
    spacing_unit="8px",
)
