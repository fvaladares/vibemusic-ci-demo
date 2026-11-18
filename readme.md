# 🎵 VibeMusic API — Demo de Integração Contínua (CI)

Projeto prático desenvolvido para a disciplina de **Gestão da Qualidade de Software (GQS)** com o objetivo de demonstrar a automação de testes unitários integrada ao fluxo de versionamento (Gitflow) utilizando **FastAPI**, **Pytest**, **uv** e **GitHub Actions**.

---

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python 3.12+
* **Framework Web:** FastAPI
* **Gerenciador de Pacotes e Ambientes:** `uv` (Astral)
* **Framework de Testes:** Pytest + HTTPX (`TestClient`)
* **Integração Contínua (CI):** GitHub Actions

---

## 📂 Estrutura do Projeto

```text
vibemusic-ci-demo/
├── .github/
│   └── workflows/
│       └── ci.yml          # Esteira de CI (Quality Gate)
├── main.py                 # API REST com operações GET, POST, PUT e DELETE em memória
├── test_main.py            # Suíte de testes automatizados das rotas e regras de negócio
├── pyproject.toml          # Configuração do projeto e dependências
├── uv.lock                 # Lockfile de dependências reprodutíveis
└── README.md               # Documentação do projeto
```

---

## 🚀 Como Executar Localmente

### 1. Pré-requisitos
Certifique-se de ter o gerenciador **`uv`** instalado em sua máquina:
* **Linux / macOS:**
  ```bash
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```
* **Windows (PowerShell):**
  ```powershell
  powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
  ```

### 2. Clonar e Sincronizar o Ambiente
```bash
git clone <URL_DO_REPOSITORIO>
cd vibemusic-ci-demo

# Cria o ambiente virtual (.venv) e instala as dependências exatas do projeto
uv sync
```

### 3. Iniciar a API
```bash
uv run fastapi dev main.py
```
* **URL Base da API:** `http://127.0.0.1:8000`
* **Documentação Interativa (Swagger UI):** `http://127.0.0.1:8000/docs`

---

## 🧪 Executando os Testes Automatizados

Para rodar a suíte de testes unitários localmente antes de enviar alterações para o repositório remoto:

```bash
uv run pytest -v
```

### Cenários Cobertos
* `test_get_musica_existente`: Valida o retorno de uma faixa cadastrada (`HTTP 200`).
* `test_post_criar_musica_valida`: Valida o cadastro de uma nova música (`HTTP 201`).
* `test_post_bloquear_duracao_invalida`: Garante o princípio *Fail Fast*, bloqueando músicas com duração menor ou igual a zero (`HTTP 400`).
* `test_put_atualizar_musica`: Valida a atualização de dados de uma faixa existente (`HTTP 200`).
* `test_delete_remover_musica`: Valida a exclusão de uma música do armazenamento em memória (`HTTP 200`).

---

## ⚙️ Esteira de Integração Contínua (Quality Gate)

O arquivo `.github/workflows/ci.yml` configura um **Quality Gate** automatizado no GitHub Actions. 

* **Gatilhos:** Todo `push` ou `pull_request` direcionado às branches `main` ou `dev`.
* **Comportamento:** O GitHub sobe um ambiente Linux, instala o `uv`, sincroniza as dependências via `uv sync --locked` e executa `uv run pytest -v`.
* **Proteção de Código:** Caso qualquer teste falhe (por exemplo, uma alteração indevida na regra de validação de duração), o Pull Request é sinalizado com falha (`❌`), impedindo que código com defeitos seja integrado às branches principais.

---

## 🎯 Roteiro de Prática em Aula (Simulação de Falha)

1. Crie uma nova branch de funcionalidade a partir da `dev`:
   ```bash
   git checkout dev
   git checkout -b feature/alterar-regra
   ```
2. Introduza intencionalmente uma falha de regra de negócio em `main.py` (ex: permitir o cadastro de músicas com duração negativa).
3. Faça o `commit` e o `push` da branch:
   ```bash
   git add main.py
   git commit -m "feat: altera validacao de duracao"
   git push origin feature/alterar-regra
   ```
4. Abra um **Pull Request** no GitHub para a branch `dev` e observe a esteira do GitHub Actions detectar e bloquear o defeito automaticamente.
5. Corrija o código na mesma branch, envie um novo `push` e valide a aprovação (`✅`) antes de concluir o *merge*.