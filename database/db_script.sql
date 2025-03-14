/* db_logic: */

CREATE TABLE tb_users (
    id_email VARCHAR(100) NOT NULL UNIQUE,
    id_cpf VARCHAR(11) NOT NULL UNIQUE,
    dt_birthdate DATE NOT NULL,
    nm_first_name VARCHAR(100) NOT NULL,
    nm_last_name VARCHAR(200) NOT NULL,
    id SERIAL PRIMARY KEY NOT NULL,
    ts_created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ts_updated_at TIMESTAMP,
    ds_password VARCHAR(100) NOT NULL
);

CREATE TABLE tb_transactions (
    dt_transaction DATE NOT NULL DEFAULT CURRENT_DATE,
    ds_description VARCHAR(200),
    ds_title VARCHAR(100) NOT NULL,
    vl_transaction DECIMAL(10, 2) NOT NULL,
    id SERIAL PRIMARY KEY NOT NULL,
    ts_created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ts_updated_at TIMESTAMP,
    fk_tb_transaction_categories_id INTEGER NOT NULL,
    fk_tb_users_id INTEGER NOT NULL,
    fk_tb_transaction_types_id INTEGER NOT NULL,
    fk_tb_currencies_id INTEGER NOT NULL
);

CREATE TABLE tb_transaction_categories (
    id SERIAL PRIMARY KEY NOT NULL,
    ds_title VARCHAR(100) NOT NULL,
    ds_description VARCHAR(200),
    ts_created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ts_updated_at TIMESTAMP,
    fk_tb_users_id INTEGER NOT NULL
);

CREATE TABLE tb_transaction_types (
    id SERIAL PRIMARY KEY NOT NULL,
    ds_title VARCHAR(100) UNIQUE NOT NULL,
    ts_created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ts_updated_at TIMESTAMP
);

CREATE TABLE tb_currencies (
    id SERIAL PRIMARY KEY NOT NULL,
    ds_title VARCHAR(100) UNIQUE NOT NULL,
    cd_iso VARCHAR(3) UNIQUE NOT NULL,
    ts_created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ts_updated_at TIMESTAMP
);

CREATE TABLE tb_goals (
    id SERIAL PRIMARY KEY NOT NULL,
    ds_title VARCHAR(100) NOT NULL,
    dt_end DATE NOT NULL,
    vl_goal DECIMAL(10, 2) NOT NULL,
    fk_tb_users_id INTEGER NOT NULL,
    ts_created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ts_updated_at TIMESTAMP
);
 
ALTER TABLE tb_transactions ADD CONSTRAINT FK_tb_transactions_2
    FOREIGN KEY (fk_tb_transaction_categories_id)
    REFERENCES tb_transaction_categories (id)
    ON DELETE CASCADE;
 
ALTER TABLE tb_transactions ADD CONSTRAINT FK_tb_transactions_3
    FOREIGN KEY (fk_tb_users_id)
    REFERENCES tb_users (id)
    ON DELETE CASCADE;

ALTER TABLE tb_transactions ADD CONSTRAINT FK_tb_transactions_4
    FOREIGN KEY (fk_tb_transaction_types_id)
    REFERENCES tb_transaction_types (id);
 
ALTER TABLE tb_transactions ADD CONSTRAINT FK_tb_transactions_5
    FOREIGN KEY (fk_tb_currencies_id)
    REFERENCES tb_currencies (id);
 
ALTER TABLE tb_transaction_categories ADD CONSTRAINT FK_tb_transaction_categories_2
    FOREIGN KEY (fk_tb_users_id)
    REFERENCES tb_users (id)
    ON DELETE CASCADE;

ALTER TABLE tb_goals ADD CONSTRAINT FK_tb_goals_2
    FOREIGN KEY (fk_tb_users_id)
    REFERENCES tb_users (id)
    ON DELETE CASCADE;