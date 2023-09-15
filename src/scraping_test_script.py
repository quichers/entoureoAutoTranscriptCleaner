from repositories.scrapper import Scrapper
from config import ENTOUREO_EMAIL, ENTOUREO_PASSWORD


def main():
    scrapper = Scrapper(email=ENTOUREO_EMAIL, password=ENTOUREO_PASSWORD)
    scrapper.login()
    chapters = scrapper.get_all_chapters()

    transcriptions = scrapper.get_chapter_data(chapters.loc[0, '_id'])

    transcriptName, transcriptData = scrapper.get_transcription(transcriptions[0]['_id'])

    print(transcriptName)
    print(transcriptData)


if __name__ == '__main__':
    main()