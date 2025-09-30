# NOTI Backend - Sistema de Notificaciones de Cortes de Luz

Sistema backend modular para la gestión de notificaciones de cortes de luz eléctrica, organizado en servicios separados con arquitectura de bundle contexts.

## 🚀 Inicio Rápido

```bash
# 1. Clonar el repositorio
git clone <repository-url>
cd NOTI_Backend

# 2. Configurar variables de entorno
cp .env.example .env

# 3. Levantar todos los servicios
docker-compose -f docker-compose.dev.yml up --build -d

# 4. Verificar que todo funciona
curl http://localhost:8000/          # Backend API
curl http://localhost:8001/          # Scraping Service
```

**¡Listo!** El sistema estará funcionando en:
- Backend API: http://localhost:8000
- Scraping Service: http://localhost:8001
- Base de datos: localhost:5432

## 🏗️ Arquitectura

El proyecto está organizado en la siguiente estructura:

```
NOTI_Backend/
├── backend/                    # Servicio principal de API
│   ├── api/                    # Capa de API
│   ├── core/                   # Funcionalidad central
│   ├── bundles/                # Bundle contexts por modelo
│   │   ├── geo_locations/      # Gestión de ubicaciones
│   │   ├── incidents/          # Gestión de incidentes
│   │   ├── notifications/      # Sistema de notificaciones
│   │   ├── users/              # Gestión de usuarios
│   │   ├── profiles/           # Perfiles de usuario
│   │   └── config/             # Configuraciones
│   └── shared/                 # Utilidades del backend
├── scraping/                   # Servicio de scraping
│   ├── api/                    # API del servicio de scraping
│   ├── core/                   # Configuración del scraping
│   ├── services/               # Servicios de scraping
│   └── shared/                 # Utilidades del scraping
├── shared/                     # Código compartido
│   ├── models/                 # Modelos de base de datos
│   ├── database/               # Conexión a BD
│   └── utils/                  # Utilidades compartidas
└── SQL/                        # Scripts de base de datos
```

## 🚀 Servicios

### Backend API (Puerto 8000)
- **API REST** para el frontend
- **Bundle contexts** organizados por modelo
- **Autenticación** y autorización
- **Scheduler** para tareas programadas

### Scraping Service (Puerto 8001)
- **Scraping automático** de datos de cortes
- **API independiente** para control del scraping
- **Integración** con la misma base de datos

## 🐳 Docker

### Desarrollo
```bash
# Levantar todos los servicios en modo desarrollo
docker-compose -f docker-compose.dev.yml up --build

# Levantar en segundo plano
docker-compose -f docker-compose.dev.yml up --build -d

# Solo la base de datos
docker-compose -f docker-compose.dev.yml up postgres

# Ver logs
docker-compose -f docker-compose.dev.yml logs -f

# Ver logs de un servicio específico
docker-compose -f docker-compose.dev.yml logs -f backend
docker-compose -f docker-compose.dev.yml logs -f scraping

# Detener servicios
docker-compose -f docker-compose.dev.yml down
```

### Producción
```bash
# Levantar todos los servicios
docker-compose up --build

# Levantar en segundo plano
docker-compose up --build -d

# Solo servicios específicos
docker-compose up backend postgres

# Ver logs
docker-compose logs -f

# Detener servicios
docker-compose down

# Detener y eliminar volúmenes
docker-compose down -v
```

### Comandos Útiles
```bash
# Acceder al shell de un contenedor
docker-compose -f docker-compose.dev.yml exec backend bash
docker-compose -f docker-compose.dev.yml exec scraping bash
docker-compose -f docker-compose.dev.yml exec postgres psql -U postgres -d noti_db

# Reiniciar un servicio específico
docker-compose -f docker-compose.dev.yml restart backend
docker-compose -f docker-compose.dev.yml restart scraping

# Ver estado de los servicios
docker-compose -f docker-compose.dev.yml ps

# Reconstruir una imagen específica
docker-compose -f docker-compose.dev.yml build backend
docker-compose -f docker-compose.dev.yml build scraping
```

## 🛠️ Configuración

1. Copia el archivo de configuración:
```bash
cp .env.example .env
```

2. Configura las variables de entorno según tu entorno

3. Ejecuta las migraciones de base de datos:
```bash
# Los scripts SQL se ejecutan automáticamente con Docker
```

## 📡 Endpoints

