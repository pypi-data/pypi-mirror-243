from enum import IntEnum


class Key(IntEnum):
    BACKSPACE = 8
    ENTER = 13
    ESC = 27
    BLANK = 32

    D0 = 48
    D1 = 49
    D2 = 50
    D3 = 51
    D4 = 52
    D5 = 53
    D6 = 54
    D7 = 55
    D8 = 56
    D9 = 57

    LEFT = 81
    UP = 82
    RIGHT = 83
    DOWN = 84
    PAGE_UP = 85
    PAGE_DOWN = 86
    INS = 99
    F1 = 190
    F2 = 191
    F3 = 192
    F4 = 193
    F5 = 194
    F6 = 195
    F7 = 196
    F8 = 197
    F9 = 198
    F10 = 199
    DEL = 255


class Flag(IntEnum):
    CTRL = 8
    ALT = 32
    SHIFT = 16


def test_key():
    assert Key.ESC == 27
    assert Key.D9 - Key.D0 == 9
