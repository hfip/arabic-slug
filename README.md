# arabic-slug

Slug generation that knows Arabic exists.

Most slug libraries either strip the text or leave a row of dashes. Arabic also brings
diacritics, tatweel, four shapes of alef and two sets of digits, none of which belong in a
URL.

```python
from arabic_slug import slugify

slugify("مرحبا بالعالم")  # "mrhba-balaalm"
slugify("مرحبا بالعالم", mode="keep")  # "مرحبا-بالعالم"
slugify("تقرير ٢٠٢٦")  # "tqryr-2026"
slugify("واحد اثنان ثلاثة", max_length=8)  # "wahd"
```

One honest note about the transliteration: it is letter by letter. Arabic does not write
short vowels, so `مرحبا` becomes `mrhba` and not `marhaba`. Inventing vowels needs a
dictionary, not a mapping table, and this package does not pretend otherwise. If you want
the readable Arabic form in the URL, use `mode="keep"`.

## Two modes

| mode | output | when |
| --- | --- | --- |
| `translit` (default) | `mrhba-balaalm` | you need ASCII-only URLs |
| `keep` | `مرحبا-بالعالم` | modern browsers, readable links |

Both modes remove tashkeel, tatweel, punctuation and emoji, collapse runs of separators,
convert Arabic-Indic digits to ASCII, and truncate at a word boundary instead of mid-word.

## Install

```bash
pipx install git+https://github.com/hfip/arabic-slug.git
```

Or as a library: `pip install git+https://github.com/hfip/arabic-slug.git`.

## CLI

```bash
arabic-slug "مرحبا بالعالم"
arabic-slug --mode keep "مقال عن التقنية"
arabic-slug --separator _ --max-length 40 "عنوان طويل جداً"
cat titles.txt | arabic-slug --stdin
```

Exit codes: `0` success, `2` nothing to slugify.

## API

```python
slugify(text, mode="translit", separator="-", max_length=80, lowercase=True)
slugify_all(["عنوان", "آخر"])
normalize("٢٠٢٦")  # "2026"
strip_marks("مَرْحَبًا")  # "مرحبا"
```

## بالعربي

<div dir="rtl" align="right">

معظم مكتبات الـ slug تطلع `-----` أو تحذف النص العربي كامل. هذي تتعامل مع التشكيل
والتطويل وأشكال الألف المختلفة والأرقام العربية:

```bash
arabic-slug "مرحبا بالعالم"
```

التحويل الصوتي حرف بحرف، فـ`مرحبا` تصير `mrhba` مو `marhaba` — لأن الحركات القصيرة ما
هي مكتوبة أصلاً. إذا تبي العربية تبقى في الرابط استخدم `--mode keep`.

</div>

## License

MIT. See [LICENSE](LICENSE).
