# HTML for Plasma — MVP v1 Specification

## 1) Input format

The converter accepts a local `.html` file and produces a `.qml` file.

### Supported source features (v1)

- HTML5 documents with nested tags.
- Inline styles (`style="..."`) using simple CSS declarations.
- Common attributes:
  - `id`
  - `class`
  - `src` (for images)
  - `href` (for links)
  - `type`, `placeholder`, `value` (for inputs)

### CSS scope (v1)

The MVP reads only inline style declarations and maps a safe subset:

- `width`, `height`
- `background`, `background-color`
- `color`
- `font-size`, `font-weight`
- `border-radius`
- `display: flex`
- `flex-direction: row|column`
- `padding`, `margin` (best effort)

Unsupported properties are ignored with warnings in CLI output.

---

## 2) Mapping rules v1

| HTML element | Main QML target | Notes |
| --- | --- | --- |
| `div`, `section`, `main`, `header`, `footer` | `Rectangle` | Defaults to transparent background unless set. |
| `span`, `p`, `label`, `h1`, `h2`, `h3` | `Text` | Heading tags apply larger default font size. |
| `button` | `Button` | Content text mapped from inner text. |
| `input type=text|password|email` | `TextField` | Placeholder/value mapped when present. |
| `input type=checkbox` | `CheckBox` | Label uses nearby text content if available. |
| `textarea` | `TextArea` | Inner text becomes the default text value. |
| `img` | `Image` | `src` mapped to QML `source`. |
| `a` | `Text` | Rendered as clickable-looking text; `href` kept as comment. |
| `ul`, `ol` | `Column` | List container. |
| `li` | `Text` | Prefixes bullet (`•`) for `ul`. |

### Layout rules

- `display:flex` + `flex-direction: row` => `Row` container.
- `display:flex` + `flex-direction: column` => `Column` container.
- Otherwise, block containers use `Column` for child flow.
- Width and height are emitted directly when numeric values can be parsed.

---

## 3) Project structure

```text
html-for-plasma/
  docs/
    MVP_SPEC.md
  samples/
    sample_dashboard.html
  src/html_for_plasma/
    __init__.py
    cli.py
    converter.py
    html_parser.py
    mapper.py
    qml_emitter.py
    style.py
  tests/
    test_converter.py
  README.md
```

---

## 4) CLI behavior (v1)

```bash
python -m html_for_plasma.cli \
  --input samples/sample_dashboard.html \
  --output build/Main.qml
```

The command:

1. Parses HTML into an internal tree.
2. Converts each node with v1 mapping rules.
3. Emits a standalone `ApplicationWindow` QML file.
4. Prints warnings for unsupported tags/styles.
