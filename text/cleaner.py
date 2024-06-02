from text import waitau, cleaned_text_to_sequence


language_module_map = {"WAITAU": waitau}


def clean_text(text, language, g2p_bypass=False):
    language_module = language_module_map[language]
    if not g2p_bypass:
        norm_text = language_module.text_normalize(text)
    else:
        norm_text = text.split()
    phones, tones, word2ph = language_module.g2p(norm_text, g2p_bypass)
    return norm_text, phones, tones, word2ph


def clean_text_bert(text, language, g2p_bypass=False):
    language_module = language_module_map[language]
    if not g2p_bypass:
        norm_text = language_module.text_normalize(text)
    else:
        norm_text = text.split()
    phones, tones, word2ph = language_module.g2p(norm_text, g2p_bypass)
    bert = language_module.get_bert_feature(norm_text, word2ph)
    return phones, tones, bert


def text_to_sequence(text, language):
    norm_text, phones, tones, word2ph = clean_text(text, language)
    return cleaned_text_to_sequence(phones, tones, language)


if __name__ == "__main__":
    pass
