from minibot import MiniBotApp


def test_app_run_once() -> None:
    app = MiniBotApp()
    out = app.run_once("ping")
    assert out == "[echo-agent] ping"
