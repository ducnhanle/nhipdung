'Read numbers and money in recorded speech.\n\nNormalize accents and case and parse numeric notation and supported English, Portuguese, Spanish, and Vietnamese number words. Vietnamese numerals keep their meaning through tone marks (sáu six, sau after; năm five, nam south; đô dollar, đó that), so their exact spellings normalize to distinct vi_ tokens read by a positional Vietnamese grammar. User-language lexicons are data and remain independent of the product interface language. Distinguish counts from money using currency context.\n\nparse_number(text) returns a number or None; parse_money(text) returns a monetary amount or None; find_money(normalized_text) returns spans with start, end, amount, and context. Public regex components allow intent detectors to reuse the supported grammar.\n\nKeep actual spoken values and currency semantics; never replace them with demonstration amounts or change decimal interpretation based only on the English interface.'

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass

# ------------------------------------------------------------------ normalization

_PUNCT_MAP = {
    "‘": "'", "’": "'", "´": "'", "`": "'",
    "“": '"', "”": '"', "–": "-", "—": "-",
    " ": " ", " ": " ", "…": "...", "*": "",
}


# Exact Vietnamese spelling -> (token, kind, value). Stripping tone marks would merge a numeral with an unrelated
# word, so these words normalize to their own tokens instead.
VIETNAMESE = {
    "không": ("vi_khong", "digit", 0), "một": ("vi_mot", "digit", 1), "mốt": ("vi_mot_tail", "tail", 1),
    "hai": ("vi_hai", "digit", 2), "ba": ("vi_ba", "digit", 3), "bốn": ("vi_bon", "digit", 4),
    "tư": ("vi_tu", "tail", 4), "năm": ("vi_nam", "digit", 5), "lăm": ("vi_lam", "tail", 5),
    "nhăm": ("vi_nham", "tail", 5), "sáu": ("vi_sau", "digit", 6), "bảy": ("vi_bay", "digit", 7),
    "bẩy": ("vi_bay", "digit", 7), "tám": ("vi_tam", "digit", 8), "chín": ("vi_chin", "digit", 9),
    "mười": ("vi_muoi", "ten", 10), "mươi": ("vi_muoi_tens", "tens", 10), "chục": ("vi_chuc", "tens", 10),
    "trăm": ("vi_tram", "hundred", 100), "linh": ("vi_linh", "link", 0), "lẻ": ("vi_le", "link", 0),
    "nghìn": ("vi_nghin", "scale", 1_000), "ngàn": ("vi_ngan", "scale", 1_000),
    "triệu": ("vi_trieu", "scale", 1_000_000), "củ": ("vi_cu", "scale", 1_000_000),
    "tỷ": ("vi_ty", "scale", 1_000_000_000), "tỉ": ("vi_ty", "scale", 1_000_000_000),
    "rưỡi": ("vi_ruoi", "half", 0.5), "nửa": ("vi_nua", "halfof", 0.5),
    "đồng": ("vi_dong", "currency", None), "đô": ("vi_do", "currency", None),
}
_VI_WORD = re.compile("(?<!\\w)(" + "|".join(sorted({form for w in VIETNAMESE for form in (w, unicodedata.normalize("NFD", w))},
                                                     key=len, reverse=True)) + ")(?!\\w)", re.IGNORECASE)


def normalize(text: str) -> tuple[str, list[int]]:
    """Lowercase + strip accents. Returns (normalized, index map norm_pos -> original_pos)."""
    out: list[str] = []
    index: list[int] = []
    numerals = {m.start(): m for m in _VI_WORD.finditer(text)}
    skip_to = 0
    for i, ch in enumerate(text):
        if i < skip_to:
            continue
        numeral = numerals.get(i)
        if numeral is not None:
            token = VIETNAMESE[unicodedata.normalize("NFC", numeral.group(0)).lower()][0]
            out.extend(token)
            index.extend(min(i + k, numeral.end() - 1) for k in range(len(token)))
            skip_to = numeral.end()
            continue
        mapped = _PUNCT_MAP.get(ch)
        pieces = mapped if mapped is not None else unicodedata.normalize("NFKD", ch)
        for piece in pieces:
            if unicodedata.combining(piece):
                continue
            for c in piece.lower():
                out.append(c)
                index.append(i)
    return "".join(out), index


def normal_value(text: str) -> str:
    return normalize(text)[0]


# ------------------------------------------------------------------ numbers & money

