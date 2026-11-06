"""
Qbot's voice in the virtual robot: speaks text in Henry's chosen Piper
voice (R-307) through this computer's speakers, and works out the mouth
levels from the same audio (organs/mouth/levels.py, D-024) so the
virtual mouth can be judged against real speech.

prepare() is slow (loading the voice ~0.5 s the first time, then roughly
0.1 s per sentence on the dev machine), so call it off the UI thread.
Each sentence is synthesised on its own, so we know when it starts:
that's what the subtitles show. Each is trimmed of silence at both ends
and joined with a short pause: Piper sometimes puts over a second of
silence before a sentence (e.g. "Shall we build something amazing
today?" starts with 1.6 s of nothing), which looks and sounds like a stall.
"""

import os
import re
import shutil
import subprocess
import threading
from array import array
from dataclasses import dataclass, field

from config.settings import VOICE_MODEL
from organs.mouth.levels import RATE, levels_from_audio


SILENCE = 500          # |sample| at or below this is silence (16-bit)
KEEP_SECONDS = 0.03    # keep this much either side of the sound when trimming
PAUSE_SECONDS = 0.2    # between sentences


def trim_silence(audio: bytes, sample_rate: int) -> bytes:
    samples = array("h", audio)
    loud = [i for i, s in enumerate(samples) if abs(s) > SILENCE]
    if not loud:
        return b""
    keep = int(KEEP_SECONDS * sample_rate)
    return samples[max(0, loud[0] - keep):loud[-1] + 1 + keep].tobytes()


@dataclass
class Utterance:
    audio: bytes                 # mono signed 16-bit
    sample_rate: int
    levels: list                 # 0.0-1.0, RATE per second
    sentences: list = field(default_factory=list)   # [(start_seconds, text)]

    @property
    def seconds(self):
        return len(self.audio) / 2 / self.sample_rate

    def sentence_at(self, seconds):
        current = ""
        for start, text in self.sentences:
            if seconds >= start:
                current = text
        return current


def split_sentences(text):
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", text.strip()) if s.strip()]


class VirtualVoice:
    def __init__(self, model_path=VOICE_MODEL):
        self.model_path = model_path
        self._voice = None
        self._player = None

    def unavailable_reason(self):
        """None if it can speak, else why not (shown on the bench)."""
        try:
            import piper  # noqa: F401
        except ImportError as e:
            import sys
            return (f"Piper won't load in {sys.executable} ({e}). "
                    'Is this the project\'s .venv? If so: pip install -e ".[voice]"')
        if not os.path.exists(self.model_path):
            return f"No voice model at {self.model_path}"
        if not shutil.which("aplay"):
            return "No aplay to play sound with (sudo apt install alsa-utils)"
        return None

    def prepare(self, text):
        if self._voice is None:
            from piper import PiperVoice
            self._voice = PiperVoice.load(self.model_path)
        audio, sentences, sample_rate = bytearray(), [], 22050
        for sentence in split_sentences(text):
            said = bytearray()
            for chunk in self._voice.synthesize(sentence):
                sample_rate = chunk.sample_rate
                said += chunk.audio_int16_bytes
            said = trim_silence(bytes(said), sample_rate)
            if not said:
                continue
            if audio:
                audio += bytes(2 * int(PAUSE_SECONDS * sample_rate))
            sentences.append((len(audio) / 2 / sample_rate, sentence))
            audio += said
        audio = bytes(audio)
        return Utterance(audio, sample_rate, levels_from_audio(audio, sample_rate, RATE), sentences)

    def play(self, utterance):
        """Start playing and return at once."""
        self.stop()
        self._player = subprocess.Popen(
            ["aplay", "-q", "-t", "raw", "-f", "S16_LE", "-c", "1", "-r", str(utterance.sample_rate), "-"],
            stdin=subprocess.PIPE, stderr=subprocess.PIPE,
        )
        player = self._player

        def feed():
            try:
                player.stdin.write(utterance.audio)
                player.stdin.close()
            except (BrokenPipeError, ValueError):
                pass  # stopped early

        threading.Thread(target=feed, daemon=True).start()

    def failure(self):
        """Why the sound didn't play, once aplay has given up — else None.
        (Without this a broken sound setup is just silence.)"""
        player = self._player
        if player is None or player.poll() is None or player.returncode <= 0:
            return None  # playing, finished fine, or stopped by us
        self._player = None
        said = player.stderr.read().decode(errors="replace").strip()
        return said or f"aplay stopped with code {player.returncode}"

    def stop(self):
        if self._player and self._player.poll() is None:
            self._player.kill()
        self._player = None
