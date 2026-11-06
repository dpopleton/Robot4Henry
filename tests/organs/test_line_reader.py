import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "organs", "pico_common"))

from line_reader import LineReader  # noqa: E402


def _Reader(max_line=10):
    return LineReader(None, max_line)  # no stream: feed() only


def _feed(reader, text):
    lines = []
    for ch in text:
        reader.feed(ch, lines.append)
    return lines


def test_splits_lines_and_ignores_carriage_returns():
    assert _feed(_Reader(), "Ehappy\r\nD1,2\n") == ["Ehappy", "D1,2"]


def test_a_partial_line_waits_for_its_newline():
    reader = _Reader()
    assert _feed(reader, "Eha") == []
    assert _feed(reader, "ppy\n") == ["Ehappy"]


def test_an_overlong_line_is_dropped_whole_and_the_next_one_still_arrives():
    assert _feed(_Reader(max_line=5), "123456789\nB\n") == ["B"]


def test_drain_reads_from_a_real_stream():
    r, w = os.pipe()
    stream = os.fdopen(r, "rb", buffering=0)
    os.write(w, b"Ehappy\nB\n")
    reader = LineReader(stream, max_line=64)
    reader.feed = lambda ch, on_line, feed=reader.feed: feed(ch.decode(), on_line)
    lines = []
    reader.drain(lines.append)
    assert lines == ["Ehappy", "B"]
    os.close(w)
    stream.close()