WORD_NUMBERS = {
    "um": 1, "uma": 1, "dois": 2, "duas": 2, "tres": 3, "quatro": 4, "cinco": 5, "seis": 6,
    "sete": 7, "oito": 8, "nove": 9, "dez": 10, "onze": 11, "doze": 12, "treze": 13,
    "quatorze": 14, "catorze": 14, "quinze": 15, "dezesseis": 16, "dezessete": 17,
    "dezoito": 18, "dezenove": 19, "vinte": 20, "trinta": 30, "quarenta": 40,
    "cinquenta": 50, "sessenta": 60, "setenta": 70, "oitenta": 80, "noventa": 90,
    "cem": 100, "cento": 100, "duzentos": 200, "duzentas": 200, "trezentos": 300,
    "quatrocentos": 400, "quinhentos": 500, "seiscentos": 600, "setecentos": 700,
    "oitocentos": 800, "novecentos": 900, "meio": 0.5, "meia": 0.5,
}
# "milão" is spoken slang for one million ("tá fazendo milão")
MULTIPLIERS = {"mil": 1_000, "k": 1_000, "milhao": 1_000_000, "milhoes": 1_000_000, "milao": 1_000_000,
               "miloes": 1_000_000, "mi": 1_000_000, "bilhao": 1_000_000_000, "bilhoes": 1_000_000_000,
               "bi": 1_000_000_000}

# Language lexicons describe recorded speech, not product interface strings.
WORD_NUMBERS.update({
    "zero": 0, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6,
    "seven": 7, "eight": 8, "nine": 9, "ten": 10, "eleven": 11, "twelve": 12,
    "thirteen": 13, "fourteen": 14, "fifteen": 15, "sixteen": 16, "seventeen": 17,
    "eighteen": 18, "nineteen": 19, "twenty": 20, "thirty": 30, "forty": 40,
    "fifty": 50, "sixty": 60, "seventy": 70, "eighty": 80, "ninety": 90,
    "hundred": 100, "half": 0.5,
    "uno": 1, "dos": 2, "tres": 3, "cuatro": 4, "cinco": 5, "seis": 6,
    "siete": 7, "ocho": 8, "nueve": 9, "diez": 10, "veinte": 20, "treinta": 30,
    "cuarenta": 40, "cincuenta": 50, "sesenta": 60, "setenta": 70, "ochenta": 80,
    "noventa": 90, "cien": 100, "ciento": 100,
})
MULTIPLIERS.update({"thousand": 1_000, "million": 1_000_000, "billion": 1_000_000_000,
                    "millon": 1_000_000, "millones": 1_000_000})

WORD_NUMBERS.update({"un": 1, "una": 1, "medio": .5, "media": .5,
                     "dieciseis": 16, "diecisiete": 17, "dieciocho": 18, "diecinueve": 19,
                     "veintiuno": 21, "veintidos": 22, "veintitres": 23, "veinticuatro": 24,
                     "veinticinco": 25, "veintiseis": 26, "veintisiete": 27, "veintiocho": 28,
                     "veintinueve": 29, "doscientos": 200, "trescientos": 300, "cuatrocientos": 400,
                     "quinientos": 500, "seiscientos": 600, "setecientos": 700,
                     "ochocientos": 800, "novecientos": 900})
VI_DIGITS = {t: v for t, k, v in VIETNAMESE.values() if k == "digit"}
VI_TAILS = {t: v for t, k, v in VIETNAMESE.values() if k == "tail"}
VI_SCALES = {t: v for t, k, v in VIETNAMESE.values() if k == "scale"} | {"tr": 1_000_000}
# Units after "mười" or "X mươi": năm stays out ("mười năm" is ten years; fifteen is "mười lăm").
VI_AFTER_TEN = {t: v for t, v in (VI_DIGITS | VI_TAILS).items() if t not in ("vi_khong", "vi_nam", "vi_tu", "vi_mot_tail")}
VI_AFTER_TENS = {t: v for t, v in (VI_DIGITS | VI_TAILS).items() if t not in ("vi_khong", "vi_nam")}
VI_NUMBER_TOKENS = set(VI_DIGITS) | set(VI_TAILS) | {"vi_muoi", "vi_muoi_tens", "vi_chuc", "vi_tram", "vi_linh",
                                                      "vi_le", "vi_ruoi", "vi_nua"}
