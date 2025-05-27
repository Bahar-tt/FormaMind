from translations import translations

def translate(text, lang="en"):
    """
    Translate text to the specified language.
    If translation is not found, returns the original text.
    """
    if lang in translations and text in translations[lang]:
        return translations[lang][text]
    return text