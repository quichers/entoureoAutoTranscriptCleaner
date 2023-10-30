import os

import pandas as pd


class TextsDatabaseRepository:
    def __init__(self, name: str) -> None:
        self.__name = name

    def get_text(self, chapterName: str = "all_texts") -> pd.DataFrame | None:
        try:
            return pd.read_csv(f"data/{self.__name}/{chapterName}.csv", sep=";", index_col=False)
        except FileNotFoundError:
            return None

    def save_text(
            self, 
            data: pd.DataFrame,
            chapterName: str) -> None:
        if not os.path.exists(f"data/{self.__name}"):
            os.makedirs(f"data/{self.__name}")
        data.to_csv(f"data/{self.__name}/{chapterName}.csv", sep=";", index=False, encoding="utf-8-sig")
