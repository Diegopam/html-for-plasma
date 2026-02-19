"""html-for-plasma: convert HTML UI structures to QML (Plasma/Qt) skeletons."""

from .converter import convert_html_file, convert_html_string

__all__ = ["convert_html_file", "convert_html_string"]
