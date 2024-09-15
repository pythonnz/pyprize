from typing import Optional
from sqlmodel import Field, SQLModel
from datetime import datetime


class Candidate(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    drawn_at: Optional[datetime] = Field(
        default=None, sa_column_kwargs={"nullable": True}
    )
    awarded_prize: bool = Field(default=False)

    def mark_as_drawn(self):
        self.drawn_at = datetime.now()

    # TODO(iokiwi): 
    def award_prize(self, prize=None):
        self.awarded_prize = True


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(sa_column_kwargs={"unique": True})
    password: str = Field()
