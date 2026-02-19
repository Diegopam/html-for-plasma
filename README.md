# html-for-plasma

Ferramenta MVP para converter uma estrutura de interface em HTML para uma estrutura aproximada em QML (Qt/Plasma).

## Objetivo

Permitir que uma pessoa monte um layout inicial em HTML e gere um app/base QML com aparência e hierarquia parecidas.

## Estado atual (MVP v1)

- Conversor funcional via CLI.
- Suporte inicial para componentes HTML como:
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


## Instalação (Linux)

### 1) Pré-requisitos

- Python 3.10+
- `pip`

No Ubuntu/Debian:

```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv
```

### 2) Instalar a partir do código-fonte

```bash
git clone <URL_DO_REPOSITORIO>
cd html-for-plasma
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -e .
```

> O `-e` instala em modo desenvolvimento (qualquer alteração no código já reflete sem reinstalar).

### 3) Validar instalação

```bash
html-for-plasma --help
```

Se aparecer a ajuda da CLI, a instalação está OK.

## Como usar

### Exemplo rápido

```bash
html-for-plasma \
  --input samples/sample_dashboard.html \
  --output build/Main.qml
```

Saída esperada:

- Arquivo QML gerado no caminho definido em `--output`.

### Usando com Python (sem instalar script global)

```bash
PYTHONPATH=src python -m html_for_plasma.cli \
  --input samples/sample_dashboard.html \
  --output build/Main.qml
```

## Estrutura do projeto

```text
html-for-plasma/
  docs/MVP_SPEC.md
  samples/sample_dashboard.html
  src/html_for_plasma/
  tests/test_converter.py
```


## Rodar testes

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

- Veja detalhes completos em [`docs/MVP_SPEC.md`](docs/MVP_SPEC.md).
- Veja detalhes completos no arquivo [`docs/MVP_SPEC.md`](docs/MVP_SPEC.md).
