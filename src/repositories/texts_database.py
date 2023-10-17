import os

import pandas as pd


class TextsDatabaseRepository:
    def __init__(self, name: str) -> None:
        self.__name = name

    def get_all_texts(self, chapterName: str = "all_texts") -> pd.DataFrame | None:
        try:
            return pd.read_csv(f"data/{self.__name}/{chapterName}.csv", sep="\t", index_col=False)
        except FileNotFoundError:
            return None

    def save_all_texts(
            self, 
            data: pd.DataFrame,
            chapterName: str) -> None:
        if not os.path.exists(f"data/{self.__name}"):
            os.makedirs(f"data/{self.__name}")
        data.to_csv(f"data/{self.__name}/{chapterName}.csv", sep="\t", index=False)
