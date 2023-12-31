import time
from typing import Any

import pandas as pd
import requests
from repositories.texts_database import TextsDatabaseRepository


class EntoureoConnection:
    LOGIN_URL = "https://redaction-backend-prod.herokuapp.com/public/connexions/login"

    def __init__(self, scrapper_email: str, scrapper_password: str) -> None:
        self.__email = scrapper_email
        self.__password = scrapper_password
        self.__session = requests.session()
        if not self.__email or not self.__password:
            print(
                f"Found {self.__email} for username and {self.__password} "
                f"for password. Need to set them in the .env file"
            )
            return

        payload = {"email": self.__email, "password": self.__password}

        print("Login to entoureo ...")
        response = self.__session.post(self.LOGIN_URL, data=payload)
        assert (
            200 <= response.status_code < 300
        ), f"The request wasn't valid, got status code {response.status_code}"
        print(
            response.status_code
        )  # If the request went Ok we usually get a 200 status.

        self.token = response.json()["accessToken"]
        self.biography_id = response.json()["projectsList"][0]["_id"]
        # self.userId = response.json()["user"]["_id"]

    def post(self, url: str, data: dict[str, Any]) -> requests.Response:
        return self.__session.post(
            url,
            headers={"authorization": self.token},
            data=data,
        )


class Scrapper:
    CHAPTERS_URL = (
        "https://redaction-backend-prod.herokuapp.com/platform/chapters/get-all-for-bio"
    )
    CHAPTER_URL = "https://redaction-backend-prod.herokuapp.com/platform/chapters/get-chapter-data"
    TRANSCRIPT_URL = (
        "https://redaction-backend-prod.herokuapp.com/platform/transcripts/get-model"
    )

    def __init__(
        self,
        entoureo_connection: EntoureoConnection,
        texts_database: TextsDatabaseRepository,
    ) -> None:
        self.__connection = entoureo_connection
        self.__texts_database = texts_database

    # def login(self) -> None:
    #     if not self.__email or not self.__password:
    #         print(
    #             f"Found {self.__email} for username and {self.__password} "
    #             f"for password. Need to set them in the .env file"
    #         )
    #         return

    #     payload = {"email": self.__email, "password": self.__password}

    #     print("Login to entoureo ...")
    #     response = self.__session.post(self.LOGIN_URL, data=payload)
    #     assert (
    #         200 <= response.status_code < 300
    #     ), f"The request wasn't valid, got status code {response.status_code}"
    #     print(
    #         response.status_code
    #     )  # If the request went Ok we usually get a 200 status.

    #     self.token = response.json()["accessToken"]
    #     self.biography_id = response.json()["projectsList"][0]["_id"]
    #     self.userId = response.json()["user"]["_id"]

    def get_all_chapters(self) -> pd.DataFrame:
        payload = {"biographyId": self.__connection.biography_id}

        print("Catching chapters ids ...")
        response = self.__connection.post(
            self.CHAPTERS_URL,
            data=payload,
        )
        print(
            response.status_code
        )  # If the request went Ok we usually get a 200 status.

        chaptersList = pd.DataFrame(response.json()["chaptersList"])
        chapters2Clean = chaptersList.loc[chaptersList["status"] == "editionProcess"]

        print("Number of chapters :", chapters2Clean.shape[0])
        print()
        time.sleep(1)
        return chapters2Clean

    def get_chapter_data(self, chapterId: str) -> list[dict]:
        payload = {"chapterId": chapterId}

        print("Catching first chapter ...")
        response = self.__connection.post(
            self.CHAPTER_URL,
            data=payload,
        )
        print(
            response.status_code
        )  # If the request went Ok we usually get a 200 status.
        transcriptsList = response.json()["transcriptsList"]

        print("Number of Transcriptions in this chapter :", len(transcriptsList))

        print()
        time.sleep(1)
        return transcriptsList

    def get_transcription(
        self,
        transcriptId: str,
        chapterId: str,
        chapterName: str = "all_texts",
    ) -> pd.DataFrame:
        payload = {"transcriptId": transcriptId}

        print("Catching first transcription ...")
        response = self.__connection.post(
            self.TRANSCRIPT_URL,
            data=payload,
        )
        print(
            response.status_code
        )  # If the request went Ok we usually get a 200 status.

        text_concat = '\n'.join([element['text'] for element in response.json()["transcript"]["userTranscriptData"]])
        transcriptName = response.json()["transcript"]["title"]
        transcriptData = pd.DataFrame(data=[{"transcriptName": transcriptName,
                                            "transcriptId": transcriptId,
                                            "chapterId" : chapterId,
                                            "text_concat": text_concat}])

        local_database = self.__texts_database.get_text(chapterName)
        if local_database is None:
            print("No local database found, creating one ...")
            self.__texts_database.save_text(transcriptData, chapterName)
        else:
            # TODO: might cause performance issues: https://stackoverflow.com/questions/49928463/python-pandas-update-a-dataframe-value-from-another-dataframe
            print(f"Updating local database with {len(transcriptData)} record...")
            updated_texts = pd.concat([local_database, transcriptData]).drop_duplicates(
                ["transcriptName", "transcriptId", "chapterId"], keep="last"
            )
            self.__texts_database.save_text(updated_texts, chapterName)

        return transcriptData
    
    def get_all_datas(
            self, 
            chaptersList: pd.DataFrame
            ) -> pd.DataFrame:
        for index, chapter in chaptersList.iterrows():
            print(chapter["title"])
            transcriptions = self.get_chapter_data(chapter["_id"])

            for transcript in transcriptions:
                print(transcript["title"])
                self.get_transcription(transcript["_id"], chapter["_id"], chapter["title"])

        return 