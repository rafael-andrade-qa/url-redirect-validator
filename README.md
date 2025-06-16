# 🔁 URL Redirect Validator

Ferramenta automatizada para **validar redirecionamentos de URL** com base nos dados publicados via Builder.io. Gera relatórios com os resultados dos testes, identificando URLs que não estão redirecionando corretamente ou retornam códigos HTTP incorretos.

## ✨ Visão Geral

Este projeto executa duas etapas principais:

1. **`generate_redirect_json.py`**  
   Consulta a API do Builder.io para gerar um arquivo `redirects.json` contendo os redirecionamentos publicados.

2. **`check_redirects.py`**  
   Lê o arquivo JSON e testa se cada redirecionamento está funcionando corretamente (com o status HTTP esperado). Gera relatórios organizados em `./reports`.

> ✅ Suporte a **wildcards** (ex: `/rafa-test/*/`) substituindo por `wildcard` para evitar falsos negativos durante a validação.

---

## ⚙️ Requisitos

- Python 3.x
- [requests](https://pypi.org/project/requests/)
- Acesso à API do Builder.io com uma `API_KEY` válida

---

## 📦 Instalação

### 1. Clone o projeto

```bash
git clone https://github.com/rafael-andrade-qa/url-redirect-validator.git
cd url-redirect-validator
```

### 2. Crie e ative o ambiente virtual (opcional, mas recomendado)

```bash
python -m venv venv
# Ativação no macOS/Linux
source venv/bin/activate
# Ativação no Windows
.\venv\Scripts\activate 
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure a chave da API

Copie o arquivo `.env-example` e edite com sua chave da API Builder:

```bash
cp .env-example .env
```

Abra `.env` e edite:

```
API_KEY=sua_chave_aqui
```

---

## 🚀 Como Usar

### 1. Gerar lista de redirecionamentos (Builder.io)

```bash
python generate_redirect_json.py
```

> Opcional: filtre por nome do redirect
```bash
python generate_redirect_json.py "meu-filter"
```

O arquivo será salvo em:  
```
./json/redirects.json
```

---

### 2. Validar os redirecionamentos

```bash
python check_redirects.py ./json/redirects.json https://www.seusite.com.br
```

O script testará:

- Se cada URL inicial (`initial_url`) redireciona corretamente para a URL de destino (`redirected_url`)
- Se o código HTTP retornado está dentro do esperado (ex: 301 para redirect permanente)

#### Saídas geradas:

- ✅ `./reports/results.json`: todos os resultados
- ❌ `./reports/failed_tests.json`: somente redirecionamentos com falha

---

## 🧠 Suporte a Wildcards

Ao detectar URLs com `*`, como:

```json
{
  "initial_url": "/rafa-test/*/",
  "redirected_url": "/builder/homes/*/",
  "permanent": true
}
```

O script automaticamente substitui `*` por `wildcard` para simular e validar corretamente:

```
/rafa-test/wildcard/ → /builder/homes/wildcard/
```
