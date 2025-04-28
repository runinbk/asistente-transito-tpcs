# 📄 Proyecto: API de Búsqueda y Chat sobre Documentos Normativos

## 1. 🎯 Objetivo del Proyecto

Desarrollar una **API en FastAPI** que permita:

- Cargar documentos normativos.
- Indexarlos en un motor de búsqueda vectorial.
- Realizar búsquedas semánticas en lenguaje natural.
- Mantener sesiones de chat (historial de preguntas y respuestas).

Todo el sistema deberá ser **online** (por ahora), y deberá ser **fácilmente portable a contenedores** mediante Docker.

---

## 2. 🛠 Tecnologías utilizadas

| Tecnología | Uso |
|:-----------|:----|
| FastAPI | Framework web para la API |
| Uvicorn | Servidor ASGI para correr FastAPI |
| PostgreSQL (en Docker) | Base de datos principal |
| SQLAlchemy | ORM para la conexión a PostgreSQL |
| psycopg2-binary | Driver de PostgreSQL |
| Docker | Contenerización de servicios |
| Docker Compose | Orquestar la API y la base de datos |
| OpenAI Embeddings o Sentence Transformers | Generación de embeddings para búsquedas semánticas |
| FAISS | Motor de búsqueda vectorial |
| Python-dotenv | Manejo de variables de entorno (.env) |

---

## 3. 📁 Estructura de Carpetas del Proyecto

```plaintext
/backend
│
├── app/
│   ├── __init__.py
│   ├── main.py          # Arranca FastAPI
│   ├── routes/
│   │   └── chat.py      # Endpoints de la API
│   ├── services/
│   │   ├── agent.py     # Módulo para manejar conversaciones (IA, lógica de contexto)
│   │   ├── document_loader.py  # Carga y preprocesamiento de documentos
│   ├── models/
│   │   └── chat_session.py   # Modelos de SQLAlchemy para sesiones de chat
│   ├── db/
│   │   └── database.py  # Conexión y gestión de base de datos PostgreSQL
│   └── utils/
│       └── vector_store.py   # Utilidades para almacenar y consultar embeddings (FAISS)
│
├── .env                 # Variables de entorno (nunca versionar directamente)
├── requirements.txt     # Librerías necesarias del proyecto
├── Dockerfile           # Imagen de Docker para la API
├── docker-compose.yml   # Orquestación de servicios Docker (API + PostgreSQL)
└── README.md            # Documentación general del proyecto
```

---

## 4. 📦 Contenedores Docker a utilizar

Inicialmente:
- **PostgreSQL** (contenedor para la base de datos)
- **API de FastAPI** (contenedor que levanta la aplicación)

En el futuro se puede agregar:
- Un contenedor separado para FAISS (si se desea escalar el motor vectorial)

---

## 5. 🌐 Variables de entorno `.env`

Estas serán las principales (ejemplo):

```bash
POSTGRES_USER=normativa_user
POSTGRES_PASSWORD=normativa_pass
POSTGRES_DB=normativa_db
POSTGRES_HOST=db
POSTGRES_PORT=5432

OPENAI_API_KEY=your-openai-api-key-here

# Otros parámetros que necesitemos
```

---

## 6. 🚀 Librerías confirmadas en `requirements.txt`

```plaintext
fastapi
uvicorn[standard]
psycopg2-binary
sqlalchemy
python-dotenv
openai
sentence-transformers
faiss-cpu
```

*Nota: Se puede ajustar si en el futuro decidimos usar solo OpenAI o solo Sentence Transformers.*

---

## 7. 📝 Notas importantes

- Se trabajará **100% online** en esta primera versión.
- El contexto y estructura **NO deben cambiar** una vez definidos.
- El motor de embeddings puede ser **OpenAI o Sentence Transformers**, según facilidad y velocidad de implementación para la demo.
- **FAISS** será el motor vectorial base para almacenar y buscar embeddings.
- **PostgreSQL** será nuestra base de datos principal (manejado en contenedor Docker).

---

# 📍 Resumen Final

**Esta es la única estructura, tecnologías y enfoque que seguiremos hasta terminar esta primera versión.**  
Todo cambio posterior debe ser previamente discutido.

