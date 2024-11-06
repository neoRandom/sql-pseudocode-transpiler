CREATE DATABASE code;
USE code;

CREATE TABLE animal (
    cod_animal UNSIGNED INT IDENTITY,
    cod_container UNSIGNED INT,
    cod_veterinario UNSIGNED INT,
    id_classe UNSIGNED INT,
    id_especie UNSIGNED INT,
    nome VARCHAR(64) NOT NULL,
    cor VARCHAR(32) NOT NULL,
    altura DECIMAL(20, 5) NOT NULL,
    peso DECIMAL(20, 5) NOT NULL,
    genero VARCHAR(16) NOT NULL,

    PRIMARY KEY (cod_animal),
    FOREIGN KEY (cod_container) REFERENCES container,
    FOREIGN KEY (cod_veterinario) REFERENCES veterinario,
    FOREIGN KEY (id_classe) REFERENCES classe_animal,
    FOREIGN KEY (id_especie) REFERENCES especie_animal
);

CREATE TABLE classe_animal (
    id_classe UNSIGNED INT IDENTITY,
    descricao VARCHAR(64) NOT NULL,

    PRIMARY KEY (id_classe)
);

CREATE TABLE especie_animal (
    id_especie UNSIGNED INT IDENTITY,
    descricao VARCHAR(64) NOT NULL,

    PRIMARY KEY (id_especie)
);

CREATE TABLE container (
    cod_container UNSIGNED INT IDENTITY,
    id_tipo_container UNSIGNED INT,
    id_ala UNSIGNED INT,
    descricao VARCHAR(64) NOT NULL,
    diagonal DECIMAL(20, 5) NOT NULL,
    area DECIMAL(20, 5) NOT NULL,

    PRIMARY KEY (cod_container),
    FOREIGN KEY (id_tipo_container) REFERENCES tipo_container,
    FOREIGN KEY (id_ala) REFERENCES ala
);

CREATE TABLE tipo_container (
    id_tipo_container UNSIGNED INT IDENTITY,
    descricao VARCHAR(64) NOT NULL,

    PRIMARY KEY (id_tipo_container)
);

CREATE TABLE ala (
    id_ala UNSIGNED INT IDENTITY,
    endereco VARCHAR(128) NOT NULL,
    descricao VARCHAR(64) NOT NULL,

    PRIMARY KEY (id_ala)
);

CREATE TABLE veterinario (
    cod_veterinario UNSIGNED INT IDENTITY,
    cod_funcionario UNSIGNED INT,

    PRIMARY KEY (cod_veterinario),
    FOREIGN KEY (cod_funcionario) REFERENCES funcionario
);

CREATE TABLE consulta (
    cod_consulta UNSIGNED INT IDENTITY,
    cod_animal UNSIGNED INT,
    datahora DATETIME NOT NULL,
    descricao VARCHAR(64) NOT NULL,

    PRIMARY KEY (cod_consulta),
    FOREIGN KEY (cod_animal) REFERENCES animal
);

CREATE TABLE funcionario (
    cod_funcionario UNSIGNED INT IDENTITY,
    id_cargo UNSIGNED INT,
    nome VARCHAR(128) NOT NULL,
    data_nasc DATE NOT NULL,
    cpf VARCHAR(14) NOT NULL,
    rg VARCHAR(12) NOT NULL,
    endereco VARCHAR(128) NOT NULL,
    salario_bonus DECIMAL(20, 5) NOT NULL,

    PRIMARY KEY (cod_funcionario),
    FOREIGN KEY (id_cargo) REFERENCES cargo
);

CREATE TABLE cargo (
    id_cargo UNSIGNED INT IDENTITY,
    descricao VARCHAR(500) NOT NULL,
    salario_base DECIMAL(20, 5) NOT NULL,

    PRIMARY KEY (id_cargo)
);

CREATE TABLE limpeza_ontainer (
    cod_limpeza UNSIGNED INT IDENTITY,
    cod_container UNSIGNED INT,
    cod_funcionario UNSIGNED INT,
    datahora DATETIME NOT NULL,
    descricao VARCHAR(64) NOT NULL,

    PRIMARY KEY (cod_limpeza),
    FOREIGN KEY (cod_container) REFERENCES container,
    FOREIGN KEY (cod_funcionario) REFERENCES funcionario
);
