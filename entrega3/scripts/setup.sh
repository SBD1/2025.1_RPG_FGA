#!/bin/bash

# --- Configuração ---
PG_USER="postgres"         # Superusuário do PostgreSQL
DB_NAME="rpg_fga"          # Nome do banco de dados
APP_USER="estudante"       # Nome do usuário da aplicação
APP_PASSWORD="123"         # Senha do usuário

# --- Inicialização segura ---
set -e

# --- Caminho atual do script ---
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
echo "📂 Diretório dos scripts detectado: $SCRIPT_DIR"

# --- Cópia para /tmp ---
echo "📦 Copiando arquivos SQL para /tmp..."
cp "$SCRIPT_DIR/DDL.sql" /tmp/DDL.sql
cp "$SCRIPT_DIR/DML.sql" /tmp/DML.sql
cp "$SCRIPT_DIR/permissions.sql" /tmp/permissions.sql

# --- Recriação do banco ---
echo "🚧 Recriando o banco de dados '$DB_NAME'..."
sudo -u "$PG_USER" psql -d postgres -c "DROP DATABASE IF EXISTS $DB_NAME;"
sudo -u "$PG_USER" psql -d postgres -c "CREATE DATABASE $DB_NAME;"
echo "✅ Banco de dados '$DB_NAME' criado."

# --- Criação do usuário ---
echo "👤 Criando o usuário '$APP_USER' e concedendo permissões..."
sudo -u "$PG_USER" psql -d "$DB_NAME" <<-EOSQL
    DO \$\$
    BEGIN
        IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = '$APP_USER') THEN
            CREATE USER $APP_USER WITH PASSWORD '$APP_PASSWORD';
        END IF;
    END
    \$\$;
    ALTER USER $APP_USER WITH SUPERUSER;
EOSQL

# --- Execução dos scripts SQL ---
echo "🧱 Executando DDL.sql..."
sudo -u "$PG_USER" psql -d "$DB_NAME" -f /tmp/DDL.sql

echo "🌱 Executando DML.sql..."
sudo -u "$PG_USER" psql -d "$DB_NAME" -f /tmp/DML.sql

echo "🔐 Executando permissions.sql..."
sudo -u "$PG_USER" psql -d "$DB_NAME" -f /tmp/permissions.sql

# --- Limpeza temporária (opcional) ---
echo "🧹 Limpando arquivos temporários..."
rm -f /tmp/DDL.sql /tmp/DML.sql /tmp/permissions.sql

echo ""
echo "🎉 Banco de dados '$DB_NAME' configurado com sucesso!"