from container import Container


def main():
    # chapters = Container.scrapper.get_all_chapters()
    # transcriptions = Container.scrapper.get_chapter_data(chapters.loc[0, "_id"])

    # transcriptName, transcriptData = Container.scrapper.get_transcription(
    #     transcriptions[0]["_id"], chapters.loc[0, "_id"]
    # )
    # print(transcriptName)
    # print(transcriptData)
    Container.scrapper.save_to_story("6529456e77d0b130fde581ac", "rwrite this shit")


if __name__ == "__main__":
    main()
