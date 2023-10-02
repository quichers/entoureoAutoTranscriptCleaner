import os

import pandas as pd


class TextsDatabaseRepository:
    def __init__(self, name: str) -> None:
        self.__name = name

    def get_all_texts(self) -> pd.DataFrame | None:
        try:
            return pd.read_csv(f"data/{self.__name}/all_texts.csv", index_col=False)
        except FileNotFoundError:
            return None

    def save_all_texts(self, data: pd.DataFrame) -> None:
        if not os.path.exists(f"data/{self.__name}"):
            os.makedirs(f"data/{self.__name}")
        data.to_csv(f"data/{self.__name}/all_texts.csv", index=False)
