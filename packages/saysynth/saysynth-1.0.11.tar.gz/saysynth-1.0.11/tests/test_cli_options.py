from saysynth.cli.options import (expand_opt_name, format_opt_value,
                                  log_configurations, shorten_opt_name)


def test_expand_opt_name_text():
    assert expand_opt_name("-tx") == "text"
    assert expand_opt_name("tx") == "text"
    assert expand_opt_name("--text") == "text"
    assert expand_opt_name(" --TEXT ") == "text"


def test_shorten_opt_name_text():
    assert shorten_opt_name("-tx") == "tx"
    assert shorten_opt_name("tx") == "tx"
    assert shorten_opt_name("--text") == "tx"
    assert shorten_opt_name(" --TEXT ") == "tx"


def test_format_opt_value_chord_notes():
    assert format_opt_value("-cn", "1,2,4,5") == [1, 2, 4, 5]
    assert format_opt_value("--chord_notes", "1,2,4,5") == [1, 2, 4, 5]


def test_log_configurations():
    configs = log_configurations("chord", yaml=True, voice="Fred")
    config_options = list(configs["tracks"][0].values())[0]["options"]
    assert "yaml" not in config_options
    assert config_options["voice"] == "Fred"
