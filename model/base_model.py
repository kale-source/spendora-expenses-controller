import uuid
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, registry

table_registry = registry()

class Base(DeclarativeBase):
    "para garantir que todos os models sejam registrados aqui, assim na hora de criar, só cria aqui."
    registry = table_registry
    
@dataclass
class BaseModel(Base):
    "modelo padrão para todos os models desse projeto"
    __abstract__ = True
    
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        index=True,
        default=uuid.uuid4,
        nullable=False,
        comment="Chave primária técnica (UUID v4)"
    )
    created_by: Mapped[str] = mapped_column(default="System")
    created_at: Mapped[datetime] = mapped_column(default=func.utcnow())
    updated_by: Mapped[Optional[str]] = mapped_column(default=None, nullable=True)
    updated_at: Mapped[Optional[datetime]] = mapped_column(default=None, onupdate=func.utcnow())
    deleted_by: Mapped[Optional[str]] = mapped_column(default=None, nullable=True)
    deleted_at: Mapped[Optional[datetime]] = mapped_column(default=None, onupdate=func.utcnow())
    activated_by: Mapped[Optional[str]] = mapped_column(default=None, nullable=True)
    activated_at: Mapped[Optional[datetime]] = mapped_column(default=None, onupdate=func.utcnow())
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False, index=True)
    is_deleted:Mapped[bool] = mapped_column(Boolean, default=False, nullable=False, index=True)
    
    def as_dict(self):
        """Converte o objeto SQLAlchemy em um dicionário."""
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }
    
    def soft_activate(self, activated_by: Optional[str] = None) -> None:
        self.is_active = True
        self.activated_at = func.utcnow()
        self.activated_by = activated_by
    
    def restore_activate(self) -> None:
        self.is_active = False
        self.activated_at = None
        self.activated_by = None
    
    def soft_delete(self, deleted_by: Optional[str] = None) -> None:
        self.deleted_at = func.utcnow()
        self.deleted_by = deleted_by
        self.is_deleted = True

    def restore_delete(self) -> None:
        self.deleted_at = None
        self.deleted_by = None
        self.is_deleted = False
    
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        super().__init__(**kwargs)
