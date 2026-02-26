# Arquitetura de `base_model.py` e `settings.py`

---

## 📦 `model/base_model.py`

Este arquivo contém a definição da classe base para todos os modelos SQLAlchemy utilizados no projeto. Ele utiliza o sistema de mapeamento do SQLAlchemy moderno com `DeclarativeBase` e define campos comuns e utilidades para herança.

### Principais componentes

- **`table_registry`**: um `registry()` utilizado para registrar automaticamente todas as tabelas criadas pelos modelos herdados, facilitando a geração de esquema e migrações.

- **`class Base(DeclarativeBase)`**: classe abstrata que garante que todos os modelos derivem de um mesmo registro. Ela injeta o `table_registry` para centralizar o registro de tabelas.

- **`@dataclass class BaseModel(Base)`**: define campos padrões que qualquer entidade no banco de dados terá.
  - Campos comuns:
    - `id`: UUID primária gerada automaticamente (v4).
    - `created_by`, `created_at`, `updated_by`, `updated_at`, `deleted_by`, `deleted_at`, `activated_by`, `activated_at`: metadados de auditoria.
    - `is_active`, `is_deleted`: flags booleanas com índices para consultas rápidas.
  - Métodos utilitários:
    - `as_dict()`: converte instâncias em dicionários, útil para serialização.
    - `soft_activate()`, `restore_activate()`: marcas de ativação/desativação lógica.
    - `soft_delete()`, `restore_delete()`: exclusão lógica e restauração.
  - Construtor personalizado que aceita `**kwargs` e atribui os valores aos atributos antes de chamar o super.

### Uso

Modelos específicos do domínio devem herdar de `BaseModel` e declarar suas próprias colunas. Eles já herdarão os campos de auditoria e utilitários.

Exemplo breve:
```python
class User(BaseModel):
    __tablename__ = 'users'
    name: Mapped[str] = mapped_column()
```

---

## ⚙️ `services/settings.py`

Este arquivo implementa a configuração da aplicação utilizando **Pydantic Settings**. Ele centraliza todas as variáveis de ambiente e oferece uma interface para construção de URLs de conexão com o banco de dados.

### Principais componentes

- **`class Settings(BaseSettings)`**: classe que herda de `BaseSettings`, permitindo a carga de configurações via variáveis de ambiente (inclui `.env`). O `model_config` estabelece comportamento como arquivos `.env`, case sensitive e ignorar extras.

- **Campos de configuração**:
  - **Informações gerais**: `APP_NAME`, `APP_VERSION`, `DATE_TIME`, `DEBUG`, `ENVIRONMENT`, `ASYNC_MODE`.
  - **Dados de banco**: credenciais (`DB_USER`, `DB_PASSWORD`), host, porta, nomes de bancos (produção e teste), `DATABASE_ECHO`, `DB_SCHEMA`.

- **Método `get_database_url()`**:
  - Constrói um objeto `sqlalchemy.engine.URL` usando os parâmetros divididos.
  - Suporta driver assíncrono (`asyncpg`) ou síncrono (`psycopg2`) e alterna para banco de teste.

- **`settings = Settings()`**: instância global que pode ser importada por outros módulos para acessar a configuração.

### Uso

Importe `settings` onde precisar de valores de configuração ou URL de conexão:
```python
from services.settings import settings

engine = create_engine(settings.get_database_url())
```

---

> 🔍 **Resumo**
> - `base_model.py` define a fundação de todos os modelos SQLAlchemy com campos e funções utilitárias para gerenciamento de estado.
> - `settings.py` concentra a configuração da aplicação usando Pydantic Settings e abstrai a criação de URLs de banco de dados.

Este documento serve como referência rápida para entender o funcionamento e como estender esses componentes no projeto.