from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class ItemDB(Base):
    __tablename__ = "items"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str]
    price: Mapped[float]
    category_id: Mapped[int | None] = mapped_column(ForeignKey("categories.id"))
    in_stock: Mapped[bool | None] = mapped_column(default=True)
    created_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    category: Mapped["CategoryDB | None"] = relationship(back_populates="items")


class CategoryDB(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str | None]
    created_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    items: Mapped[list["ItemDB"]] = relationship(
        back_populates="category", passive_deletes=True
    )
