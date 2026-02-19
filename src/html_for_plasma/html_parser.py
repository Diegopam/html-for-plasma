from __future__ import annotations

from dataclasses import dataclass, field
from html.parser import HTMLParser

from .style import Style


@dataclass
class HtmlNode:
    tag: str
    attrs: dict[str, str] = field(default_factory=dict)
    style: Style = field(default_factory=Style)
    text: str = ""
    children: list["HtmlNode"] = field(default_factory=list)


class UiHtmlParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.root = HtmlNode(tag="root")
        self.stack: list[HtmlNode] = [self.root]

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attrs_dict: dict[str, str] = {k: (v or "") for k, v in attrs}
        node = HtmlNode(
            tag=tag.lower(),
            attrs=attrs_dict,
            style=Style.parse(attrs_dict.get("style")),
        )
        self.stack[-1].children.append(node)
        self.stack.append(node)

    def handle_endtag(self, tag: str) -> None:
        if len(self.stack) > 1:
            self.stack.pop()

    def handle_data(self, data: str) -> None:
        stripped = data.strip()
        if stripped:
            node = self.stack[-1]
            if node.text:
                node.text += " "
            node.text += stripped


def parse_html(html_content: str) -> HtmlNode:
    parser = UiHtmlParser()
    parser.feed(html_content)
    parser.close()
    return parser.root
