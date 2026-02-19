from html_for_plasma.converter import convert_html_string


def test_generates_expected_components() -> None:
    html = """
    <html><body>
      <div style='display:flex; flex-direction:row;'>
        <span>Nome</span>
        <input type='text' placeholder='Seu nome' />
        <button>Salvar</button>
        <input type='checkbox' value='Ativo' />
      </div>
      <textarea>Notas</textarea>
      <img src='pic.png' />
      <ul><li>A</li></ul>
    </body></html>
    """
    qml, warnings = convert_html_string(html)

    assert "ApplicationWindow" in qml
    assert "Row {" in qml
    assert "TextField {" in qml
    assert "Button {" in qml
    assert "CheckBox {" in qml
    assert "TextArea {" in qml
    assert "Image {" in qml
    assert "• A" in qml
    assert warnings == []
