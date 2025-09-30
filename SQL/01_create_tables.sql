-- NOTI Database Schema
-- Create all tables for the NOTI system

-- Users table
CREATE TABLE IF NOT EXISTS res_users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(100) UNIQUE NOT NULL,
    pwd_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- User profiles table
CREATE TABLE IF NOT EXISTS res_profiles (
    id SERIAL PRIMARY KEY,
    user_id INT UNIQUE REFERENCES res_users(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    address TEXT,
    city VARCHAR(100),
    country VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Geographic locations table
CREATE TABLE IF NOT EXISTS geo_locations (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    latitude DECIMAL(10, 8) NOT NULL,
    longitude DECIMAL(11, 8) NOT NULL,
    region VARCHAR(100),
    city VARCHAR(100),
    address VARCHAR(180),
    country VARCHAR(100),
    postal_code VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Incident types table
CREATE TABLE IF NOT EXISTS inc_incident_types (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Incidents table
CREATE TABLE IF NOT EXISTS inc_incidents (
    id SERIAL PRIMARY KEY,
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP NOT NULL,
    description TEXT,
    type_id VARCHAR(100) NOT NULL,
    suspendido BOOLEAN DEFAULT FALSE,
    url TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Incident addresses table (many-to-many relationship)
CREATE TABLE IF NOT EXISTS inc_incident_addresses (
    id SERIAL PRIMARY KEY,
    incident_id INT NOT NULL REFERENCES inc_incidents(id) ON DELETE CASCADE,
    location_id INT NOT NULL REFERENCES geo_locations(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(incident_id, location_id)
);

-- Notifications table
CREATE TABLE IF NOT EXISTS not_notification (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL REFERENCES res_users(id) ON DELETE CASCADE,
    incident_id INT NOT NULL REFERENCES inc_incidents(id) ON DELETE CASCADE,
    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    seen BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Configuration table
CREATE TABLE IF NOT EXISTS res_config (
    id SERIAL PRIMARY KEY,
    key VARCHAR(100) UNIQUE NOT NULL,
    value TEXT,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_geo_locations_coordinates ON geo_locations(latitude, longitude);
CREATE INDEX IF NOT EXISTS idx_inc_incidents_time ON inc_incidents(start_time, end_time);
CREATE INDEX IF NOT EXISTS idx_inc_incidents_type ON inc_incidents(type_id);
CREATE INDEX IF NOT EXISTS idx_not_notification_user ON not_notification(user_id);
CREATE INDEX IF NOT EXISTS idx_not_notification_incident ON not_notification(incident_id);
CREATE INDEX IF NOT EXISTS idx_inc_incident_addresses_incident ON inc_incident_addresses(incident_id);
CREATE INDEX IF NOT EXISTS idx_inc_incident_addresses_location ON inc_incident_addresses(location_id);
