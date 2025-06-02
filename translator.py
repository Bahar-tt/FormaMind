from deep_translator import GoogleTranslator

def translate(text, lang):
    try:
        translator = GoogleTranslator(source='auto', target=lang)
        result = translator.translate(text)
        return result
    except Exception as e:
        print(f"Translation failed: {e}")
        return text