from dependencies import Injector, value
from repositories.text_smoother import TextSmootherRepository
from typing import cast
from repositories.texts_database import TextsDatabaseRepository
from repositories.scrapper import Scrapper
from config import ENTOUREO_EMAIL, ENTOUREO_PASSWORD


class Container(Injector):
    text_smoother = cast(TextSmootherRepository, TextSmootherRepository)
    texts_database = cast(TextsDatabaseRepository, TextsDatabaseRepository)
    scrapper = cast(Scrapper, Scrapper)

    @value
    def name() -> str:
        return "renaudTests"

    @value
    def scrapper_email() -> str:
        return ENTOUREO_EMAIL

    @value
    def scrapper_password() -> str:
        return ENTOUREO_PASSWORD
