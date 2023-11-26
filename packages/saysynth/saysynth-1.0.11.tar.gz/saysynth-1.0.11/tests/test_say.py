from saysynth.lib import say


def test_gen_data_format_arg():
    data_format = say._gen_data_format_arg("AIFF", "LE", "F", 32, 22050)
    assert data_format == "BEF32@22050"
    data_format = say._gen_data_format_arg("WAVE", "LE", "F", 32, 22050)
    assert data_format == "LEF32@22050"
    data_format = say._gen_data_format_arg("WAVE", "LE", "F", 16, 22050)
    assert data_format == "LEF32@22050"


def test_say_cmd():
    args = say.cmd(
        voice="Fred",
        rate=70,
        input_text="Hello World",
        audio_device="test",
        executable="/usr/bin/say",
        stereo=True,
    )
    assert args == [
        "/usr/bin/say",
        "Hello World",
        "-v",
        "Fred",
        "-r",
        "70",
        "--quality=127",
        "-a",
        "test",
    ]
    args = say.cmd(
        voice="Alex",
        rate=70,
        input_text="Hello World",
        audio_device="test",
        executable="/usr/bin/say",
        stereo=True,
        sample_rate=12000,
        sample_size=8,
        endianness="BE",
        data_type="I",
        audio_output_file="test.wav",
    )
    assert args == [
        "/usr/bin/say",
        "Hello World",
        "-v",
        "Alex",
        "-r",
        "70",
        "--file-format",
        "WAVE",
        "-o",
        "test.wav",
        "--data-format",
        "BEI8@12000",
        "--channels=2",
    ]
