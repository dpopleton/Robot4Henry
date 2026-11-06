"""
Turns speech audio into the mouth's voice levels (D-024): how loud the
voice is in each 1/25 s slice, 0.0-1.0, ready to send as L lines in step
with playback. Host-side; used by the virtual robot's voice now and by
text-to-speech on the robot later (R-307).

Levels are scaled to each utterance's own loud parts, so a quiet voice
still opens the mouth fully on its stressed syllables, and quiet slices
(gaps between words) drop to 0.
"""

import math
from array import array

RATE = 25            # levels per second
LOUD_PERCENTILE = 0.95   # this share of slices sit at or below "fully open"
CURVE = 0.7          # <1 lifts quieter sounds, so soft syllables still show
SILENCE = 0.06       # below this (after scaling) counts as a gap: 0


def levels_from_audio(samples, sample_rate, rate=RATE):
    """samples: mono signed 16-bit (an array('h'), list, or bytes)."""
    if isinstance(samples, (bytes, bytearray)):
        samples = array("h", samples)
    window = max(1, round(sample_rate / rate))
    rms = []
    for start in range(0, len(samples), window):
        chunk = samples[start:start + window]
        rms.append(math.sqrt(sum(s * s for s in chunk) / len(chunk)))
    if not rms:
        return []
    loud = sorted(rms)[min(len(rms) - 1, int(len(rms) * LOUD_PERCENTILE))] or 1.0
    levels = []
    for value in rms:
        level = min(1.0, value / loud) ** CURVE
        levels.append(0.0 if level < SILENCE else level)
    return levels
