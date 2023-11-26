"""
Assorted utilities for use throughout `saysynth`
"""

import collections
import math
import os
import tempfile
from typing import Any, Dict, List, Union

from hashids import Hashids

from .constants import (DEFAULT_BPM_TIME_BPM, DEFAULT_BPM_TIME_COUNT,
                        DEFAULT_BPM_TIME_SIG)

hashids = Hashids(salt="saysynth", min_length=3, alphabet="42069iacabplurwtf")


def frange(start: float, stop: float, by: float, sig_digits: int = 5):
    """
    Generate a range of float values.

    Args:
        start: The starting value of the range.
        stop: The ending value of the range.
        by: the amount to divide the range by.
        sig_digits:  The number of significant digits to use when rounding.

    """
    div = math.pow(10, sig_digits)
    for value in range(int(start * div), int(stop * div), int(by * div)):
        yield round(value / div, sig_digits)


def here(f, *args):
    """
    Pass `__file__` to get the current directory and `*args` to generate a filepath relative
    to the current directory.

    Args:
        f: Usually `__file__`
    """
    return os.path.join(os.path.dirname(os.path.abspath(f)), *args)


def make_tempfile(format: str = "txt"):
    """
    Make a tempfile
    Args:
        format: The file's suffix.
    """
    return tempfile.mkstemp(suffix=f".{format}")[-1]


def bpm_to_time(
    bpm: float = 120.00,
    count: Union[str, int, float] = 1,
    time_sig: str = DEFAULT_BPM_TIME_SIG,
) -> float:
    """
    Take a bpm, note count, and time_sig and return a length in milliseconds
    Args:
        bpm: The bpm as a float
        count: the count as a string, int, or float (eg: '2/1', 2, 2.0 )
        time_sig: The time signature as a string (eg: '4/4')

    """
    if isinstance(count, str):
        if "/" in count:
            numerator, denominator = count.split("/")
            count = float(numerator) / float(denominator)
    time_segments = time_sig.split("/")
    return (
        (60.00 / float(bpm)) * float(time_segments[0]) * float(count) * 1000.0
    )


def rescale(
    x: Union[int, float],
    range_x: List[Union[int, float]],
    range_y: List[Union[int, float]],
    sig_digits: int = 3,
) -> float:
    """
    Rescale value `x` to scale `y` give the range of `x` and the range of `y`

    Args:
        x: An value to rescale
        range_x: The range ([min, max]) of the origin scale
        range_y: The range ([min, max]) of the target scale
        sig_digits: The number of significant digits to use when rounding.

    """
    # Figure out how 'wide' each range is
    x_min = min(range_x)
    y_min = min(range_y)
    x_span = max(range_x) - x_min
    y_span = max(range_y) - y_min

    # Compute the scale factor between left and right values
    scale_factor = float(y_span) / float(x_span)

    return round(y_min + (x - x_min) * scale_factor, sig_digits)


def calculate_total_duration(**kwargs) -> str:
    """
    Calculate the total duration of a track/chord/etc and
    format it as a string.
    Args:
        start_bpm/count/time_sig: the start of the track
        duration_bpm/count/time_sig: the duration of the passage
    Returns: float
    """
    if not kwargs.get("start_duration", None):
        start_duration = bpm_to_time(
            kwargs.get("start_bpm", DEFAULT_BPM_TIME_BPM),
            kwargs.get("start_count", DEFAULT_BPM_TIME_COUNT),
            kwargs.get("start_time_sig", DEFAULT_BPM_TIME_SIG),
        )
    else:
        start_duration = kwargs.get("start_duration", 0)
    if not kwargs.get("duration", None):
        duration = bpm_to_time(
            kwargs.get("duration_bpm", DEFAULT_BPM_TIME_BPM),
            kwargs.get("duration_count", DEFAULT_BPM_TIME_COUNT),
            kwargs.get("duration_time_sig", DEFAULT_BPM_TIME_SIG),
        )
    else:
        duration = kwargs.get("duration", 0)

    seconds = (start_duration + duration) / 1000.0
    minutes = math.floor(seconds / 60.0)
    remainder_seconds = seconds - (minutes * 60.0)
    return f"{minutes}:{int(math.floor(remainder_seconds)):02}"


def update_dict(d: Dict[Any, Any], u: Dict[Any, Any]) -> Dict[Any, Any]:
    """
    Recursively update a dictionary.
    Args:
        d: the dictionary to be updated
        u: the dictionary to use in update
    Returns: dict
    """
    for k, v in u.items():
        if isinstance(v, collections.Mapping):
            d[k] = update_dict(d.get(k, {}), v)
        else:
            d[k] = v
    return d


def random_track_name(track_type: str, **options) -> str:
    """
    Generate a unique track name given a type and a dict of options
    """
    hash_id = hashids.encode(
        int.from_bytes((track_type + str(options)).encode(), "little")
    )[:5]
    return f"{track_type}-{str(hash_id)}"
