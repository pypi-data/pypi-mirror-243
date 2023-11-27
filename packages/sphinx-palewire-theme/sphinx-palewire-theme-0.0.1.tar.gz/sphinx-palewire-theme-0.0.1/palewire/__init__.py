"""Sphinx theme for palewi.re documentation."""
from pathlib import Path


def setup(app):
    """Register the theme with Sphinx."""
    theme_path = Path(__file__).parent.absolute()
    app.add_html_theme("palewire", str(theme_path))
    return {"parallel_read_safe": True, "parallel_write_safe": True}
