import re
import unicodedata
import cn2an
import pinyin_jyutping
import pycantonese

from text.symbols import punctuation
# from symbols import punctuation

from functools import reduce


def normalizer(x):
    return cn2an.transform(x, "an2cn")


j = pinyin_jyutping.PinyinJyutping()

INITIALS = [
    "äi",
    "äm",
    "äng",
    "äu",
    "äp",
    "ät",
    "äk",
    "æ",
    "a",
    "p",
    "b",
    "e",
    "ts",
    "t",
    "dz",
    "d",
    "kw",
    "k",
    "gw",
    "g",
    "f",
    "h",
    "l",
    "m",
    "ng",
    "n",
    "s",
    "w",
    "c",
    "z",
    "y",
    "ong",
    "on",
    "ou",
    "oi",
    "ok",
    "o",
    "uk",
    "ung",
]


rep_map = {
    "￼": ",",
    "：": ",",
    "︰": ",",
    "；": ",",
    "，": ",",
    "。": ".",
    "！": "!",
    "？": "?",
    "﹖": "?",
    "﹗": "!",
    "\n": ".",
    "·": ",",
    "、": ",",
    "丶": ",",
    "...": "…",
    "⋯": "…",
    "$": ".",
    "“": "'",
    "”": "'",
    '"': "'",
    "‘": "'",
    "’": "'",
    "（": "'",
    "）": "'",
    "(": "'",
    ")": "'",
    "《": "'",
    "》": "'",
    "【": "'",
    "】": "'",
    "[": "'",
    "]": "'",
    "—": "-",
    "～": "-",
    "~": "-",
    "「": "'",
    "」": "'",
    "_": "-",
}

replacement_chars = {
    "ㄧ": "一",
    "—": "一",
    "更": "更",
    "不": "不",
    "料": "料",
    "聯": "聯",
    "行": "行",
    "利": "利",
    "謢": "護",
    "岀": "出",
    "鎭": "鎮",
    "戯": "戲",
    "旣": "既",
    "立": "立",
    "來": "來",
    "年": "年",
    "㗇": "蝦",
}


def replace_punctuation(text):
    # text = text.replace("嗯", "恩").replace("呣", "母")
    pattern = re.compile("|".join(re.escape(p) for p in rep_map.keys()))

    replaced_text = pattern.sub(lambda x: rep_map[x.group()], text)

    replaced_text = "".join(
        c
        for c in replaced_text
        if unicodedata.name(c, "").startswith("CJK UNIFIED IDEOGRAPH")
        or c in punctuation
    )

    return replaced_text


def replace_chars(text):
    for k, v in replacement_chars.items():
        text = text.replace(k, v)
    return text


def text_normalize(text):
    text = normalizer(text)
    text = replace_punctuation(text)
    text = replace_chars(text)
    return text


def rom_to_initials_finals_tones(jyuping_syllables):
    initials_finals = []
    tones = []
    word2ph = []

    for syllable in jyuping_syllables:
        if syllable in punctuation:
            initials_finals.append(syllable)
            tones.append(0)
            word2ph.append(1)  # Add 1 for punctuation
        else:
            try:
                tone = int(syllable[-1])
                syllable_without_tone = syllable[:-1]
            except ValueError:
                tone = 0
                syllable_without_tone = syllable

            assert str(tone) in "1234560"

            for initial in INITIALS:
                if syllable_without_tone.startswith(initial):
                    if syllable_without_tone.startswith("nga"):
                        initials_finals.extend(
                            [
                                syllable_without_tone[:2],
                                syllable_without_tone[2:] or syllable_without_tone[-1],
                            ]
                        )
                        tones.extend([tone, tone])
                        word2ph.append(2)
                    else:
                        final = syllable_without_tone[len(initial) :] or initial[-1]
                        initials_finals.extend([initial, final])
                        tones.extend([tone, tone])
                        word2ph.append(2)
                    break
    print(initials_finals)
    assert len(initials_finals) == len(tones)
    assert sum(word2ph) == len(initials_finals)
    return initials_finals, tones, word2ph


