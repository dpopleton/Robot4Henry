import os

import pytest

from virtual_robot.voice import Utterance, VirtualVoice, split_sentences


def test_split_sentences():
    assert split_sentences("Hello Henry! I'm Qbot.  Shall we build?") == ["Hello Henry!", "I'm Qbot.", "Shall we build?"]
    assert split_sentences("no full stop") == ["no full stop"]
    assert split_sentences("   ") == []


def test_sentence_at():
    u = Utterance(b"", 22050, [], [(0.0, "One."), (1.5, "Two.")])
    assert [u.sentence_at(t) for t in (0.0, 1.4, 1.5, 9.0)] == ["One.", "One.", "Two.", "Two."]


def test_missing_model_is_reported():
    assert "No voice model" in (VirtualVoice("/nowhere/voice.onnx").unavailable_reason() or "")


voice = VirtualVoice()


@pytest.mark.skipif(voice.unavailable_reason() is not None, reason="Piper voice not available here")
def test_real_voice_gives_audio_levels_and_sentence_starts():
    u = voice.prepare("Hello Henry! I'm Qbot.")
    assert 1.0 < u.seconds < 5.0
    assert abs(len(u.levels) - u.seconds * 25) <= 1
    assert max(u.levels) > 0.9 and min(u.levels) == 0.0      # loud syllables and gaps
    assert [text for _, text in u.sentences] == ["Hello Henry!", "I'm Qbot."]
    assert u.sentences[0][0] == 0.0 and 0.3 < u.sentences[1][0] < u.seconds


def test_trim_silence_keeps_a_little_either_side():
    from array import array
    from virtual_robot.voice import trim_silence
    sound = array("h", [0] * 1000 + [9000, -9000] * 50 + [0] * 1000)
    trimmed = array("h", trim_silence(sound.tobytes(), 1000))   # 1000 Hz: KEEP = 30 samples
    assert len(trimmed) == 30 + 100 + 30
    assert trim_silence(bytes(200), 1000) == b""


@pytest.mark.skipif(voice.unavailable_reason() is not None, reason="Piper voice not available here")
def test_no_long_silence_before_a_sentence():
    u = voice.prepare("Hi! Shall we build something amazing today?")   # Piper adds 1.6 s of silence to the 2nd
    second_start = int(u.sentences[1][0] * 25)
    assert max(u.levels[second_start:second_start + 4]) > 0.1   # talking within ~0.15 s of its subtitle


def test_failure_reports_what_aplay_said():
    import subprocess
    voice = VirtualVoice()
    voice._player = subprocess.Popen(["sh", "-c", "echo 'no sound server' >&2; exit 1"],
                                     stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    voice._player.wait()
    assert voice.failure() == "no sound server"
    assert voice.failure() is None  # reported once


def test_no_failure_when_it_played_or_was_stopped():
    import subprocess
    voice = VirtualVoice()
    assert voice.failure() is None
    voice._player = subprocess.Popen(["true"], stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    voice._player.wait()
    assert voice.failure() is None
    voice._player = subprocess.Popen(["sleep", "5"], stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    assert voice.failure() is None  # still playing
    voice.stop()
    assert voice.failure() is None
