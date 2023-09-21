from functools import lru_cache
from typing import cast

from config import ENTOUREO_EMAIL, ENTOUREO_PASSWORD
from dependencies import Injector, value
from repositories.scrapper import EntoureoConnection, Scrapper
from repositories.text_smoother import TextSmootherRepository
from repositories.texts_database import TextsDatabaseRepository


class Container(Injector):
    text_smoother = cast(TextSmootherRepository, TextSmootherRepository)
    texts_database = cast(TextsDatabaseRepository, TextsDatabaseRepository)
    scrapper = cast(Scrapper, Scrapper)
    entoureo_connection = cast(EntoureoConnection, EntoureoConnection)

    @value
    def name() -> str:
        return "renaudTests"

    @value
    @lru_cache
    def entoureo_connection() -> EntoureoConnection:
        return EntoureoConnection(ENTOUREO_EMAIL, ENTOUREO_PASSWORD)
