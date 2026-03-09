from fastapi import APIRouter, HTTPException, Depends
from models.message import Message, MessageCreate, MessageResponse
from models.room import Room
from models.user import User
from dependencies import get_current_user
from typing import List

router = APIRouter(prefix="/rooms", tags=["Messages"])

@router.post("/{room_id}/messages", response_model=MessageResponse, status_code=201)
async def send_message(
    room_id: str,
    data: MessageCreate,
    current_user: User = Depends(get_current_user)
):
    room = await Room.get(room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    message = Message(
        room_id=room_id,
        sender_id=str(current_user.id),
        sender_name=current_user.name,
        content=data.content
    )
    await message.insert()
    return MessageResponse(
        id=str(message.id), room_id=room_id,
        sender_name=message.sender_name,
        content=message.content,
        created_at=message.created_at
    )

@router.get("/{room_id}/messages", response_model=List[MessageResponse])
async def get_messages(
    room_id: str,
    limit: int = 50,
    current_user: User = Depends(get_current_user)
):
    room = await Room.get(room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    messages = await Message.find(
        Message.room_id == room_id
    ).sort(-Message.created_at).limit(limit).to_list()
    return [
        MessageResponse(
            id=str(m.id), room_id=m.room_id,
            sender_name=m.sender_name,
            content=m.content,
            created_at=m.created_at
        ) for m in messages
    ]
@router.delete("/{room_id}/messages/{message_id}", status_code=204)
async def delete_message(
    room_id: str,
    message_id: str,
    current_user: User = Depends(get_current_user)
):
    message = await Message.get(message_id)
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    if message.sender_id != str(current_user.id):
        raise HTTPException(status_code=403, detail="Not authorized")
    await message.delete()