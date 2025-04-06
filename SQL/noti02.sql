CREATE TABLE res_users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(100) UNIQUE NOT NULL,
    pwd_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE res_profiles (
    id SERIAL PRIMARY KEY,
    user_id INT UNIQUE REFERENCES res_users(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    address TEXT,
    city VARCHAR(100),
    country VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE geo_locations (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    latitude DECIMAL(9,6) NOT NULL,
    longitude DECIMAL(9,6) NOT NULL,
    region VARCHAR(100),
    city VARCHAR(100),
    address VARCHAR(180),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    country VARCHAR(100),
    postal_code VARCHAR(100)
);

CREATE TABLE inc_incident_types (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE inc_incidents (
    id SERIAL PRIMARY KEY,
    location_id INT REFERENCES geo_locations(id) ON DELETE CASCADE,
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP NOT NULL,
    description TEXT,
    type_id INT REFERENCES inc_incident_types(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE not_notifications (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES res_users(id) ON DELETE CASCADE,
    incident_id INT REFERENCES inc_incidents(id) ON DELETE CASCADE,
    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    seen BOOLEAN DEFAULT FALSE
);

CREATE TABLE res_config (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES res_users(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    priority INT DEFAULT 5,
    interval INT DEFAULT 7
);