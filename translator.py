from googletrans import Translator

def translate(text, dest_lang):
    if dest_lang == "en":
        return text
    try:
        translator = Translator()
        result = translator.translate(text, dest=dest_lang)
        return result.text
    except Exception as e:
        print(f"Translation faild: {e}")
        return text