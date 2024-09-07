from typing import Optional
from sqlmodel import Field, SQLModel


class Candidate(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    already_won: bool = Field(default=False)