VI_CURRENCY_RE = r"(?:vi_dong|vi_do(?:[ -]la)?|vnđ|vnd)"
_WORDNUM_ALT = "|".join(sorted(set(WORD_NUMBERS) | VI_NUMBER_TOKENS, key=len, reverse=True))
MULT_RE = "(?:" + "|".join(sorted(set(MULTIPLIERS) | set(VI_SCALES), key=len, reverse=True)) + ")"
# A Vietnamese scale or "củ" alone is not an amount ("đồ cũ", "hàng triệu người"): it needs a number before it.
_MULT_BARE_RE = "(?:" + "|".join(sorted(MULTIPLIERS, key=len, reverse=True)) + ")"
# Match grouping before decimals so a thousands separator cannot truncate a value.
DIGITS_RE = r"(?:\d{1,3}(?:,\d{3})+(?:\.\d{1,2})?|\d{1,3}(?:\.\d{3})+(?:,\d{1,2})?|\d+(?:[.,]\d{1,2})?)(?!\d)"
_WORD_ATOM = rf"(?:{_WORDNUM_ALT}|{MULT_RE})\b"
WORDNUM_RE = rf"{_WORD_ATOM}(?:[ -]+(?:(?:e|and|y)\s+)?(?:a\s+)?{_WORD_ATOM})*"
_NUMBER_ATOM = rf"(?:{DIGITS_RE}|{_WORD_ATOM})"
NUM_RE = rf"{_NUMBER_ATOM}(?:[ -]+(?:(?:e|and|y)\s+)?(?:a\s+)?{_NUMBER_ATOM})*"
CUR_RE = rf"(?:dollars?|pounds?|reais|real|contos?|pilas?|dolares|dolar|euros?|usd|brl|gbp|{VI_CURRENCY_RE})"
DIGIT_COUNT_RE = r"(?:cinco|seis|sete|oito|nove|5|6|7|8|9)\s+digitos\b"
# Explicit currencies take precedence; bare scaled numbers still need context downstream.
MONEY_RE = (
    rf"(?:(?:r\$|us\$|u\$|\$|€|£)\s*{NUM_RE}(?:\s+(?:de\s+)?{CUR_RE}\b)?"
    rf"|(?<![\w$]){NUM_RE}\s+(?:de\s+)?{CUR_RE}\b"
    rf"|(?<![\w$]){NUM_RE}\s*{MULT_RE}\b(?:[ -]+(?:(?:e|and|y)\s+)?(?:a\s+)?{_NUMBER_ATOM})*"
    rf"|(?<![\w$]){NUM_RE}\s*(?:₫|đ(?!\w))"
    rf"|\b{_MULT_BARE_RE}\b(?:[ -]+(?:(?:e|and|y)\s+)?(?:a\s+)?{_NUMBER_ATOM})*|(?<![\w$]){DIGIT_COUNT_RE})"
)
_MONEY_COMPILED = re.compile(MONEY_RE)

# Nouns that make a bare "10 mil" a count, not money.
NON_MONEY_NOUNS = re.compile(
    r"\s*(?:de\s+)?(?:followers?|subscribers?|students?|people|customers?|units?|years?|hours?|seguidor\w*|inscrit\w*|visualiza\w*|views?|curtidas?|likes?|pessoas?|alun\w*|"
    r"clientes?|leads?|vendas?|pedidos?|unidades?|produtos?|pecas?|metros?|km|quilos?|kg|horas?|"
    r"minutos?|dias?|anos?|mensage\w*|comentarios?|compartilhament\w*|downloads?|acessos?|cliques?|"
    r"impress\w*|membros?|usuari\w*|contatos?|numeros?|videos?|posts?|lojas?|fornecedor\w*|itens|"
    r"copias?|livros?|pacotes?|caixas?|vezes|passos|reels|stories|grupos?|mulheres|homens|familias?)\b"
)


@dataclass
class Money:
    start: int
    end: int
    value: float | None
    bare: bool  # no currency marker (R$, reais...): needs context to count as money


def _numeric_literal(token: str) -> float | None:
    if re.fullmatch(r"\d{1,3}(?:,\d{3})+(?:\.\d{1,2})?", token):
        return float(token.replace(",", ""))
    if re.fullmatch(r"\d{1,3}(?:\.\d{3})+(?:,\d{1,2})?", token):
        return float(token.replace(".", "").replace(",", "."))
    if re.fullmatch(r"\d+(?:[.,]\d{1,2})?", token):
        return float(token.replace(",", "."))
    return None


