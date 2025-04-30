# Manual de Uso y Pruebas: API de Asistente de Tránsito

## Índice
1. [Introducción](#introducción)
2. [Requisitos Previos](#requisitos-previos)
3. [Iniciar el Servidor](#iniciar-el-servidor)
4. [Pruebas con Swagger UI](#pruebas-con-swagger-ui)
   - [Gestión de Sesiones de Chat](#gestión-de-sesiones-de-chat)
   - [Carga de Documentos](#carga-de-documentos)
   - [Interacción con el Asistente](#interacción-con-el-asistente)
   - [Consulta de Documentos](#consulta-de-documentos)
5. [Flujo de Trabajo Completo](#flujo-de-trabajo-completo)
6. [Resolución de Problemas](#resolución-de-problemas)

## Introducción

Este manual proporciona instrucciones detalladas para iniciar, configurar y realizar pruebas con la API del Asistente de Tránsito. El sistema permite cargar documentos normativos, indexarlos en un motor de búsqueda vectorial, mantener sesiones de chat y realizar consultas en lenguaje natural sobre la normativa de tránsito.

## Requisitos Previos

Antes de iniciar, asegúrese de tener instalado:

1. Docker y Docker Compose
2. Un archivo `.env` en la raíz del proyecto con las siguientes variables:

```
POSTGRES_USER=normativa_user
POSTGRES_PASSWORD=normativa_pass
POSTGRES_DB=normativa_db
POSTGRES_HOST=db
POSTGRES_PORT=5432
OPENAI_API_KEY=your-openai-api-key-here
```

> **Importante**: Reemplace `your-openai-api-key-here` con su clave API de OpenAI válida.

## Iniciar el Servidor

1. **Inicie los contenedores Docker**:

   ```bash
   docker-compose up -d
   ```

   Este comando iniciará dos contenedores:
   - Base de datos PostgreSQL
   - Servidor API FastAPI

2. **Verifique que los contenedores estén funcionando correctamente**:

   ```bash
   docker-compose ps
   ```

   Debería ver ambos contenedores con el estado "Up".

3. **Acceda a la documentación Swagger UI**:

   Abra su navegador web y visite:
   ```
   http://localhost:8000/docs
   ```

## Pruebas con Swagger UI

### Gestión de Sesiones de Chat

#### 1. Crear una nueva sesión de chat

1. Expanda el endpoint `POST /api/chat_sessions`
2. Haga clic en "Try it out"
3. Ingrese un nombre para la sesión en el cuerpo de la solicitud:
   ```json
   {
     "session_name": "Sesión de prueba"
   }
   ```
4. Haga clic en "Execute"
5. Verifique la respuesta (código 200) y anote el `id` de la sesión para usarlo más adelante

#### 2. Listar todas las sesiones de chat

1. Expanda el endpoint `GET /api/chat_sessions`
2. Haga clic en "Try it out" y luego en "Execute"
3. Verifique que la sesión creada aparezca en la lista

### Carga de Documentos

#### 1. Cargar documentos normativos

1. Expanda el endpoint `POST /api/documents/upload`
2. Haga clic en "Try it out"
3. En el campo `files`, haga clic en "Select files" y seleccione uno o más documentos PDF o TXT con normativa de tránsito
4. Haga clic en "Execute"
5. Verifique la respuesta (código 200) con el mensaje "Documentos cargados exitosamente"

### Interacción con el Asistente

#### 1. Enviar un mensaje al asistente

1. Expanda el endpoint `POST /api/agent/chat/{session_id}`
2. Haga clic en "Try it out"
3. En el campo `session_id`, ingrese el ID de la sesión creada anteriormente
4. En el cuerpo de la solicitud, ingrese:
   ```json
   {
     "session_id": 1,
     "sender": "user",
     "message": "¿Cuál es la velocidad máxima permitida en zona urbana?"
   }
   ```
   > **Nota**: Asegúrese de que el `session_id` en la URL y en el cuerpo coincidan
5. Haga clic en "Execute"
6. Verifique la respuesta del asistente (código 200)

#### 2. Ver el historial de mensajes de una sesión

1. Expanda el endpoint `GET /api/chat_messages/session/{session_id}`
2. Haga clic en "Try it out"
3. En el campo `session_id`, ingrese el ID de la sesión creada anteriormente
4. Haga clic en "Execute"
5. Verifique que aparezca el mensaje enviado y la respuesta del asistente

### Consulta de Documentos

#### 1. Realizar una consulta directa a los documentos

1. Expanda el endpoint `POST /api/documents/query`
2. Haga clic en "Try it out"
3. Complete el formulario:
   - `query`: "velocidad máxima en zona urbana"
   - `top_k`: 3 (número de resultados a devolver)
4. Haga clic en "Execute"
5. Examine los resultados para ver los fragmentos de documentos más relevantes para la consulta

## Flujo de Trabajo Completo

A continuación, se muestra un flujo de trabajo completo para probar el sistema:

1. **Iniciar el servidor** (Docker Compose)
2. **Crear una sesión de chat** (`POST /api/chat_sessions`)
3. **Cargar documentos normativos** (`POST /api/documents/upload`)
4. **Realizar una consulta al asistente** (`POST /api/agent/chat/{session_id}`)
5. **Verificar la respuesta y el historial** (`GET /api/chat_messages/session/{session_id}`)
6. **Realizar consultas adicionales** para probar diferentes aspectos de la normativa
7. **Consultar documentos directamente** para verificar la relevancia (`POST /api/documents/query`)

## Resolución de Problemas

### Error de conexión a la base de datos

Si encuentra errores de conexión a la base de datos:

1. Verifique que los contenedores estén en ejecución:
   ```bash
   docker-compose ps
   ```

2. Verifique los logs del contenedor de la API:
   ```bash
   docker-compose logs -f api
   ```

3. Asegúrese de que las variables de entorno en el archivo `.env` sean correctas

### Error al cargar documentos

Si encuentra errores al cargar documentos:

1. Verifique que los formatos de archivo sean compatibles (PDF, TXT)
2. Asegúrese de que la clave API de OpenAI sea válida
3. Compruebe los logs del servidor para obtener más detalles:
   ```bash
   docker-compose logs -f api
   ```

### Respuestas incorrectas o irrelevantes del asistente

Si el asistente proporciona respuestas incorrectas o irrelevantes:

1. Verifique que los documentos se hayan cargado correctamente
2. Pruebe consultando directamente los documentos para verificar que contienen la información relevante
3. Considere cargar documentos adicionales con información más específica sobre su consulta