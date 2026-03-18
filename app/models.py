from sqlalchemy.orm import Mapped, mapped_column
from .database import Base

class UserORM(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True, index=True)