def _vi_group(words: list[str], i: int) -> tuple[float | None, int, bool]:
    """(value, next index, plain) of a Vietnamese group below one thousand starting at words[i]: (None, i, False)
    when none. `plain` marks a lone digit word, which cannot follow a scale as a group of its own."""
    n = len(words)
    literal = _numeric_literal(words[i]) if i < n else None
    if literal is not None:
        return literal, i + 1, False
    hundreds, structured = 0, False
    if i + 1 < n and words[i] in VI_DIGITS and words[i + 1] == "vi_tram":
        hundreds, structured, i = VI_DIGITS[words[i]] * 100, True, i + 2   # "không trăm" keeps the structure
    elif i < n and words[i] == "vi_tram":
        hundreds, structured, i = 100, True, i + 1
    if structured:
        if i + 1 < n and words[i] in ("vi_linh", "vi_le") and words[i + 1] in VI_DIGITS:
            return hundreds + VI_DIGITS[words[i + 1]], i + 2, False   # một trăm linh năm: 105
        if i < n and words[i] == "vi_ruoi":
            return hundreds + 50, i + 1, False                         # trăm rưỡi: 150
        if (i < n and words[i] in VI_AFTER_TENS and not (i + 1 < n and words[i + 1] in ("vi_muoi_tens", "vi_chuc"))):
            return hundreds + (VI_DIGITS | VI_TAILS)[words[i]] * 10, i + 1, False   # một trăm hai: 120
    if i < n and words[i] == "vi_muoi":
        if i + 1 < n and words[i + 1] in VI_AFTER_TEN:
            return hundreds + 10 + VI_AFTER_TEN[words[i + 1]], i + 2, False   # mười lăm: 15
        return hundreds + 10, i + 1, False
    if i + 1 < n and words[i] in VI_DIGITS and words[i + 1] in ("vi_muoi_tens", "vi_chuc"):
        tens = VI_DIGITS[words[i]] * 10
        if i + 2 < n and words[i + 2] in VI_AFTER_TENS:
            return hundreds + tens + VI_AFTER_TENS[words[i + 2]], i + 3, False   # hai mươi mốt: 21
        return hundreds + tens, i + 2, False
    if i < n and words[i] in VI_DIGITS and not structured:
        return VI_DIGITS[words[i]], i + 1, True
    return (hundreds, i, False) if structured else (None, i, False)


def parse_vietnamese(words: list[str]) -> float | None:
    """Value of normalized Vietnamese number tokens (hai triệu rưỡi, một trăm linh năm, 500 nghìn), or None
    when they do not form one number. A digit right after the last scale is its tenth: một triệu hai is 1.2
    million; năm is never read that way, since "hai nghìn năm" is two thousand years."""
    total, i, n, last = 0.0, 0, len(words), None
    while i < n:
        word = words[i]
        if word == "vi_nua" and i + 1 < n and words[i + 1] in VI_SCALES:
            total, last, i = total + VI_SCALES[words[i + 1]] / 2, VI_SCALES[words[i + 1]], i + 2
            continue
        if word in VI_SCALES and last is not None and VI_SCALES[word] > last:
            total, last, i = total * VI_SCALES[word], VI_SCALES[word], i + 1   # một nghìn tỷ
            continue
        group, j, plain = _vi_group(words, i)
        if group is None or (plain and last is not None):
            return None   # after a scale a lone digit is only its tenth ("hai nghìn năm" is two thousand years)
        if j < n and words[j] in VI_SCALES:
            scale = VI_SCALES[words[j]]
            if last is not None and scale >= last:
                return None
            total, last, i = total + group * scale, scale, j + 1
            if i < n and words[i] == "vi_ruoi":
                total, i = total + scale / 2, i + 1
            elif i == n - 1 and words[i] in VI_AFTER_TENS:
                total, i = total + (VI_DIGITS | VI_TAILS)[words[i]] * scale / 10, i + 1
            elif i == n - 1 and re.fullmatch(r"[1-9]", words[i]):
                total, i = total + int(words[i]) * scale / 10, i + 1
            continue
        if last is not None and last <= group:
            return None
        return total + group if j == n else None
    return total if last is not None else None


