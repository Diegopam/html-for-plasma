# html-for-plasma

Ferramenta MVP para converter uma estrutura de interface em HTML para uma estrutura aproximada em QML (Qt/Plasma).

## Objetivo

Permitir que uma pessoa monte um layout inicial em HTML e gere um app/base QML com aparência e hierarquia parecidas.

## Estado atual (MVP v1)

- Conversor funcional via CLI.
- Suporte inicial para **10 componentes HTML**:
  - `div`/containers
  - `span`, `p`, `label`, `h1`, `h2`, `h3`
  - `button`
  - `input` (text/password/checkbox)
  - `textarea`
  - `img`
  - `a`
  - `ul` / `ol`
  - `li`

## Estrutura do projeto

```text
html-for-plasma/
  docs/MVP_SPEC.md
  samples/sample_dashboard.html
  src/html_for_plasma/
  tests/test_converter.py
```

## Como rodar

```bash
PYTHONPATH=src python -m html_for_plasma.cli \
  --input samples/sample_dashboard.html \
  --output build/Main.qml
```

## Testes

```bash
PYTHONPATH=src pytest -q
```

## Observações

- O v1 foca em mapeamento seguro e previsível.
- CSS avançado (grid complexo, pseudo-classes, animações, etc.) ainda não é suportado.
- Veja detalhes completos no arquivo [`docs/MVP_SPEC.md`](docs/MVP_SPEC.md).
