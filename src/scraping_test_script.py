from container import Container


def main():
    # chapters = Container.scrapper.get_all_chapters()

    # Container.scrapper.get_all_datas(chapters)
    chapterId = Container.scrapper.create_new_story("test")
    Container.scrapper.save_to_story(chapterId, "rwrite this shit")

if __name__ == "__main__":
    main()
