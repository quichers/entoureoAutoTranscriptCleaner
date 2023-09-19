import pandas as pd


class TextsDatabaseRepository:
    def __init__(self, name: str) -> None:
        self.__name = name

    def get_all_texts(self) -> pd.DataFrame:
        return pd.read_csv(f"data/{self.__name}/all_texts.csv")

    def save_all_texts(self) -> pd.DataFrame:
        pd.to_csv(f"data/{self.__name}/all_texts.csv")