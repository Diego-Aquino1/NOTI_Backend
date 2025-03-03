INSERT INTO res_users (email, pwd_hash) VALUES
('usuario1@example.com', 'hashedpassword1'),
('usuario2@example.com', 'hashedpassword2'),
('usuario3@example.com', 'hashedpassword3');

INSERT INTO res_profiles (user_id, name, phone, address, city, country) VALUES
(1, 'Juan Pérez', '+51123456789', 'Av. Siempre Viva 123', 'Lima', 'Perú'),
(2, 'María López', '+525512345678', 'Calle Falsa 456', 'CDMX', 'México'),
(3, 'Carlos Gómez', '+541123456789', 'Av. Corrientes 789', 'Buenos Aires', 'Argentina');

INSERT INTO geo_locations (name, latitude, longitude, region, city, address) VALUES
('Zona Norte', -12.0464, -77.0428, 'Lima Metropolitana', 'Lima', 'Calle A, Distrito 1'),
('Centro Histórico', -12.0432, -77.0283, 'Lima Metropolitana', 'Lima', 'Calle B, Distrito 2'),
('Surquillo', -12.1123, -77.0251, 'Lima Metropolitana', 'Lima', 'Calle C, Distrito 3');

INSERT INTO inc_incident_types (name) VALUES
('scheduled'),
('incidence');

INSERT INTO inc_incidents (location_id, start_time, end_time, description, type_id) VALUES
(1, '2025-03-10 08:00:00', '2025-03-10 12:00:00', 'Mantenimiento programado en Zona Norte', 1),
(2, '2025-03-11 14:00:00', '2025-03-11 18:00:00', 'Corte inesperado por falla técnica en el Centro Histórico', 2),
(3, '2025-03-12 09:00:00', '2025-03-12 13:00:00', 'Reparaciones en la red eléctrica en Surquillo', 1);

INSERT INTO not_notifications (user_id, incident_id, sent_at, seen) VALUES
(1, 1, '2025-03-09 18:00:00', FALSE),
(2, 2, '2025-03-10 20:00:00', FALSE),
(3, 3, '2025-03-11 21:00:00', TRUE);
