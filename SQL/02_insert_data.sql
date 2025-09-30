-- NOTI Database Initial Data
-- Insert initial data for testing and development

-- Insert incident types
INSERT INTO inc_incident_types (name, description) VALUES
('scheduled', 'Corte programado para mantenimiento'),
('incidence', 'Corte por incidencia o falla técnica')
ON CONFLICT (name) DO NOTHING;

-- Insert sample users
INSERT INTO res_users (email, pwd_hash) VALUES
('usuario1@example.com', 'hashedpassword1'),
('usuario2@example.com', 'hashedpassword2'),
('usuario3@example.com', 'hashedpassword3')
ON CONFLICT (email) DO NOTHING;

-- Insert sample user profiles
INSERT INTO res_profiles (user_id, name, phone, address, city, country) VALUES
(1, 'Juan Pérez', '+51123456789', 'Av. Siempre Viva 123', 'Lima', 'Perú'),
(2, 'María López', '+525512345678', 'Calle Falsa 456', 'CDMX', 'México'),
(3, 'Carlos Gómez', '+541123456789', 'Av. Corrientes 789', 'Buenos Aires', 'Argentina')
ON CONFLICT (user_id) DO NOTHING;

-- Insert sample geographic locations
INSERT INTO geo_locations (name, latitude, longitude, region, city, address, country, postal_code) VALUES
('Zona Norte', -12.0464, -77.0428, 'Lima Metropolitana', 'Lima', 'Calle A, Distrito 1', 'Perú', '15001'),
('Centro Histórico', -12.0432, -77.0283, 'Lima Metropolitana', 'Lima', 'Calle B, Distrito 2', 'Perú', '15002'),
('Surquillo', -12.1123, -77.0251, 'Lima Metropolitana', 'Lima', 'Calle C, Distrito 3', 'Perú', '15003')
ON CONFLICT DO NOTHING;

-- Insert sample incidents
INSERT INTO inc_incidents (start_time, end_time, description, type_id, suspendido, url) VALUES
('2025-03-10 08:00:00', '2025-03-10 12:00:00', 'Mantenimiento programado en Zona Norte', 'scheduled', FALSE, 'https://example.com/incident/1'),
('2025-03-11 14:00:00', '2025-03-11 18:00:00', 'Corte inesperado por falla técnica en el Centro Histórico', 'incidence', FALSE, 'https://example.com/incident/2'),
('2025-03-12 09:00:00', '2025-03-12 13:00:00', 'Reparaciones en la red eléctrica en Surquillo', 'scheduled', FALSE, 'https://example.com/incident/3')
ON CONFLICT DO NOTHING;

-- Insert incident addresses (linking incidents to locations)
INSERT INTO inc_incident_addresses (incident_id, location_id) VALUES
(1, 1),
(2, 2),
(3, 3)
ON CONFLICT (incident_id, location_id) DO NOTHING;

-- Insert sample notifications
INSERT INTO not_notification (user_id, incident_id, sent_at, seen) VALUES
(1, 1, '2025-03-09 18:00:00', FALSE),
(2, 2, '2025-03-10 20:00:00', FALSE),
(3, 3, '2025-03-11 21:00:00', TRUE)
ON CONFLICT DO NOTHING;

-- Insert system configuration
INSERT INTO res_config (key, value, description) VALUES
('scraping_enabled', 'true', 'Enable automatic scraping'),
('scraping_interval', '60', 'Scraping interval in minutes'),
('notification_enabled', 'true', 'Enable notifications'),
('maintenance_mode', 'false', 'System maintenance mode')
ON CONFLICT (key) DO NOTHING;
