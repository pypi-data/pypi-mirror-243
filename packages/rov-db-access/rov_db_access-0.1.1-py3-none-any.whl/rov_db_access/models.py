""" Models for this app """
from datetime import datetime
from typing import Optional

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import DateTime
from geoalchemy2 import Geometry


class Base(DeclarativeBase):
    """Base Class of the model"""


class Tile(Base):
    """Tile model"""

    __tablename__ = "tiles"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    geom = mapped_column(Geometry("POLYGON", srid=4326))
    last_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    last_img_status: Mapped[str] = mapped_column(default="none")
    last_s3_key: Mapped[Optional[str]]
    required: Mapped[bool]
    last_img_uuid: Mapped[Optional[str]]


class SentinelImage(Base):
    """Sentinel Image"""

    __tablename__ = "sentinel_images"
    id: Mapped[int] = mapped_column(primary_key=True)
    uuid: Mapped[str]
    tile: Mapped[str]
    date: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    s3_key: Mapped[str]
    cloud: Mapped[float]
    footprint = mapped_column(Geometry("POLYGON", srid=4326))
    required: Mapped[bool] = mapped_column(default=False)


class MissingImage(Base):
    """Missing Sentinel Image"""

    __tablename__ = "missing_images"
    uuid: Mapped[str] = mapped_column(primary_key=True)
    tile: Mapped[str]


class ImageToProcess:
    """Helper model for keeping track of images to process"""

    def __init__(self, tile_id: int, tile: str, uuid: str):
        self.tile = tile
        self.uuid = uuid
        self.tile_id = tile_id
