from container import Container


def main():
<<<<<<< HEAD
    chapters = Container.scrapper.get_all_chapters()
    transcriptions = Container.scrapper.get_chapter_data(chapters.loc[1, "_id"])

    transcriptData = Container.scrapper.get_transcription(
        transcriptions[0]["_id"], chapters.loc[0, "_id"]
    )
    print(transcriptData)
=======
    # chapters = Container.scrapper.get_all_chapters()
    # transcriptions = Container.scrapper.get_chapter_data(chapters.loc[0, "_id"])

    # transcriptName, transcriptData = Container.scrapper.get_transcription(
    #     transcriptions[0]["_id"], chapters.loc[0, "_id"]
    # )
    # print(transcriptName)
    # print(transcriptData)
    Container.scrapper.save_to_story("6529456e77d0b130fde581ac", "rwrite this shit")
>>>>>>> 4c59fc5f4ced5ed185e349e68e00581e46837765

    Container.scrapper.get_all_datas(chapters)

if __name__ == "__main__":
    main()
