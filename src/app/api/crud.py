from app.api.models import NoteSchema
from app.db import notes, database


async def post(payload: NoteSchema):
    query = notes.insert().values(title=payload.title, content=payload.content)
    return await database.execute(query=query)


async def get(note_id: int):
    query = notes.select().where(notes.c.id == note_id)
    return await database.fetch_one(query=query)


async def get_all():
    query = notes.select()
    return await database.fetch_all(query=query)


async def update(node_id: int, payload: NoteSchema):
    query = (
        notes
        .update()
        .where(notes.c.id == node_id)
        .values(title=payload.title, content=payload.content)
        .returning(notes.c.id)
    )
    return await database.execute(query=query)


async def delete(note_id: int):
    query = notes.delete().where(notes.c.id == note_id)
    return await database.execute(query=query)
