from datetime import datetime
from typing import List, Dict, Any
from sqlalchemy import Engine, select, create_engine
from sqlalchemy.orm import Session
from .models import Tile, SentinelImage, MissingImage, ImageToProcess


def init_db_engine(user: str, password: str, host: str, database: str) -> Engine:
    """Initializes sqlalchemy engine that connects to postgis database

    Args:
        user (str): the user name
        password (str): the password
        host (str): the url of the database host
        database (str): the name of the database

    Returns:
        Engine: connection to postgis database
    """

    return create_engine(f"postgresql+psycopg2://{user}:{password}@{host}/{database}")


def fetch_image_data(tile_name: str, engine: Engine):
    with Session(engine) as session:
        result = []
        requested = session.scalars(select(Tile).where(Tile.name == tile_name))
        for tile in requested:
            result.append(
                {"id": tile.id, "last_img_uuid": tile.last_img_uuid, "name": tile.name}
            )

        return result


def fetch_requested_images(engine: Engine) -> List[Dict[str, Any]]:
    with Session(engine) as session:
        result = []
        requested = session.scalars(
            select(Tile).where(Tile.last_img_status == "requested")
        )
        for tile in requested:
            result.append(
                {
                    "id": tile.id,
                    "last_img_uuid": tile.last_img_uuid,
                    "name": tile.name,
                }
            )

        return result


def fetch_required_tiles(engine: Engine) -> List[Tile]:
    """Fetches tiles that completely cover Chile (i.e. required=true)"""
    with Session(engine) as session:
        result = []
        query = select(Tile).where(Tile.required).order_by(Tile.name)
        for tile in session.scalars(query):
            result.append(tile)
        return result


def fetch_missing_images(engine: Engine) -> List[ImageToProcess]:
    """Fetches images that have not been processed"""
    with Session(engine) as session:
        result = []
        img_query = select(Tile.id, MissingImage.tile, MissingImage.uuid).join(
            Tile, onclause=Tile.name == MissingImage.tile
        )
        for img in session.execute(img_query):
            result.append(ImageToProcess(img[0], img[1], img[2]))
        return result


def fetch_tile_images(
    engine: Engine, tile: str, columns: List = [SentinelImage]
) -> List[datetime]:
    result = []
    query = select(*columns).where(
        SentinelImage.required == True, SentinelImage.tile == tile
    )
    with Session(engine) as session:
        for row in session.execute(query):
            result.append(row)
    return result


def add_missing_image(engine: Engine, uuid: str, tile: str):
    with Session(engine) as session:
        new_image = MissingImage(uuid=uuid, tile=tile)
        session.add(new_image)


def fetch_images_from_tile(tile: str, engine: Engine) -> List[SentinelImage]:
    with Session(engine) as session:
        images = []
        img_query = (
            select(SentinelImage)
            .where(SentinelImage.tile == tile)
            .order_by(SentinelImage.date)
        )

        for img in session.scalars(img_query):
            images.append(img)

        return images
