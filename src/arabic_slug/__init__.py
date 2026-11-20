"""arabic-slug - URL slugs for Arabic text."""

from .slugify import normalize, slugify, slugify_all, strip_marks, transliterate

__version__ = "0.1.0"

__all__ = ["normalize", "slugify", "slugify_all", "strip_marks", "transliterate", "__version__"]
