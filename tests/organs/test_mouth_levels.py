import math
from array import array

from organs.mouth.levels import RATE, levels_from_audio

SR = 22050


def tone(seconds, amplitude):
    return [int(amplitude * math.sin(2 * math.pi * 200 * i / SR)) for i in range(int(seconds * SR))]


def test_one_level_per_25th_of_a_second():
    assert len(levels_from_audio(tone(2.0, 8000), SR)) == 2 * RATE


def test_loud_opens_quiet_drops_to_zero():
    levels = levels_from_audio(tone(1.0, 10000) + [0] * SR + tone(1.0, 2500), SR)
    loud, gap, soft = levels[:RATE], levels[RATE:2 * RATE], levels[2 * RATE:]
    assert min(loud[1:-1]) > 0.9
    assert max(gap) == 0.0
    assert 0.2 < max(soft) < 0.6


def test_scaled_to_the_utterance_so_a_quiet_voice_still_opens_fully():
    assert max(levels_from_audio(tone(1.0, 1500), SR)) > 0.95


def test_accepts_raw_bytes_and_empty_audio():
    raw = array("h", tone(0.5, 8000)).tobytes()
    assert levels_from_audio(raw, SR) == levels_from_audio(tone(0.5, 8000), SR)
    assert levels_from_audio(b"", SR) == []
