# Asistente de Tránsito - API

Sistema de asistente virtual especializado en normativas de tránsito con capacidad de búsqueda semántica en documentos normativos.

## 📋 Descripción

Este proyecto implementa una API REST en FastAPI que permite:
- Cargar documentos normativos (PDF, TXT)
- Indexarlos en un motor de búsqueda vectorial (FAISS)
- Realizar búsquedas semánticas en lenguaje natural
- Mantener sesiones de chat con historial de preguntas y respuestas
- Utilizar un asistente IA basado en LangChain y OpenAI para responder consultas

El sistema está diseñado para funcionar como backend de una aplicación de asistencia en temas normativos de tránsito, permitiendo a los usuarios hacer preguntas en lenguaje natural y recibir respuestas precisas basadas en la documentación oficial.

## 🚀 Tecnologías

- **FastAPI**: Framework web para la API
- **Uvicorn**: Servidor ASGI
- **PostgreSQL**: Base de datos relacional
- **SQLAlchemy**: ORM para la conexión a PostgreSQL
- **LangChain**: Framework para aplicaciones con LLMs
- **OpenAI**: Proveedor de modelos de lenguaje
- **FAISS**: Biblioteca para búsqueda de similitud vectorial
- **PyMuPDF/PyPDF2**: Procesamiento de documentos PDF

## 📁 Estructura del Proyecto

```
/
├── app/
│   ├── db/
│   │   └── database.py         # Configuración de la base de datos
│   ├── models/
│   │   ├── chat_message.py     # Modelo de mensaje de chat
│   │   └── chat_session.py     # Modelo de sesión de chat
│   ├── routes/
│   │   ├── agent_chat.py       # Endpoints para el chat con IA
│   │   ├── chat.py             # Endpoints para sesiones de chat
│   │   ├── chat_message.py     # Endpoints para mensajes
│   │   ├── document.py         # Endpoints para gestión de documentos
│   │   └── message.py          # Endpoints adicionales para mensajes
│   ├── schemas/
│   │   ├── chat_message.py     # Esquemas Pydantic para mensajes
│   │   ├── chat_session.py     # Esquemas Pydantic para sesiones
│   │   └── message.py          # Esquemas adicionales para mensajes
│   ├── services/
│   │   ├── agent.py            # Servicio del asistente IA
│   │   ├── chat_message_service.py  # Servicio para mensajes
│   │   ├── chat_retrieval_service.py  # Servicio para búsqueda
│   │   ├── chat_session_service.py  # Servicio para sesiones
│   │   ├── document_loader.py  # Servicio para cargar documentos
│   │   └── message_service.py  # Servicio adicional para mensajes
│   ├── utils/
│   │   └── vector_store.py     # Utilidades para almacén vectorial
│   └── main.py                 # Punto de entrada de la aplicación
├── documents/                  # Carpeta para almacenar documentos
├── .env                        # Variables de entorno (no incluido en git)
└── requirements.txt            # Dependencias del proyecto
```

## ⚙️ Requisitos

- Python 3.9+
- PostgreSQL
- Clave API de OpenAI

## 🔧 Instalación

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/tu-usuario/asistente-transito-tpcs.git
   cd asistente-transito-tpcs
   ```

2. **Crear entorno virtual**
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar variables de entorno**
   
   Crea un archivo `.env` en la raíz del proyecto con el siguiente contenido:
   ```
   POSTGRES_USER=tu_usuario
   POSTGRES_PASSWORD=tu_contraseña
   POSTGRES_DB=asistente_transito
   POSTGRES_HOST=localhost
   POSTGRES_PORT=5432
   
   OPENAI_API_KEY=tu_clave_api_openai
   ```

5. **Iniciar la base de datos**
   
   Asegúrate de tener PostgreSQL corriendo y haber creado la base de datos configurada en `.env`.

## 🚀 Ejecución

**Iniciar el servidor de desarrollo**
```bash
uvicorn app.main:app --reload
```

El servidor estará disponible en `http://127.0.0.1:8000`

**Documentación de la API**
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## 🔄 Flujo de Funcionamiento

1. **Carga de documentos**
   - Sube documentos normativos a través del endpoint `/api/documents/upload`
   - Los documentos se procesan, dividen en chunks y se indexan en FAISS

2. **Creación de sesiones**
   - Crea una sesión de chat con el endpoint `/api/chat_sessions`

3. **Interacción con el asistente**
   - Envía mensajes al asistente con el endpoint `/api/agent/chat/{session_id}`
   - El sistema busca documentos relevantes usando embeddings
   - Combina los documentos con el historial de conversación
   - El modelo LLM genera una respuesta contextualizada
   - La respuesta se guarda y se devuelve al usuario

## 📝 Características Principales

- **Búsqueda semántica**: Encuentra información relevante incluso cuando las consultas no contienen las palabras exactas.
- **Memoria de conversación**: El asistente mantiene el contexto de la conversación.
- **Preprocesamiento de consultas**: Sistema de sinónimos para mapear términos coloquiales a técnicos.
- **Procesamiento de documentos**: Soporte para PDF y documentos de texto plano.

## 🧪 Pruebas

Para probar la API usando curl:

**Crear una sesión de chat**
```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/api/chat_sessions' \
  -H 'Content-Type: application/json' \
  -d '{"session_name": "Consulta sobre límites de velocidad"}'
```

**Enviar un mensaje al asistente**
```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/api/agent/chat/1' \
  -H 'Content-Type: application/json' \
  -d '{"session_id": 1, "sender": "user", "message": "¿Cuál es el límite de velocidad en zonas urbanas?"}'
```

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue para discutir cambios importantes antes de enviar un pull request.

## 📄 Licencia

[MIT](LICENSE)