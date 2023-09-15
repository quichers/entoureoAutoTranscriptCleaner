import time
import requests
import pandas as pd

class Scrapper:
    
	LOGIN_URL = "https://redaction-backend-prod.herokuapp.com/public/connexions/login"
	CHAPTERS_URL = "https://redaction-backend-prod.herokuapp.com/platform/chapters/get-all-for-bio"
	CHAPTER_URL = "https://redaction-backend-prod.herokuapp.com/platform/chapters/get-chapter-data"
	TRANSCRIPT_URL = "https://redaction-backend-prod.herokuapp.com/platform/transcripts/get-model"

	
	
	def __init__(self, email: str, password: str) -> None:
		self.__email = email
		self.__password = password
		self.__session = requests.session()

	def login(self) -> None:
		if not self.__email or not self.__password:
			print(
                f"Found {self.__email} for username and {self.__password} for password. Need to set them in the .env file"
            )
			return

		payload={
			"email": self.__email,
			"password": self.__password
		}

		print("Login to entoureo ...")
		response = self.__session.post(self.LOGIN_URL, data=payload)
		assert 200 <= response.status_code < 300, f"The request wasn't valid, got status code {response.status_code}"
		print(response.status_code) # If the request went Ok we usually get a 200 status.

		self.token = response.json()["accessToken"]
		self.biographyId = response.json()['projectsList'][0]['_id']
		self.userId = response.json()["user"]['_id']
	
	def get_all_chapters(self) -> pd.DataFrame:
		payload = {
			"biographyId": self.biographyId
		}

		print("Catching chapters ids ...")
		response = self.__session.post(self.CHAPTERS_URL, headers={'authorization': self.token}, data=payload)
		print(response.status_code) # If the request went Ok we usually get a 200 status.

		chaptersList = pd.DataFrame(response.json()['chaptersList'])
		chapters2Clean = chaptersList.loc[chaptersList["status"] == "editionProcess"]
		chaptersSize = chapters2Clean.shape[0]

		print("Number of chapters :", chaptersSize)
		print()
		time.sleep(1)
		return chapters2Clean

	def get_chapter_data(self, chapterId: str) -> list[dict]:
		payload = {
			"chapterId": chapterId
		}

		print("Catching first chapter ...")
		response = self.__session.post(self.CHAPTER_URL, headers={'authorization': self.token}, data=payload)
		print(response.status_code) # If the request went Ok we usually get a 200 status.
		transcriptsList = response.json()['transcriptsList']

		print("Number of Transcriptions in this chapter :", len(transcriptsList))

		print()
		time.sleep(1)
		return transcriptsList

	def get_transcription(self, transcriptId: str) -> tuple[str, pd.DataFrame]:
		payload = {
			"transcriptId": transcriptId
		}

		print("Catching first transcription ...")
		response = self.__session.post(self.TRANSCRIPT_URL, headers={'authorization': self.token}, data=payload)
		print(response.status_code) # If the request went Ok we usually get a 200 status.

		transcriptData = pd.DataFrame(response.json()['transcript']['userTranscriptData'])
		transcriptName = response.json()['transcript']['title']
		return (transcriptName, transcriptData)
	