from fastapi import APIRouter, HTTPException

from app.api import crud
from app.api.models import NoteDB, NoteSchema
from utils import status

router = APIRouter()


@router.post("/", response_model=NoteDB, status_code=status.HTTP_201_CREATED)
async def create_note(payload: NoteSchema):
    note_id = await crud.post(payload)
    response = {
        "id": note_id,
        "title": payload.title,
        "content": payload.content,
    }
    return response


@router.get("/", response_model=list[NoteDB], status_code=status.HTTP_200_OK)
async def read_all_notes():
    notes = await crud.get_all()
    # response = [
    #     {
    #         "id": note.id,
    #         "title": note.title,
    #         "content": note.content,
    #     }
    #     for note in notes
    # ]
    return notes


@router.get("/{note_id}", response_model=NoteDB, status_code=status.HTTP_200_OK)
async def read_note(note_id: int):
    note = await crud.get(note_id)
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Note not found")
    return note


@router.put("/{note_id}", response_model=NoteDB, status_code=status.HTTP_200_OK)
async def update_note(note_id: int, payload: NoteSchema):
    note = await crud.get(note_id)
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Note not found")
    note_ = await crud.update(note_id, payload)
    response = {
        "id": note_,
        "title": payload.title,
        "content": payload.content,
    }
    return response


@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_note(note_id: int):
    note = await crud.get(note_id)
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Note not found")
    await crud.delete(note_id)
    return note
