from saysynth.utils import (bpm_to_time, calculate_total_duration,
                            random_track_name)


def test_bpm_to_time_str_count():
    t = bpm_to_time(60, "1/16")
    assert t == 250


def test_bpm_to_time_str_count_time_sig():
    t = bpm_to_time(60, "1/8", "3/3")
    assert t == 375


def test_bpm_to_time_float_count():
    t = bpm_to_time(60, 1.0 / 8.0, "3/3")
    assert t == 375


def test_calculate_total_duration_without_bpm():
    total_duration = calculate_total_duration(
        start_duration=60000, duration=60000
    )
    assert total_duration == "2:00"


def test_calculate_total_duration_with_bpm():
    total_duration = calculate_total_duration(
        start_bpm=120,
        start_count=10,
        start_time_sig="4/4",
        duration_bpm=120,
        duration_count=20,
        duration_time_sig="4/4",
    )
    assert total_duration == "1:00"


def test_calculate_total_duration_with_duration_bpm_and_without_start_bpm():
    total_duration = calculate_total_duration(
        start_duration=30000,
        duration_bpm=120,
        duration_count=15,
        duration_time_sig="4/4",
    )
    assert total_duration == "1:00"


def test_calculate_total_duration_without_duration_bpm_and_with_start_bpm():
    total_duration = calculate_total_duration(
        start_bpm=120, start_count=15, start_time_sig="4/4", duration=30000
    )
    assert total_duration == "1:00"


def test_random_track_name():
    track, hash = random_track_name("test", foo="123").split("-")
    assert track == "test"
    assert len(hash) > 3
