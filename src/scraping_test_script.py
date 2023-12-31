from container import Container


def main():
    chapters = Container.scrapper.get_all_chapters()
    transcriptions = Container.scrapper.get_chapter_data(chapters.loc[1, "_id"])

    transcriptData = Container.scrapper.get_transcription(
        transcriptions[0]["_id"], chapters.loc[0, "_id"]
    )
    print(transcriptData)

    Container.scrapper.get_all_datas(chapters)

if __name__ == "__main__":
    main()
