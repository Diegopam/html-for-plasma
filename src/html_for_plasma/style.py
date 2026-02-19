from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Style:
    values: dict[str, str] = field(default_factory=dict)

    @staticmethod
    def parse(style_text: str | None) -> "Style":
        if not style_text:
            return Style()
        parsed: dict[str, str] = {}
        for decl in style_text.split(";"):
            if ":" not in decl:
                continue
            key, value = decl.split(":", 1)
            key = key.strip().lower()
            value = value.strip()
            if key and value:
                parsed[key] = value
        return Style(values=parsed)

    def get(self, key: str, default: str | None = None) -> str | None:
        return self.values.get(key.lower(), default)


def parse_px(value: str | None) -> int | None:
    if not value:
        return None
    text = value.strip().lower().replace("px", "")
    try:
        return int(float(text))
    except ValueError:
        return None
