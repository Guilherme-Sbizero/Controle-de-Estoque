# Controle de Estoque

Um aplicativo simples de controle de estoque com interface gráfica moderna utilizando `CustomTkinter` e banco de dados SQLite.

## Funcionalidades

- Cadastro de produtos com nome, quantidade, preço e tipo (Unidade/Caixa)
- Edição e exclusão de produtos
- Pesquisa por nome de produto
- Ordenação por preço (crescente/decrescente)
- Exportação para arquivo Excel (.xlsx)
- Interface visual moderna com cores personalizadas

## Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/ControleEstoque.git
   cd ControleEstoque
   ```

2. Crie um ambiente virtual (opcional, mas recomendado):
   ```bash
   python -m venv venv
   source venv/bin/activate  # no Linux/macOS
   venv\Scripts\activate     # no Windows
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

## Como usar

Execute o programa com:

```bash
python main.py
```

O banco de dados será criado automaticamente como `estoque.db`.

## Requisitos

- Python 3.8 ou superior

## Estrutura do Projeto

```
ControleEstoque/
├── main.py
├── interface.py
├── banco_de_dados.py
├── requirements.txt
└── README.md
```

---

## Licença

MIT License © 2025 Guilherme Sbizero
