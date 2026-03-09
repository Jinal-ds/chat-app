from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from database import init_db
from routers import auth, rooms, messages

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    print("✅ MongoDB connected!")
    yield
    print("🔴 Shutting down...")

app = FastAPI(
    title="💬 Chat App API",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(rooms.router)
app.include_router(messages.router)

@app.get("/", tags=["Health"])
async def root():
    return {"status": "✅ Chat API running!"}