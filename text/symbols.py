punctuation = ["!", "?", "…", ",", ".", "'", "-"]
pu_symbols = punctuation + ["SP", "UNK"]
pad = "_"

# waitau

waitau_symbols = [
    "a",
    "ai",
    "ak",
    "am",
    "an",
    "ang",
    "ap",
    "at",
    "au",
    "äi",
    "äk",
    "äm",
    "än",
    "äng",
    "äp",
    "ät",
    "äu",
    "b",
    "c",
    "d",
    "e",
    "ei",
    "ek",
    "eng",
    "öi",
    "eon",
    "öt",
    "eu",
    "em",
    "en",
    "ep",
    "et",
    "f",
    "g",
    "gw",
    "h",
    "i",
    "ik",
    "im",
    "in",
    "ing",
    "ip",
    "it",
    "iu",
    "y",
    "k",
    "kw",
    "l",
    "m",
    "n",
    "ng",
    "o",
    "ö",
    "ök",
    "öng",
    "oi",
    "ok",
    "on",
    "ong",
    "ot",
    "ou",
    "p",
    "s",
    "t",
    "u",
    "ui",
    "uk",
    "un",
    "ung",
    "ut",
    "w",
    "ü",
    "ün",
    "üt",
    "oing",
    "z",
    "ä",
    "äing",
    "æing",
    "æk",
    "æng",
    "ön",
    "ük",
    "üng",
]
num_waitau_tones = 7

# combine all symbols
normal_symbols = sorted(set(waitau_symbols))
symbols = [pad] + normal_symbols + pu_symbols
symbols = symbols + sorted((set(waitau_symbols) - set(symbols)))
sil_phonemes_ids = [symbols.index(i) for i in pu_symbols]

# combine all tones
num_tones = num_waitau_tones

# language maps
language_id_map = {"WAITAU": 0}
num_languages = len(language_id_map.keys())

language_tone_start_map = {
    "WAITAU": 0,
}

if __name__ == "__main__":
    a = set(waitau_symbols)
    print(sorted(a))