### Backend API
- `GET /` - Health check
- `GET /health` - Estado del servicio
- `GET /api/v1/users/` - Gestión de usuarios
- `GET /api/v1/locations/` - Gestión de ubicaciones
- `GET /api/v1/incidents/` - Gestión de incidentes
- `GET /api/v1/notifications/` - Sistema de notificaciones
- `GET /api/v1/profiles/` - Perfiles de usuario
- `GET /api/v1/config/` - Configuraciones

### Scraping Service
- `GET /` - Health check del scraping
- `POST /trigger` - Ejecutar scraping manualmente

## 🔧 Desarrollo Local

### Requisitos
- Python 3.11+
- PostgreSQL 15+
- Docker y Docker Compose

### Opción 1: Con Docker (Recomendado)
```bash
# Clonar el repositorio
git clone <repository-url>
cd NOTI_Backend

# Configurar variables de entorno
cp .env.example .env

# Levantar todos los servicios
docker-compose -f docker-compose.dev.yml up --build -d

# Ver logs
docker-compose -f docker-compose.dev.yml logs -f
```

### Opción 2: Desarrollo Local
```bash
# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env

# Configurar base de datos PostgreSQL local
# Crear base de datos: noti_db
# Ejecutar scripts SQL en /SQL/

# Ejecutar backend (en una terminal)
python -m backend.api.main

# Ejecutar scraping (en otra terminal)
python -m scraping.api.main
```

## 🗄️ Base de Datos

El sistema utiliza PostgreSQL con los siguientes modelos principales:

- **geo_locations** - Ubicaciones geográficas
- **inc_incidents** - Incidentes de cortes de luz
- **not_notification** - Notificaciones
- **res_users** - Usuarios del sistema
- **res_profiles** - Perfiles de usuario
- **res_config** - Configuraciones del sistema

### Configurar Base de Datos

Si las tablas no existen o necesitas recrear la base de datos:

```bash
# 1. Crear todas las tablas
docker-compose -f docker-compose.dev.yml exec postgres psql -U [usuario_db] -d [nombre_db] -f /docker-entrypoint-initdb.d/01_create_tables.sql

# 2. Insertar datos de prueba
docker-compose -f docker-compose.dev.yml exec postgres psql -U [usuario_db] -d [nombre_db] -f /docker-entrypoint-initdb.d/02_insert_data.sql

# 3. Verificar que se crearon las tablas
docker-compose -f docker-compose.dev.yml exec postgres psql -U [usuario_db] -d [nombre_db] -c "\dt"
```

**Nota**: Los scripts SQL se ejecutan automáticamente al crear la base de datos por primera vez, pero si necesitas recrear las tablas manualmente, usa los comandos de arriba reemplazando `[usuario_db]` y `[nombre_db]` con los valores de tu archivo `.env`.

## 🔄 Bundle Contexts

Cada modelo tiene su propio bundle context que incluye:
- **API** - Endpoints REST
- **Controllers** - Lógica de negocio
- **Models** - Modelos específicos (si aplica)
- **Schemas** - Esquemas de validación
- **Services** - Servicios de dominio

## 📝 Notas de Desarrollo

- Los servicios comparten la misma base de datos
- El scraping se ejecuta automáticamente según el scheduler
- La estructura modular facilita el mantenimiento
- Cada bundle context es independiente y testeable

## 🔧 Troubleshooting

### Problemas Comunes

#### Puerto ocupado
```bash
# Verificar qué está usando el puerto
lsof -i :8000  # Backend
lsof -i :8001  # Scraping
lsof -i :5432  # PostgreSQL

# Cambiar puertos en .env si es necesario
```

#### Limpiar todo y empezar de nuevo
```bash
# Detener y eliminar todo
docker-compose -f docker-compose.dev.yml down -v
docker system prune -f

# Volver a levantar
docker-compose -f docker-compose.dev.yml up --build -d
```

### Logs y Debugging
```bash
# Ver logs de todos los servicios
docker-compose -f docker-compose.dev.yml logs -f

# Ver logs de un servicio específico
docker-compose -f docker-compose.dev.yml logs -f backend
docker-compose -f docker-compose.dev.yml logs -f scraping

# Acceder al shell de un contenedor para debugging
docker-compose -f docker-compose.dev.yml exec backend bash
docker-compose -f docker-compose.dev.yml exec postgres psql -U postgres -d noti_db
```
