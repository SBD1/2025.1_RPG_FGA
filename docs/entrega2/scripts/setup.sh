#!/bin/bash

# --- Configuração ---
# O nome de usuário do banco de dados e o nome do banco de dados
PG_USER="postgres" # Superusuário do PostgreSQL para a criação inicial
DB_NAME="rpg_fga"
APP_USER="estudante"

# --- Lógica do Script ---

# Para o script se encontrar um erro
set -e

# Detecta o diretório onde o script está localizado. Isso torna os caminhos dinâmicos.
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

echo "Diretório dos scripts detectado: $SCRIPT_DIR"
echo "--- Iniciando configuração do banco de dados: $DB_NAME ---"

# Passo 1: Recria o banco de dados. Usa 'sudo' para rodar como o usuário postgres.
sudo -u "$PG_USER" psql -d postgres -c "DROP DATABASE IF EXISTS $DB_NAME;"
sudo -u "$PG_USER" psql -d postgres -c "CREATE DATABASE $DB_NAME;"

echo "✅ Banco de dados '$DB_NAME' criado."

# Passo 2: Executa os scripts SQL no banco de dados recém-criado.
echo "-> Criando o usuário '$APP_USER' e concedendo permissões..."
sudo -u "$PG_USER" psql -d "$DB_NAME" <<-EOSQL
    DO \$\$
    BEGIN
        IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = '$APP_USER') THEN
            CREATE USER $APP_USER WITH PASSWORD '123';
        END IF;
    END
    \$\$;
    ALTER USER $APP_USER WITH SUPERUSER;
EOSQL

echo "-> Executando DDL para criar a estrutura do banco..."
sudo -u "$PG_USER" psql -d "$DB_NAME" -f "$SCRIPT_DIR/DDL.sql"

echo "-> Executando DML para popular o banco de dados..."
sudo -u "$PG_USER" psql -d "$DB_NAME" -f "$SCRIPT_DIR/DML.sql"

echo "-> Configurando permissões..."
sudo -u "$PG_USER" psql -d "$DB_NAME" -f "$SCRIPT_DIR/permissions.sql"

echo ""
echo "🎉 Configuração do banco de dados concluída com sucesso!"