def parse_number(token: str) -> float | None:
    """Read grouped digits or a compound spoken number without changing its magnitude."""
    token = normal_value(token).strip()
    literal = _numeric_literal(token)
    if literal is not None:
        return literal
    # "500k", "10mil", "2tr": an attached scale is its own word
    token = re.sub(r"(?<=\d)(?=[a-z])", " ", token)
    if any(w.startswith("vi_") or w == "tr" for w in re.split(r"[ -]+", token)):
        return parse_vietnamese([w for w in re.split(r"[ -]+", token) if w])
    words = [w for w in re.split(r"[ -]+", token) if w not in {"e", "and", "y", "a"}]
    if not words or any(w not in WORD_NUMBERS and w not in MULTIPLIERS and _numeric_literal(w) is None for w in words):
        return None
    total, group, last_scale = 0.0, 0.0, 1.0
    for i, word in enumerate(words):
        if word == "hundred":
            group = (group or 1.0) * 100
        elif word in MULTIPLIERS:
            scale = float(MULTIPLIERS[word])
            if scale > last_scale and total:
                total = (total + group) * scale
            else:
                total += (group or 1.0) * scale
            group, last_scale = 0.0, scale
        else:
            value = WORD_NUMBERS.get(word)
            if value is None:
                value = _numeric_literal(word)
            # A terminal half after a scale means half of that scale, not half a unit.
            group += value * last_scale if value == .5 and i == len(words) - 1 and not group else value
    return total + group


def parse_money(text: str) -> float | None:
    """Read the amount in its recorded currency units, preserving grouped decimals."""
    text = normal_value(text)
    text = re.sub(r"(?:r\$|us\$|u\$|\$|€|£|₫)", " ", text)
    text = re.sub(rf"\b(?:de\s+)?{CUR_RE}\b", " ", text)
    text = re.sub(r"(?<=\d)\s*đ(?!\w)", " ", text).strip()
    if re.fullmatch(DIGIT_COUNT_RE, text):
        first = text.split()[0]
        count = WORD_NUMBERS.get(first) if first in WORD_NUMBERS else float(first)
        return float(10 ** (int(count) - 1))
    return parse_number(text)


def currency_prefix(text: str) -> str:
    """Preserve explicit currency; a bare amount carries no inferred currency symbol."""
    text = normal_value(text)
    if "₫" in text or re.search(r"\b(?:vi_dong|vnđ|vnd)\b|\dđ(?!\w)|\d\s+đ(?!\w)", text):
        return "₫"
    if re.search(r"\bvi_do\b", text):
        return "$"
    if re.search(r"r\$|\b(?:brl|reais|real|contos?|pilas?)\b", text):
        return "R$"
    if re.search(r"us\$|u\$|\busd\b", text):
        return "US$"
    if "€" in text or re.search(r"\beuros?\b", text):
        return "€"
    if "£" in text or re.search(r"\b(?:pounds?|gbp)\b", text):
        return "£"
    if "$" in text or re.search(r"\b(?:dollars?|dolares|dolar)\b", text):
        return "$"
    return ""


def find_money(ntext: str) -> list[Money]:
    """Money spans in normalized text."""
    found: list[Money] = []
    for m in _MONEY_COMPILED.finditer(ntext):
        s = m.group(0).rstrip()
        start, end = m.start(), m.start() + len(s)
        bare = not re.search(f'(?:r\\$|\\$|€|£|₫|\\dđ(?!\\w)|\\d\\s+đ(?!\\w)|\\b{CUR_RE}\\b)', s)
        if re.search(r"digitos$", s):
            if re.search(r"\b(?:senha|codigo|numero|pin|token|cep|cpf|cnpj|telefone|celular|chave)\s+(?:\w+\s+)?(?:de|com)\s+$",
                         ntext[max(0, start - 30):start]):
                continue  # A six-digit password is a count, not money.
            bare = False
        counted = NON_MONEY_NOUNS.match(ntext, end) if bare else None
        if counted and not re.match(r"\s+(?:passad[oa]|retrasad[oa]|atras)\b", ntext[counted.end():]):
            continue  # "10 mil seguidores" is a count ("1 milhão ano passado" is still money)
        if bare and re.fullmatch(r"\d+\s*(?:mi|bi)", s):  # "5 mi" is too ambiguous alone
            continue
        if re.search(r"\bvi_dong$", s) and not re.search(rf"\d{{4}}|\d\.\d{{3}}|\b(?:{'|'.join(VI_SCALES)}|k)\b", s):
            continue  # "hai đồng hồ", "không đồng ý": đồng is money with thousands, not alone
        if any(w.startswith("vi_") for w in s.split()) and parse_money(s) is None:
            continue  # Vietnamese words that do not form one number
        if s in ("milao", "miloes") and re.search(r"\b(?:em|de|para|pra|pro|a|ao|da|do|na|no|via|ate)\s+$",
                                                  ntext[max(0, start - 8):start]):
            continue  # "fui pra Milão": the city, not the slang
        found.append(Money(start, end, parse_money(s), bare))
    return found
