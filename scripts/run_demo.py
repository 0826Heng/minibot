from minibot import MiniBotApp


def main() -> None:
    app = MiniBotApp()
    print(app.run_once("hello"))


if __name__ == "__main__":
    main()
