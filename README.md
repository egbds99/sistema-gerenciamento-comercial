# Sistema de Gerenciamento Comercial

MVP web acadêmico para cadastro de produtos, registro de vendas e controle de estoque de pequenos empreendimentos.

## Funcionalidades
- Autenticação com senha armazenada por Argon2id.
- Cadastro, consulta e inativação de produtos.
- Registro de venda com validação de estoque.
- Atualização automática do estoque e registro de movimentação.
- Alertas de estoque baixo e histórico de vendas.

## Tecnologias
Python 3.12, Flask 3, SQLAlchemy 2, PostgreSQL (SQLite local), Flask-Login, Flask-WTF/CSRF, Argon2id, HTML5, CSS3 e pytest.

## Executar localmente
1. Instale Python 3.12.
2. Crie um ambiente: `py -3.12 -m venv .venv` (Windows) ou `python3.12 -m venv .venv` (Linux/macOS).
3. Ative o ambiente virtual.
4. Instale: `pip install -r requirements.txt`.
5. Copie `.env.example` para `.env` e ajuste os valores. O arquivo é carregado automaticamente. Para desenvolvimento local, deixe `DATABASE_URL` vazio para usar SQLite.
6. Defina `ADMIN_USERNAME` e `ADMIN_PASSWORD` no ambiente. A senha deve ter pelo menos 10 caracteres.
7. Execute `flask --app run.py init-db` e `flask --app run.py create-admin`.
8. Inicie com `flask --app run.py run --debug` e acesse http://127.0.0.1:5000.

O `.env` não deve ser enviado ao GitHub. Em produção, configure `SECRET_KEY` forte, PostgreSQL e `COOKIE_SECURE=true` sob HTTPS.

## Testes
Execute `pytest -q`. Os testes utilizam banco SQLite temporário e dados fictícios.

## Estrutura
- `app/routes`: rotas da aplicação.
- `app/services`: regras de negócio.
- `app/models.py`: entidades e relacionamentos.
- `app/templates`: interfaces.
- `app/static`: estilos.
- `tests`: testes automatizados.

## Regras
Produtos inativos não podem ser vendidos. Preços e quantidades não podem ser negativos. Quantidade da venda deve ser positiva e não pode superar o estoque. A venda, o item, a movimentação e a atualização de estoque são persistidos em uma transação.

## Segurança e acessibilidade
Rotas protegidas por autenticação, hash Argon2id, CSRF nos formulários, ORM SQLAlchemy, cookies HttpOnly/SameSite, rótulos associados, foco visível, link para pular ao conteúdo, mensagens textuais e controles com altura mínima de 44 px.

## Limitações do MVP
O fluxo de venda registra um produto por operação. Não inclui emissão fiscal, pagamentos, integração bancária, aplicativo nativo ou operação offline. O projeto requer validação com usuários e revisão de segurança antes de uso comercial.
