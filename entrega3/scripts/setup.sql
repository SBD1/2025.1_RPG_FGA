-- Criação do banco e usuário básico

DROP DATABASE IF EXISTS rpg_fga;
CREATE DATABASE rpg_fga;

-- Conecta ao banco criado
\c rpg_fga

-- Cria usuário se não existir
DO $$
BEGIN
    IF EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'estudante') THEN
        RAISE NOTICE 'Usuário estudante já existe';
    ELSE
        CREATE USER estudante WITH PASSWORD '123';
    END IF;
END
$$;

-- -- -- Executa os scripts na ordem correta
-- \i 2025.1_RPG_FGA/entrega2/scripts/DDL.sql
-- \i 2025.1_RPG_FGA/entrega2/scripts/DML.sql
-- \i 2025.1_RPG_FGA/entrega2/scripts/permissions.sql
-- nao consegui fazer isso dar certo, tem q faze manualmente