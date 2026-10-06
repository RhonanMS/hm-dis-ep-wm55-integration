"""Tests für custom_components/hm_dis_ep_wm55/protocol.py.

Test A und Test B sind die beiden Strings, die am echten HM-Dis-EP-WM55
erfolgreich getestet wurden (siehe HM-Dis-EP-WM55.md).
"""
from __future__ import annotations

import pytest
from hm_dis_ep_wm55 import protocol

TEST_A = (
    "0x02,0x0A,0x12,0x54,0x65,0x78,0x74,0x13,0x81,0x0A,0x0A,0x12,0x54,0x65,0x78,"
    "0x74,0x20,0x31,0x13,0x84,0x0A,0x14,0xC0,0x1C,0xD0,0x1D,0xE0,0x16,0xF0,0x03"
)

TEST_B = (
    "0x02,0x0A,0x12,0x54,0x65,0x78,0x74,0x13,0x81,0x0A,0x0A,0x12,0x54,0x65,0x78,"
    "0x74,0x20,0x31,0x13,0x84,0x0A,0x14,0xC5,0x1C,0xD0,0x1D,0xE0,0x16,0xF1,0x03"
)


def test_build_submit_string_matches_verified_test_a():
    result = protocol.build_submit_string(
        line2="Text",
        icon2="ein",
        line3="",
        icon3=None,
        line4="Text 1",
        icon4="fehler",
        sound="aus",
        repeat=1,
        distance=10,
        led="aus",
    )
    assert result == TEST_A


def test_build_submit_string_matches_verified_test_b():
    result = protocol.build_submit_string(
        line2="Text",
        icon2="ein",
        line3="",
        icon3=None,
        line4="Text 1",
        icon4="fehler",
        sound="kurz_kurz",
        repeat=1,
        distance=10,
        led="rot",
    )
    assert result == TEST_B


def test_empty_line_without_icon_is_just_block_end():
    assert protocol.build_line_block(None, None) == ["0x0A"]
    assert protocol.build_line_block("", None) == ["0x0A"]


def test_icon_only_line_omits_text_prefix_content_but_keeps_structure():
    assert protocol.build_line_block(None, "aus") == ["0x12", "0x13", "0x80", "0x0A"]


def test_umlauts_are_encoded_natively():
    assert protocol.encode_text("Äöü ß") == [
        "0x5B",
        "0x7C",
        "0x7D",
        "0x20",
        "0x5F",
    ]


def test_unknown_character_falls_back_to_question_mark(caplog):
    with caplog.at_level("WARNING"):
        tokens = protocol.encode_text("A€B")
    assert tokens == ["0x41", "0x3F", "0x42"]
    assert "nicht unterstützt" in caplog.text


def test_text_longer_than_12_chars_is_truncated_with_warning(caplog):
    with caplog.at_level("WARNING"):
        tokens = protocol.encode_text("123456789012345")
    assert len(tokens) == 12
    assert tokens == [
        "0x31", "0x32", "0x33", "0x34", "0x35", "0x36",
        "0x37", "0x38", "0x39", "0x30", "0x31", "0x32",
    ]
    assert "gekürzt" in caplog.text


@pytest.mark.parametrize(
    ("repeat", "expected"),
    [
        (1, "0xD0"),
        (2, "0xD1"),
        (15, "0xDE"),
        (0, "0xDF"),
    ],
)
def test_repeat_to_code(repeat, expected):
    assert protocol.repeat_to_code(repeat) == expected


def test_repeat_to_code_clamps_out_of_range(caplog):
    with caplog.at_level("WARNING"):
        assert protocol.repeat_to_code(20) == "0xDE"
    assert "außerhalb des gültigen Bereichs" in caplog.text


@pytest.mark.parametrize(
    ("distance", "expected"),
    [
        (1, "0xE0"),
        (10, "0xE0"),
        (11, "0xE1"),
        (20, "0xE1"),
        (160, "0xEF"),
    ],
)
def test_distance_to_code(distance, expected):
    assert protocol.distance_to_code(distance) == expected


def test_distance_to_code_clamps_out_of_range(caplog):
    with caplog.at_level("WARNING"):
        assert protocol.distance_to_code(500) == "0xEF"
    assert "außerhalb des gültigen Bereichs" in caplog.text


def test_unknown_icon_raises_value_error():
    with pytest.raises(ValueError):
        protocol.build_line_block("Text", "nicht_existent")
