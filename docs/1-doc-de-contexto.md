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

---

# **Visión General de la Arquitectura**

Tu objetivo sería construir un sistema con estas *grandes piezas*:

1. **Servidor de orquestación (backend principal)**
   - Será quien maneje: peticiones del cliente móvil, conexión a LLM (OpenAI), contexto, historial, etc.
   - Aquí utilizarás **LangChain** para orquestar (manejar) toda la lógica.

2. **Motor de recuperación de información (RAG)**
   - Sistema que busca información precisa en bases de datos vectoriales (por ejemplo, FAISS, Chroma, o Pinecone).
   - Cuando llega una consulta, en lugar de preguntarle todo a OpenAI directamente, primero recuperas fragmentos relevantes de tus documentos cargados, y luego se los pasas al LLM para que responda.

3. **Base de datos de vectores (Vector Store)**
   - Donde almacenarás tus documentos procesados como vectores.
   - Aquí es donde irán las leyes de tránsito, manuales, documentos, etc.
   - Puede ser local (FAISS, Chroma) o en la nube (Pinecone, Weaviate).

4. **Manejador de contexto e historial de conversación**
   - Para que tu asistente sepa de qué se habló antes.
   - Puedes usar herramientas como **LangChain Memory** (`ConversationBufferMemory`, `ConversationSummaryMemory`, etc.).
   - Esto permitirá mantener el "hilo" de la conversación.

5. **Sistema de sinónimos / Diccionario personalizado**
   - Necesitas interceptar o preprocesar las consultas del usuario para reemplazar o mapear términos.
   - Se puede hacer como:
     - Preprocesamiento del input del usuario antes de mandarlo al LLM.
     - O enriquecer tu base de datos de vectores agregando las variantes semánticas.

6. **Conexión a LLM**
   - Te conectarás a OpenAI, Anthropic, u otro modelo vía API.
   - Pero tu servidor es el que controla qué le mandas al modelo, incluyendo los documentos encontrados + contexto de conversación.

7. **Aplicación móvil (Frontend)**
   - Que consume tu API/servidor.
   - Aquí te puedes despreocupar un rato, lo principal ahora es levantar el servidor.

---

# **Flujo de Operación (Simplificado)**

1. El usuario envía una consulta por la app móvil.
2. El servidor la recibe.
3. Se aplica normalización: diccionario de sinónimos.
4. El servidor consulta el **vector store** para recuperar documentos relevantes (RAG).
5. Combina los documentos + historial de conversación.
6. Envía todo eso al **LLM** (OpenAI API).
7. Recibe la respuesta del modelo.
8. Se guarda el nuevo fragmento en el historial/contexto.
9. Se devuelve la respuesta al usuario.

---

# **Tecnologías y Herramientas que podrías usar**

| Componente | Opción recomendada |
|------------|--------------------|
| **Framework Backend** | FastAPI (Python) |
| **Orquestador LLM** | LangChain |
| **Vector Store** | Chroma o FAISS (local) |
| **Base de Datos "normal"** | PostgreSQL para usuarios, historial |
| **Memory Manager** | LangChain Memory |
| **Motor de sinónimos** | Diccionario interno + fuzzy matching ó OpenAI Embeddings |
| **Modelo LLM** | OpenAI (gpt-3.5, gpt-4) |

---

# **Diagrama rápido (mental)**

```
App Móvil ---> API Servidor
               |
          [LangChain]
               |
  +------------------------------+
  |  Contexto Memoria Historial   |
  |  Recuperador Vectorial (RAG)  |
  |  Sinónimos / Normalizador     |
  |  Conexión LLM (OpenAI API)    |
  +------------------------------+
```

---
