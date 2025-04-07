CREATE TABLE continent (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR,
    code VARCHAR,
    population BIGINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by VARCHAR DEFAULT 'system',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_by VARCHAR DEFAULT 'system',
    deleted_at TIMESTAMP,
    deleted_by VARCHAR,
    is_deleted BOOLEAN DEFAULT FALSE
);

CREATE INDEX ix_continent_id ON continent(id);

CREATE TABLE epidemic (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    type VARCHAR NOT NULL,
    pathogen_name VARCHAR NOT NULL,
    description VARCHAR,
    transmission_mode VARCHAR,
    symptoms VARCHAR,
    reproduction_rate FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by VARCHAR DEFAULT 'system',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_by VARCHAR DEFAULT 'system',
    deleted_at TIMESTAMP,
    deleted_by VARCHAR,
    is_deleted BOOLEAN DEFAULT FALSE
);

CREATE INDEX ix_epidemic_id ON epidemic(id);

CREATE TABLE role (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(50),
    description VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by VARCHAR DEFAULT 'system',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_by VARCHAR DEFAULT 'system',
    deleted_at TIMESTAMP,
    deleted_by VARCHAR,
    is_deleted BOOLEAN DEFAULT FALSE
);

CREATE INDEX ix_role_id ON role(id);

CREATE TABLE "user" (
    id BIGSERIAL PRIMARY KEY,
    firstname VARCHAR(50),
    lastname VARCHAR(50),
    username VARCHAR(50),
    email VARCHAR(100) UNIQUE,
    password VARCHAR(100),
    gender VARCHAR(10),
    birthdate VARCHAR(10),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by VARCHAR DEFAULT 'system',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_by VARCHAR DEFAULT 'system',
    deleted_at TIMESTAMP,
    deleted_by VARCHAR,
    is_deleted BOOLEAN DEFAULT FALSE
);

CREATE INDEX ix_user_id ON "user"(id);

CREATE TABLE country (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR,
    iso2 VARCHAR,
    iso3 VARCHAR,
    population BIGINT,
    continent_id BIGINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by VARCHAR DEFAULT 'system',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_by VARCHAR DEFAULT 'system',
    deleted_at TIMESTAMP,
    deleted_by VARCHAR,
    is_deleted BOOLEAN DEFAULT FALSE,
    CONSTRAINT fk_country_continent FOREIGN KEY (continent_id) REFERENCES continent(id)
);

CREATE INDEX ix_country_id ON country(id);

CREATE TABLE user_role (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT,
    role_id BIGINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by VARCHAR DEFAULT 'system',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_by VARCHAR DEFAULT 'system',
    deleted_at TIMESTAMP,
    deleted_by VARCHAR,
    is_deleted BOOLEAN DEFAULT FALSE,
    CONSTRAINT fk_userrole_user FOREIGN KEY (user_id) REFERENCES "user"(id),
    CONSTRAINT fk_userrole_role FOREIGN KEY (role_id) REFERENCES role(id)
);

CREATE INDEX ix_user_role_id ON user_role(id);

CREATE TABLE vaccine (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR,
    laboratory VARCHAR,
    technology VARCHAR,
    dose VARCHAR,
    efficacy FLOAT,
    storage_temperature VARCHAR,
    epidemic_id BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by VARCHAR DEFAULT 'system',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_by VARCHAR DEFAULT 'system',
    deleted_at TIMESTAMP,
    deleted_by VARCHAR,
    is_deleted BOOLEAN DEFAULT FALSE,
    CONSTRAINT fk_vaccine_epidemic FOREIGN KEY (epidemic_id) REFERENCES epidemic(id)
);

CREATE INDEX ix_vaccine_id ON vaccine(id);

CREATE TABLE daily_wise (
    id BIGSERIAL PRIMARY KEY,
    date TIMESTAMP NOT NULL,
    province VARCHAR,
    latitude FLOAT,
    longitude FLOAT,
    country_id BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by VARCHAR DEFAULT 'system',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_by VARCHAR DEFAULT 'system',
    deleted_at TIMESTAMP,
    deleted_by VARCHAR,
    is_deleted BOOLEAN DEFAULT FALSE,
    CONSTRAINT fk_dailywise_country FOREIGN KEY (country_id) REFERENCES country(id)
);

CREATE INDEX ix_daily_wise_id ON daily_wise(id);

CREATE TABLE daily_wise_vaccine (
    id BIGSERIAL PRIMARY KEY,
    daily_wise_id BIGINT,
    vaccine_id BIGINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by VARCHAR DEFAULT 'system',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_by VARCHAR DEFAULT 'system',
    deleted_at TIMESTAMP,
    deleted_by VARCHAR,
    is_deleted BOOLEAN DEFAULT FALSE,
    CONSTRAINT fk_dailywisevaccine_dailywise FOREIGN KEY (daily_wise_id) REFERENCES daily_wise(id),
    CONSTRAINT fk_dailywisevaccine_vaccine FOREIGN KEY (vaccine_id) REFERENCES vaccine(id)
);

CREATE INDEX ix_daily_wise_vaccine_id ON daily_wise_vaccine(id);

CREATE TABLE statistic (
    id BIGSERIAL PRIMARY KEY,
    label VARCHAR,
    value FLOAT,
    published_at VARCHAR,
    published_by VARCHAR,
    country_id BIGINT NOT NULL,
    epidemic_id BIGINT NOT NULL,
    daily_wise_id BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by VARCHAR DEFAULT 'system',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_by VARCHAR DEFAULT 'system',
    deleted_at TIMESTAMP,
    deleted_by VARCHAR,
    is_deleted BOOLEAN DEFAULT FALSE,
    CONSTRAINT fk_statistic_country FOREIGN KEY (country_id) REFERENCES country(id),
    CONSTRAINT fk_statistic_epidemic FOREIGN KEY (epidemic_id) REFERENCES epidemic(id),
    CONSTRAINT fk_statistic_dailywise FOREIGN KEY (daily_wise_id) REFERENCES daily_wise(id)
);

CREATE INDEX ix_statistic_id ON statistic(id);
