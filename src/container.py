from dependencies import Injector
from repositories.text_smoother import TextSmootherRepository
from typing import cast


class Container(Injector):
    text_smoother = cast(TextSmootherRepository, TextSmootherRepository)
