from fastapi import APIRouter, HTTPException
from models.user import User, RegisterRequest, LoginRequest, UserResponse
from dependencies import hash_password, verify_password, create_token

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=UserResponse, status_code=201)
async def register(data: RegisterRequest):
    existing = await User.find_one(User.email == data.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = User(
        name=data.name,
        email=data.email,
        hashed_password=hash_password(data.password)
    )
    await user.insert()
    return UserResponse(id=str(user.id), name=user.name, email=user.email)

@router.post("/login")
async def login(data: LoginRequest):
    user = await User.find_one(User.email == data.email)
    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    token = create_token({"sub": str(user.id)})
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": UserResponse(id=str(user.id), name=user.name, email=user.email)
    }