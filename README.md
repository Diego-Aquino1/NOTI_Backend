# NOTI

## Descripción
NOTI es una aplicación diseñada para notificar a los usuarios sobre cortes de luz en su zona.

## Requisitos Previos
Antes de ejecutar la aplicación, asegúrese de tener instalado:
- Python 3.8 o superior
- PostgreSQL como base de datos
- pip para gestionar paquetes de Python
- uvicorn para ejecutar el servidor ASGI

## Instalación
1. **Clonar el repositorio**
   ```sh
   git clone https://github.com/tu_usuario/noti.git
   cd noti
   ```
2. **Crear un entorno virtual (opcional)**
   ```sh
   python -m venv env
   source env/bin/activate  # En Mac/Linux
   env\Scripts\activate     # En Windows
   ```
3. **Instalar dependencias**
   ```sh
   pip install -r requirements.txt
   ```
4. **Configurar variables de entorno**
   Crear un archivo `.env` en la raíz del proyecto con las credenciales necesarias, por ejemplo:
   ```ini
   DB_USER=tu_usuario
   DB_PASSWORD=tu_contraseña
   DB_NAME=noti_db
   DB_HOST=localhost
   ```

## Ejecución
Para iniciar la aplicación, ejecute el siguiente comando:
```sh
uvicorn main:app --host 0.0.0.0 --port 8000
```
Si está en modo de desarrollo y desea recargar automáticamente los cambios:
```sh
uvicorn main:app --reload
```

## Pruebas y Documentación de Endpoints
Una vez en ejecución, se puede acceder a la documentación interactiva de los endpoints en Swagger UI:
```
http://127.0.0.1:8000/docs
```
O en formato OpenAPI:
```
http://127.0.0.1:8000/redoc
```