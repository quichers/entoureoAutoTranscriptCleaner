from container import Container


def main():
    Container.scrapper.login()
    chapters = Container.scrapper.get_all_chapters()

    transcriptions = Container.scrapper.get_chapter_data(chapters.loc[0, "_id"])

    transcriptName, transcriptData = Container.scrapper.get_transcription(
        transcriptions[0]["_id"]
    )
    print(transcriptName)
    print(transcriptData)
    # Container.texts_database.get_all_texts()


if __name__ == "__main__":
    main()
