from fastapi import APIRouter, HTTPException, Depends
from models.room import Room, RoomCreate, RoomResponse
from models.user import User
from dependencies import get_current_user
from typing import List

router = APIRouter(prefix="/rooms", tags=["Rooms"])

@router.post("/", response_model=RoomResponse, status_code=201)
async def create_room(data: RoomCreate, current_user: User = Depends(get_current_user)):
    existing = await Room.find_one(Room.name == data.name)
    if existing:
        raise HTTPException(status_code=400, detail="Room name already exists")
    room = Room(**data.dict(), created_by=str(current_user.id))
    await room.insert()
    return RoomResponse(
        id=str(room.id), name=room.name,
        description=room.description,
        created_by=room.created_by,
        created_at=room.created_at
    )

@router.get("/", response_model=List[RoomResponse])
async def get_rooms(current_user: User = Depends(get_current_user)):
    rooms = await Room.find_all().to_list()
    return [
        RoomResponse(
            id=str(r.id), name=r.name,
            description=r.description,
            created_by=r.created_by,
            created_at=r.created_at
        ) for r in rooms
    ]

@router.delete("/{room_id}", status_code=204)
async def delete_room(room_id: str, current_user: User = Depends(get_current_user)):
    room = await Room.get(room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    if room.created_by != str(current_user.id):
        raise HTTPException(status_code=403, detail="Not authorized")
    await room.delete()