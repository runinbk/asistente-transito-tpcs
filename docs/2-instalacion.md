# Guía de Instalación y Configuración

Esta guía detalla los pasos para instalar y configurar correctamente el Asistente de Tránsito.

## Instalación Paso a Paso

### 1. Clonar el Repositorio

```bash
git clone https://github.com/tu-usuario/asistente-transito-tpcs.git
cd asistente-transito-tpcs
```

### 2. Configurar el Entorno Virtual

**En Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**En macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar Dependencias

```bash
pip install -r requirements.txt

# Si encuentras errores relacionados con LangChain, instala adicionalmente:
pip install -U langchain-community
```

### 4. Configurar la Base de Datos PostgreSQL

1. **Instalar PostgreSQL** (si aún no lo tienes)
   - [Descargar e instalar PostgreSQL](https://www.postgresql.org/download/)

2. **Crear la Base de Datos**
   ```sql
   CREATE DATABASE asistente_transito;
   CREATE USER transito_user WITH ENCRYPTED PASSWORD 'tu_contraseña';
   GRANT ALL PRIVILEGES ON DATABASE asistente_transito TO transito_user;
   ```

3. **Crear el archivo .env**
   ```
   POSTGRES_USER=transito_user
   POSTGRES_PASSWORD=tu_contraseña
   POSTGRES_DB=asistente_transito
   POSTGRES_HOST=localhost
   POSTGRES_PORT=5432
   
   OPENAI_API_KEY=tu_clave_api_openai
   ```

### 5. Estructura de Directorios

Asegúrate de crear los siguientes directorios si no existen:

```bash
mkdir -p documents/
mkdir -p faiss_index/
```

## Ejecución de la Aplicación

### 1. Iniciar el Servidor de Desarrollo

```bash
uvicorn app.main:app --reload
```

### 2. Verificar la Instalación

Abre tu navegador y accede a:
- http://127.0.0.1:8000 (mensaje de bienvenida)
- http://127.0.0.1:8000/docs (documentación interactiva Swagger)

## Pruebas Básicas

### 1. Crear una Sesión de Chat

**Usando curl:**
```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/api/chat_sessions' \
  -H 'Content-Type: application/json' \
  -d '{"session_name": "Mi Primera Sesión"}'
```

**Respuesta esperada:**
```json
{
  "id": 1,
  "session_name": "Mi Primera Sesión",
  "created_at": "2025-04-29T12:34:56.789012"
}
```

### 2. Cargar un Documento de Prueba

Crea un archivo de texto de ejemplo `test.txt` con alguna información sobre normativas de tránsito y colócalo en la carpeta `documents/`.

**Usando curl para subir el documento:**
```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/api/documents/upload' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'files=@documents/test.txt'
```

### 3. Enviar un Mensaje al Asistente

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/api/agent/chat/1' \
  -H 'Content-Type: application/json' \
  -d '{
    "session_id": 1,
    "sender": "user",
    "message": "¿Cuáles son las normas básicas de tránsito?"
  }'
```

## Resolución de Problemas Comunes

Si encuentras errores durante la instalación o ejecución, consulta el archivo [TROUBLESHOOTING.md](TROUBLESHOOTING.md) para soluciones a problemas comunes.

## Notas Adicionales

- La primera vez que se ejecute la aplicación, se crearán automáticamente las tablas en la base de datos.
- La carpeta `faiss_index/` se utilizará para almacenar los índices vectoriales de los documentos.
- Si tienes problemas con las dependencias, intenta crear un entorno virtual nuevo y volver a instalar todas las dependencias.