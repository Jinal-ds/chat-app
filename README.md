# 💬 Chat App

A full-stack real-time chat application built with **FastAPI**, **MongoDB**, **Docker**, and **Streamlit**. Features complete user authentication with JWT tokens, chat room management, and messaging.

## 🌍 Live Demo

| Service | URL |
|---|---|
| 🎨 Frontend (Streamlit) | https://chat-app-frontend-gjpu.onrender.com |
| ⚡ Backend API Docs | https://chat-app-production-25d6.up.railway.app/docs |

---

## ✨ Features

- 🔐 **User Authentication** — Register and login with JWT tokens
- 💬 **Chat Rooms** — Create and browse chat rooms
- 📨 **Messaging** — Send and delete messages in real time
- 🔒 **Protected Routes** — All chat features require authentication
- 🌐 **CORS Ready** — Frontend and backend run as separate services
- 🐳 **Fully Dockerized** — Runs anywhere with one command
- 🚀 **CI/CD Pipeline** — Auto deploys on every GitHub push

---

## 🛠️ Tech Stack

### Backend
| Technology | Purpose |
|---|---|
| **FastAPI** | Web framework — routing, validation, auto docs |
| **MongoDB** | NoSQL database — stores users, rooms, messages |
| **Beanie** | MongoDB ODM — Python class to collection mapping |
| **Motor** | Async MongoDB driver |
| **python-jose** | JWT token creation and verification |
| **bcrypt** | Secure password hashing |
| **Pydantic** | Data validation using Python type hints |
| **Uvicorn** | ASGI server |

### Frontend
| Technology | Purpose |
|---|---|
| **Streamlit** | Python-based web UI |
| **Requests** | HTTP calls to FastAPI backend |

### DevOps
| Technology | Purpose |
|---|---|
| **Docker** | Containerization |
| **Docker Compose** | Multi-container orchestration |
| **Railway** | Backend + MongoDB cloud deployment |
| **Render** | Frontend cloud deployment |
| **GitHub** | Version control + CI/CD trigger |

---

## 📁 Project Structure

```
chat-app/
├── docker-compose.yml          ← runs all containers together
├── .gitignore
├── README.md
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── main.py                 ← app entry, middleware, routers
│   ├── database.py             ← MongoDB connection
│   ├── config.py               ← environment variables
│   ├── dependencies.py         ← JWT auth, password hashing
│   ├── models/
│   │   ├── user.py             ← User document + schemas
│   │   ├── room.py             ← Room document + schemas
│   │   └── message.py          ← Message document + schemas
│   └── routers/
│       ├── auth.py             ← POST /auth/register, /auth/login
│       ├── rooms.py            ← GET/POST/DELETE /rooms
│       └── messages.py         ← GET/POST/DELETE /rooms/{id}/messages
└── frontend/
    ├── Dockerfile
    ├── requirements.txt
    └── app.py                  ← Streamlit UI (3 pages)
```

---

## 🚀 Run Locally with Docker

### Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running
- [Git](https://git-scm.com/) installed

### Steps

```bash
# 1. Clone the repository
git clone https://github.com/Jinal-ds/chat-app.git
cd chat-app

# 2. Run everything with one command
docker-compose up --build
```

That's it! Open:
- 🎨 **Frontend** → http://localhost:8501
- ⚡ **API Docs** → http://localhost:8000/docs

### Stop the app
```bash
docker-compose down
```

---

## 🔧 Run Locally without Docker

### Prerequisites
- Python 3.11+
- MongoDB running locally on port 27017

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend

```bash
cd frontend
pip install -r requirements.txt
streamlit run app.py
```

---

## 🔌 API Endpoints

### Auth
| Method | Endpoint | Auth | Description |
|---|---|---|---|
| POST | `/auth/register` | No | Create new account |
| POST | `/auth/login` | No | Login and get JWT token |

### Rooms
| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/rooms/` | Yes | List all rooms |
| POST | `/rooms/` | Yes | Create a new room |
| DELETE | `/rooms/{room_id}` | Yes (owner) | Delete a room |

### Messages
| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/rooms/{room_id}/messages` | Yes | Get messages in a room |
| POST | `/rooms/{room_id}/messages` | Yes | Send a message |
| DELETE | `/rooms/{room_id}/messages/{message_id}` | Yes (sender) | Delete a message |

---

## 🔐 Authentication Flow

```
1. Register with name, email, password
2. Login → receive JWT token
3. Send token in every request header:
   Authorization: Bearer <token>
4. Token expires after 60 minutes
```

---

## 🌍 Deployment Architecture

```
User Browser
     ↓
Render (Streamlit Frontend)
     ↓  HTTP requests with JWT
Railway (FastAPI Backend)
     ↓  Beanie ODM queries
Railway (MongoDB Database)
```

### Environment Variables (Backend)

| Variable | Description |
|---|---|
| `MONGO_URL` | MongoDB connection string |
| `DB_NAME` | Database name (default: chat_app) |
| `JWT_SECRET` | Secret key for JWT signing |
| `JWT_ALGORITHM` | Algorithm (default: HS256) |
| `JWT_EXPIRY_MINUTES` | Token expiry (default: 60) |

### Environment Variables (Frontend)

| Variable | Description |
|---|---|
| `API_URL` | Backend API URL |

## 🧠 Concepts Covered

- ✅ RESTful API design with FastAPI
- ✅ MongoDB document modeling with Beanie ODM
- ✅ JWT Authentication (stateless, token-based)
- ✅ Password hashing with bcrypt
- ✅ Dependency Injection pattern
- ✅ CORS middleware configuration
- ✅ Pydantic data validation
- ✅ Async/await with Motor
- ✅ Docker containerization
- ✅ Docker Compose multi-service orchestration
- ✅ Cloud deployment with Railway and Render
- ✅ CI/CD pipeline via GitHub integration
- ✅ Environment variable management
- ✅ Separation of dev and production environments

---

## 🔮 Future Improvements

- [ ] WebSockets for real-time messaging without refresh
- [ ] File/image uploads in chat
- [ ] Message pagination
- [ ] User profile with avatar
- [ ] Room search and filtering
- [ ] Online/offline user status
- [ ] Email verification on registration
- [ ] Rate limiting on API endpoints


- GitHub: [@Jinal-ds](https://github.com/Jinal-ds)

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
