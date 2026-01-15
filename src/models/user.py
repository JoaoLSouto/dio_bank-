import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..models.base import db


class User(db.Model):
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    username: Mapped[str] = mapped_column(sa.String, unique=True)
    password: Mapped[str] = mapped_column(sa.String, nullable=False)

    role_id: Mapped[int] = mapped_column(sa.ForeignKey("role.id"))
    role: Mapped["Role"] = relationship(back_populates="users")

    def __repr__(self) -> str:
        return f"User(id={self.id}, username={self.username})"
