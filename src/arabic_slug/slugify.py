"""Arabic-aware slug generation."""

from __future__ import annotations

import re
import unicodedata
from typing import Iterable

TRANSLITERATION = {
    "ا": "a",
    "أ": "a",
    "إ": "i",
    "آ": "a",
    "ٱ": "a",
    "ب": "b",
    "ت": "t",
    "ث": "th",
    "ج": "j",
    "ح": "h",
    "خ": "kh",
    "د": "d",
    "ذ": "dh",
    "ر": "r",
    "ز": "z",
    "س": "s",
    "ش": "sh",
    "ص": "s",
    "ض": "d",
    "ط": "t",
    "ظ": "z",
    "ع": "a",
    "غ": "gh",
    "ف": "f",
    "ق": "q",
    "ك": "k",
    "ل": "l",
    "م": "m",
    "ن": "n",
    "ه": "h",
    "و": "w",
    "ي": "y",
    "ى": "a",
    "ة": "a",
    "ء": "",
    "ؤ": "w",
    "ئ": "y",
}

DIACRITICS_RE = re.compile(r"[\u0610-\u061a\u064b-\u065f\u0670\u06d6-\u06ed]")
TATWEEL = "\u0640"

ARABIC_INDIC_DIGITS = str.maketrans("٠١٢٣٤٥٦٧٨٩", "0123456789")
EXTENDED_ARABIC_DIGITS = str.maketrans("۰۱۲۳۴۵۶۷۸۹", "0123456789")


def strip_marks(text: str) -> str:
    """Remove diacritics and tatweel."""
    return DIACRITICS_RE.sub("", text.replace(TATWEEL, ""))


def normalize(text: str) -> str:
    """Normalise Arabic forms and digits so slugs are stable."""
    text = unicodedata.normalize("NFKC", strip_marks(text))
    text = text.translate(ARABIC_INDIC_DIGITS).translate(EXTENDED_ARABIC_DIGITS)
    return text


def transliterate(text: str) -> str:
    return "".join(TRANSLITERATION.get(char, char) for char in text)


def _clean(value: str, separator: str) -> str:
    value = re.sub(r"[^\w\s" + re.escape(separator) + r"]+", " ", value, flags=re.UNICODE)
    value = re.sub(r"[\s_]+", separator, value)
    value = re.sub(re.escape(separator) + r"{2,}", separator, value)
    return value.strip(separator)


def slugify(
    text: str,
    mode: str = "translit",
    separator: str = "-",
    max_length: int = 80,
    lowercase: bool = True,
) -> str:
    """Turn *text* into a URL-safe slug.

    ``mode="translit"`` replaces Arabic letters with Latin approximations.
    ``mode="keep"`` keeps Arabic letters (valid in URLs) and only cleans separators.
    """
    if mode not in ("translit", "keep"):
        raise ValueError("mode must be 'translit' or 'keep'")
    if not text:
        return ""

    value = normalize(text)
    if mode == "translit":
        value = transliterate(value)

    slug = _clean(value, separator)
    if lowercase:
        slug = slug.lower()

    if max_length and len(slug) > max_length:
        slug = slug[:max_length]
        if separator in slug:
            slug = slug.rsplit(separator, 1)[0]
        slug = slug.strip(separator)

    return slug


def slugify_all(
    values: Iterable[str],
    mode: str = "translit",
    separator: str = "-",
    max_length: int = 80,
    lowercase: bool = True,
) -> list:
    return [
        slugify(value, mode=mode, separator=separator, max_length=max_length, lowercase=lowercase)
        for value in values
    ]
