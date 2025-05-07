from googletrans import Translator

translator = Translator()

def translate(text, lang):
    try:
        result = translator.translate(text, dest=lang)
        return result.text
    except Exception as e:
        print(f"Translation faild: {e}")
        return text