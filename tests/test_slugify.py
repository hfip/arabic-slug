import pytest

from arabic_slug import normalize, slugify, slugify_all, strip_marks
from arabic_slug.cli import main


def test_strip_marks_removes_tashkeel_and_tatweel():
    assert strip_marks("مَرْحَبًا") == "مرحبا"
    assert strip_marks("مـــرحبا") == "مرحبا"


def test_normalize_converts_arabic_digits():
    assert normalize("٢٠٢٦") == "2026"
    assert normalize("۱۴۰۴") == "1404"


def test_transliteration_basic():
    assert slugify("السلام") == "alslam"
    assert slugify("مرحبا") == "mrhba"


def test_words_are_joined_with_one_separator():
    assert slugify("مرحبا   بالعالم") == "mrhba-balaalm"


def test_punctuation_and_emoji_are_dropped():
    assert slugify("هل هذا صحيح؟ 🙂") == "hl-hdha-shyh"


def test_keep_mode_keeps_arabic():
    assert slugify("مرحبا بالعالم", mode="keep") == "مرحبا-بالعالم"


def test_digits_survive():
    assert slugify("تقرير ٢٠٢٦") == "tqryr-2026"


def test_max_length_cuts_at_a_word_boundary():
    slug = slugify("واحد اثنان ثلاثة اربعة", max_length=12)
    assert len(slug) <= 12
    assert not slug.endswith("-")


def test_custom_separator():
    assert slugify("مرحبا بالعالم", separator="_") == "mrhba_balaalm"


def test_keep_case():
    assert slugify("Hello مرحبا", lowercase=False) == "Hello-mrhba"


def test_empty_and_symbols_only():
    assert slugify("") == ""
    assert slugify("!!! ???") == ""


def test_unknown_mode_is_rejected():
    with pytest.raises(ValueError):
        slugify("نص", mode="bogus")


def test_slugify_all():
    assert slugify_all(["مرحبا", "شكرا"]) == ["mrhba", "shkra"]


def test_cli_prints_slugs(capsys):
    assert main(["مرحبا بالعالم"]) == 0
    assert capsys.readouterr().out.strip() == "mrhba-balaalm"


def test_cli_keep_mode(capsys):
    assert main(["--mode", "keep", "مرحبا"]) == 0
    assert capsys.readouterr().out.strip() == "مرحبا"


def test_cli_stdin(capsys, monkeypatch):
    import io

    monkeypatch.setattr("sys.stdin", io.StringIO("مرحبا\nشكرا\n"))
    assert main(["--stdin"]) == 0
    assert capsys.readouterr().out.split() == ["mrhba", "shkra"]


def test_cli_without_arguments_returns_usage():
    assert main([]) == 2