def get_jyutping(text):
    converted_text = j.jyutping(text, tone_numbers=True, spaces=True)
    converted_words = converted_text.split()

    # # replace ... with …
    # converted_text = re.sub(r"\.{2,}", "…", converted_text)
    # # replace -- with -
    # converted_text = re.sub(r"-{2,}", "-", converted_text)

    for i, word in enumerate(converted_words):
        if set(word) <= set(text) - set(punctuation):
            converted_word = pycantonese.characters_to_jyutping(word)[0][1]
            converted_words[i] = converted_word

        if (
            converted_words[i] not in punctuation
            and re.search(r"^[a-zA-Z]+[1-6]$", converted_words[i]) is None
        ):
            raise ValueError(
                f"Failed to convert {converted_words[i]}, {converted_text}"
            )

    jyutping_sentence = " ".join(converted_words)

    for symbol in punctuation:
        jyutping_sentence = jyutping_sentence.replace(symbol, " " + symbol + " ")
    jyutping_array = jyutping_sentence.split()

    return jyutping_array


def jyutping2waitau(j):
    ROM_MAPPING = {
        "a": "ä",
        "ää": "a",
        "ae": "æ",
        "oe": "ö",
        "eo": "ö",
        "yu": "ü",
        "j": "y",
    }

    return re.sub(
        "(g|k)u(?!ng|k)",
        "\\1wu",
        reduce(lambda pron, rule: pron.replace(*rule), ROM_MAPPING.items(), j),
    )


def get_bert_feature(text, word2ph):
    from text import cantonese_bert

    return cantonese_bert.get_bert_feature(text, word2ph)


def g2p(text, g2p_bypass=False):
    word2ph = []
    if not g2p_bypass:
        jyuping = get_jyutping(text)
        rom = [jyutping2waitau(j) for j in jyuping]
        phones, tones, word2ph = rom_to_initials_finals_tones(rom)
    else:
        phones, tones, word2ph = rom_to_initials_finals_tones(text)
    phones = ["_"] + phones + ["_"]
    tones = [0] + tones + [0]
    word2ph = [1] + word2ph + [1]
    return phones, tones, word2ph


def test_dataset(dataset, metadata):
    import csv
    import tqdm

    with open(metadata, "r", encoding="utf-8") as _file_:
        if dataset == "ciugo":
            reader = list(csv.reader(_file_, delimiter="|"))
            for row in tqdm.tqdm(reader, desc="Processing dataset"):
                _, _, rom_text = row
                rom_syllables = rom_text.split()
                try:
                    phones, tones, word2ph = rom_to_initials_finals_tones(rom_syllables)
                    if not len(word2ph) == len(text):
                        print(f"word2ph not fit!: {rom_text}")
                        print(f"phones: {phones}")
                        print(f"tones: {tones}")
                        print(f"word2ph: {word2ph}")
                    assert len(word2ph) == len(text)
                    # print(phones)
                except Exception as e:
                    # print(f"Error converting line: {row}")
                    # print(f"Exception: {e}")
                    print("")
        else:
            with open(metadata, "r", encoding="utf-8") as _file_:
                for line in _file_:
                    text = line.strip().split("|")[-1]
                    text = text_normalize(text)
                    try:
                        phones, tones, word2ph = g2p(text)
                        if not len(word2ph) == len(text) + 2:
                            print(f"word2ph not fit!: {text}")
                            print(f"phones: {phones}")
                            print(f"tones: {tones}")
                            print(f"word2ph: {word2ph}")
                        assert len(word2ph) == len(text) + 2
                        # print(phones)
                    except Exception as e:
                        # print(f"Error converting text: {text}")
                        # print(f"Exception: {e}")
                        print("")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", type=str, choices=["ciugo", "list"])
    parser.add_argument("--metadata", type=str)
    args = parser.parse_args()

    if args.dataset:
        if args.metadata is None:
            args.metadata = "./metadata.csv"
        test_dataset(args.dataset, args.metadata)
    else:
        g2p_bypass = False
        # from text.cantonese_bert import get_bert_feature

        # text = "你點解會咁柒㗎？我真係唔該晒你呀！"
        text = "佢哋最叻咪就係去㗇人傷害人,得個殼咋!"
        text = "不妨聽聽西廂記裏面鶯鶯嘅唱詞." # g2p_bypass = False
        text = "ni1 seng4 yäk6 co1 go2 täu4" # g2p_bypass = True
        text = "咗"

        if not g2p_bypass:
            text = text_normalize(text)
            print(text)
        else:
            text = text.split() # text: list
            print(text)
        phones, tones, word2ph = g2p(text, g2p_bypass)
        # bert = get_bert_feature(text, word2ph)

        # print(phones, tones, word2ph, bert.shape)
        print(phones, tones, word2ph)
