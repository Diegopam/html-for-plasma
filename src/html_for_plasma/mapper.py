from __future__ import annotations

from dataclasses import dataclass, field

from .html_parser import HtmlNode
from .style import parse_px


@dataclass
class QmlNode:
    component: str
    props: dict[str, str] = field(default_factory=dict)
    children: list["QmlNode"] = field(default_factory=list)


TEXT_TAGS = {"span", "p", "label", "h1", "h2", "h3"}
CONTAINER_TAGS = {"html", "div", "section", "main", "header", "footer", "article", "body"}


class Mapper:
    def __init__(self) -> None:
        self.warnings: list[str] = []

    def map_tree(self, root: HtmlNode) -> QmlNode:
        app_root = QmlNode("Column", props={"spacing": "8"})
        for child in root.children:
            mapped = self.map_node(child)
            if mapped:
                app_root.children.append(mapped)
        return app_root

    def map_node(self, node: HtmlNode) -> QmlNode | None:
        tag = node.tag
        if tag in CONTAINER_TAGS:
            qnode = self._map_container(node)
        elif tag in TEXT_TAGS:
            qnode = self._map_text(node)
        elif tag == "button":
            qnode = QmlNode("Button", props={"text": self._quote(node.text or "Button")})
        elif tag == "input":
            qnode = self._map_input(node)
        elif tag == "textarea":
            qnode = QmlNode("TextArea", props={"text": self._quote(node.text)})
        elif tag == "img":
            qnode = QmlNode("Image", props={"source": self._quote(node.attrs.get("src", ""))})
        elif tag == "a":
            label = node.text or node.attrs.get("href", "link")
            qnode = QmlNode("Text", props={"text": self._quote(label), "color": self._quote("#3b82f6")})
        elif tag in {"ul", "ol"}:
            qnode = QmlNode("Column", props={"spacing": "4"})
        elif tag == "li":
            qnode = QmlNode("Text", props={"text": self._quote(f"• {node.text}")})
        else:
            self.warnings.append(f"Unsupported tag <{tag}> ignored as Item container")
            qnode = QmlNode("Item")

        self._apply_style(node, qnode)
        for child in node.children:
            mapped = self.map_node(child)
            if mapped:
                qnode.children.append(mapped)
        return qnode

    def _map_container(self, node: HtmlNode) -> QmlNode:
        display = (node.style.get("display") or "").lower()
        direction = (node.style.get("flex-direction") or "column").lower()
        if display == "flex" and direction == "row":
            return QmlNode("Row", props={"spacing": "8"})
        if display == "flex":
            return QmlNode("Column", props={"spacing": "8"})
        return QmlNode("Rectangle", props={"color": self._quote("transparent")})

    def _map_text(self, node: HtmlNode) -> QmlNode:
        text_value = node.text or ""
        props = {"text": self._quote(text_value)}
        if node.tag == "h1":
            props["font.pixelSize"] = "28"
        elif node.tag == "h2":
            props["font.pixelSize"] = "22"
        elif node.tag == "h3":
            props["font.pixelSize"] = "18"
        return QmlNode("Text", props=props)

    def _map_input(self, node: HtmlNode) -> QmlNode:
        input_type = node.attrs.get("type", "text").lower()
        if input_type == "checkbox":
            label = node.attrs.get("value", node.text or "")
            return QmlNode("CheckBox", props={"text": self._quote(label)})
        props = {}
        if placeholder := node.attrs.get("placeholder"):
            props["placeholderText"] = self._quote(placeholder)
        if value := node.attrs.get("value"):
            props["text"] = self._quote(value)
        if input_type == "password":
            props["echoMode"] = "TextInput.Password"
        return QmlNode("TextField", props=props)

    def _apply_style(self, node: HtmlNode, qnode: QmlNode) -> None:
        width = parse_px(node.style.get("width"))
        height = parse_px(node.style.get("height"))
        if width is not None:
            qnode.props["width"] = str(width)
        if height is not None:
            qnode.props["height"] = str(height)

        bg = node.style.get("background-color") or node.style.get("background")
        if bg and qnode.component in {"Rectangle", "Text", "Button"}:
            if qnode.component == "Text":
                self.warnings.append("background on text ignored in v1")
            else:
                qnode.props["color"] = self._quote(bg)

        fg = node.style.get("color")
        if fg and qnode.component in {"Text", "Button", "CheckBox", "TextField", "TextArea"}:
            qnode.props["palette.text"] = self._quote(fg)

        radius = parse_px(node.style.get("border-radius"))
        if radius is not None and qnode.component == "Rectangle":
            qnode.props["radius"] = str(radius)

        font_size = parse_px(node.style.get("font-size"))
        if font_size is not None and qnode.component in {"Text", "Button"}:
            qnode.props["font.pixelSize"] = str(font_size)

    @staticmethod
    def _quote(text: str) -> str:
        return '"' + text.replace('"', '\\"') + '"'
