from __future__ import annotations

from pathlib import Path

from .html_parser import parse_html
from .mapper import Mapper
from .qml_emitter import emit_qml


def convert_html_string(html_content: str) -> tuple[str, list[str]]:
    html_root = parse_html(html_content)
    mapper = Mapper()
    qml_tree = mapper.map_tree(html_root)
    qml = emit_qml(qml_tree)
    return qml, mapper.warnings


def convert_html_file(input_path: str | Path, output_path: str | Path) -> list[str]:
    in_path = Path(input_path)
    out_path = Path(output_path)
    html_content = in_path.read_text(encoding="utf-8")
    qml, warnings = convert_html_string(html_content)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(qml, encoding="utf-8")
    return warnings
