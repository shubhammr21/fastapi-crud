from pydantic import BaseModel


class NoteSchema(BaseModel):
    title: str
    content: str


class NoteDB(NoteSchema):
    id: int
